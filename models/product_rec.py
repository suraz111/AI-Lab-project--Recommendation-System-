"""
Product Recommendation Engine (RECOM.ai)
Specialized for Indian tech & lifestyle brands with pricing in INR (₹),
category filtering, budget constraints, and feature similarity ranking.
"""

import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ProductRecommender:
    def __init__(
        self,
        data_path: str = "data/cleaned/products_clean.csv",
        ratings_path: str = "data/cleaned/product_ratings_clean.csv"
    ):
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Product dataset not found at {data_path}")

        self.products_df = pd.read_csv(data_path)
        self.ratings_df = pd.read_csv(ratings_path) if os.path.exists(ratings_path) else pd.DataFrame()
        
        self.products_df["content_features"] = self.products_df["content_features"].fillna("")
        
        # Build TF-IDF vectorizer over content features
        self.tfidf = TfidfVectorizer(stop_words="english", max_features=3000)
        self.tfidf_matrix = self.tfidf.fit_transform(self.products_df["content_features"])

    def get_categories(self) -> list:
        """Returns sorted list of product categories."""
        return ["All"] + sorted(self.products_df["category"].dropna().unique().tolist())

    def get_brands(self) -> list:
        """Returns sorted list of Indian brands in catalog."""
        return ["All"] + sorted(self.products_df["brand"].dropna().unique().tolist())

    def get_price_range(self) -> tuple:
        """Returns (min_price, max_price) in INR."""
        min_p = int(self.products_df["price_inr"].min())
        max_p = int(self.products_df["price_inr"].max())
        return min_p, max_p

    def recommend(
        self,
        category: str = "All",
        max_price_inr: int = None,
        brand: str = "All",
        query_text: str = "",
        top_n: int = 5,
        alpha: float = 0.6
    ) -> list:
        """
        Generates Top-N product recommendations.
        
        Parameters:
            category: 'All' or specific category (e.g. 'Audio', 'Wearables').
            max_price_inr: Upper budget cap in INR (₹).
            brand: 'All' or specific brand (e.g. 'boAt', 'Noise').
            query_text: Search terms (e.g. 'noise cancelling ANC', 'mechanical keyboard').
            top_n: Number of recommendations to return.
            alpha: Weight for Content Match [0.0 - 1.0].
        """
        df = self.products_df.copy()

        # 1. Filter by Category
        if category and category.lower() != "all":
            df = df[df["category"].str.lower() == category.lower()]

        # 2. Filter by Brand
        if brand and brand.lower() != "all":
            df = df[df["brand"].str.lower() == brand.lower()]

        # 3. Filter by Price Cap in INR
        if max_price_inr is not None and max_price_inr > 0:
            filtered_by_price = df[df["price_inr"] <= max_price_inr]
            if not filtered_by_price.empty:
                df = filtered_by_price

        if df.empty:
            df = self.products_df.copy()

        # 4. Content Feature Matching
        query_parts = []
        if category and category.lower() != "all":
            query_parts.append(category)
        if brand and brand.lower() != "all":
            query_parts.append(brand)
        if query_text and query_text.strip():
            query_parts.append(query_text.strip())

        full_query = " ".join(query_parts).strip()

        if full_query:
            query_vec = self.tfidf.transform([full_query])
            sub_tfidf = self.tfidf.transform(df["content_features"].fillna(""))
            content_sim = cosine_similarity(query_vec, sub_tfidf).flatten()
        else:
            content_sim = np.ones(len(df)) * 0.5

        # 5. Rating Normalization
        max_rating = 5.0
        rating_score = (df["rating"].fillna(4.0) / max_rating).values

        # 6. Hybrid Score Computation
        alpha_clamped = max(0.0, min(1.0, float(alpha)))
        hybrid_score = (alpha_clamped * content_sim) + ((1.0 - alpha_clamped) * rating_score)
        df["match_score"] = (hybrid_score * 100).round(1)

        # 7. Sort and retrieve Top-N
        ranked_df = df.sort_values(by=["match_score", "rating"], ascending=False).head(top_n)

        results = []
        for _, row in ranked_df.iterrows():
            brand_name = str(row["brand"])
            cat_name = str(row["category"])
            p_price = int(row["price_inr"])
            p_rating = float(row["rating"])
            score = float(row["match_score"])
            
            raw_url = str(row.get("url", "")).strip()
            if not raw_url or raw_url.lower() == "nan":
                import urllib.parse
                raw_url = f"https://www.amazon.in/s?k={urllib.parse.quote_plus(str(row['product_name']))}"

            if query_text and query_text.strip():
                explanation = f"Matches '{query_text.strip()}' by Indian brand {brand_name} in {cat_name} (₹{p_price:,}, {p_rating}★)."
            else:
                explanation = f"Top-rated {cat_name} product from Indian brand {brand_name} at ₹{p_price:,} ({p_rating}★ customer rating)."

            results.append({
                "id": int(row["product_id"]),
                "name": str(row["product_name"]),
                "category": cat_name,
                "brand": brand_name,
                "price_inr": p_price,
                "rating": p_rating,
                "description": str(row["description"]),
                "features": str(row.get("features", "")),
                "url": raw_url,
                "match_score": score,
                "explanation": explanation
            })

        return results


if __name__ == "__main__":
    recommender = ProductRecommender()
    print("=== Testing Indian Brand Audio Products ===")
    for rec in recommender.recommend(category="Audio", max_price_inr=3000, query_text="ANC wireless earbuds", top_n=2):
        print(f"[{rec['match_score']}%] {rec['name']} | Rs. {rec['price_inr']} | {rec['brand']}")

    print("\n=== Testing Gaming Gear ===")
    for rec in recommender.recommend(category="Gaming", top_n=2):
        print(f"[{rec['match_score']}%] {rec['name']} | Rs. {rec['price_inr']} | {rec['brand']}")

