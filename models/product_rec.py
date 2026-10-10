"""
Product Recommendation Engine (RECOM.ai)
Specialized for Indian tech & lifestyle brands with pricing in INR (₹),
category filtering, budget constraints, and feature similarity ranking.
"""

import os
import base64
import urllib.parse
import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_IMAGE_CACHE = {}


def generate_svg_product_poster(name: str, brand: str, category: str, price_inr: int, rating: float = 4.5) -> str:
    """Generates a stylish modern vector product poster for products lacking local artwork."""
    clean_name = re.sub(r'\(.*?\)', '', name).strip()
    words = clean_name.split()
    lines = []
    curr = []
    for w in words:
        if sum(len(x) for x in curr) + len(w) > 14 and curr:
            lines.append(" ".join(curr))
            curr = [w]
        else:
            curr.append(w)
    if curr:
        lines.append(" ".join(curr))
    lines = lines[:3]

    title_spans = []
    y_start = 220 if len(lines) == 1 else (205 if len(lines) == 2 else 190)
    for i, line in enumerate(lines):
        safe_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        title_spans.append(f'<tspan x="150" y="{y_start + i * 24}">{safe_line.upper()}</tspan>')
    title_svg = "".join(title_spans)

    cat_icons = {
        "Audio": "🎧", "Wearables": "⌚", "Watches": "⌚",
        "Fragrance": "🌸", "Desk Setup": "🖥️", "Gaming": "🎮",
        "Smart Home": "💡", "Computer Accessories": "⌨️"
    }
    icon = cat_icons.get(category, "🛍️")

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 450" width="100%" height="100%">
  <defs>
    <linearGradient id="slate_grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B" />
      <stop offset="50%" stop-color="#0F172A" />
      <stop offset="100%" stop-color="#020617" />
    </linearGradient>
    <linearGradient id="teal_grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#14B8A6" />
      <stop offset="100%" stop-color="#0D9488" />
    </linearGradient>
  </defs>
  <rect width="300" height="450" fill="url(#slate_grad)" />
  <rect x="8" y="8" width="284" height="434" fill="none" stroke="url(#teal_grad)" stroke-width="2.5" />
  <rect x="14" y="14" width="272" height="422" fill="none" stroke="#000000" stroke-width="1" opacity="0.6" />
  
  <rect x="25" y="24" width="250" height="26" fill="#000000" stroke="url(#teal_grad)" stroke-width="1" />
  <text x="150" y="41" text-anchor="middle" fill="#2DD4BF" font-family="'Space Grotesk', sans-serif" font-size="10" font-weight="900" letter-spacing="2">{brand.upper()} &bull; {category.upper()}</text>

  <circle cx="150" cy="120" r="42" fill="#020617" stroke="url(#teal_grad)" stroke-width="2" />
  <text x="150" y="135" text-anchor="middle" font-size="34">{icon}</text>

  <text text-anchor="middle" fill="#F8FAFC" font-family="'Space Grotesk', sans-serif" font-size="16" font-weight="900" letter-spacing="1">
    {title_svg}
  </text>
  
  <rect x="60" y="305" width="180" height="30" fill="#0D9488" stroke="#000000" stroke-width="1.5" />
  <text x="150" y="325" text-anchor="middle" fill="#FFFFFF" font-family="'Space Grotesk', sans-serif" font-size="13" font-weight="900">₹{price_inr:,} &bull; ★ {rating:.1f}</text>
  
  <text x="150" y="415" text-anchor="middle" fill="#14B8A6" font-family="'Space Grotesk', sans-serif" font-size="9" font-weight="800" letter-spacing="3">RECOM.AI PRODUCTS</text>
</svg>'''
    b64_svg = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    return f"data:image/svg+xml;base64,{b64_svg}"


def get_product_poster(product_id: int, name: str, brand: str, category: str, price_inr: int = 1999, rating: float = 4.5) -> tuple:
    """Resolves local base64 product image or generated SVG fallback. Always returns self-contained Data URIs."""
    img_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "product_images"))
    img_file = os.path.join(img_dir, f"{product_id}.jpg")
    file_mtime = os.path.getmtime(img_file) if os.path.exists(img_file) else 0

    cache_entry = _IMAGE_CACHE.get(product_id)
    if cache_entry and cache_entry[2] == file_mtime:
        return cache_entry[0], cache_entry[1]

    fallback = generate_svg_product_poster(name, brand, category, price_inr, rating)

    # 1. Local disk cached image
    candidate_names = [f"{product_id}", f"p{product_id}"]
    for c_name in candidate_names:
        for ext in [".jpg", ".jpeg", ".png", ".webp"]:
            local_path = os.path.join(img_dir, f"{c_name}{ext}")
            if os.path.exists(local_path) and os.path.getsize(local_path) > 100:
                try:
                    with open(local_path, "rb") as f:
                        b64 = base64.b64encode(f.read()).decode("utf-8")
                    mime = "image/png" if ext == ".png" else "image/jpeg"
                    url = f"data:{mime};base64,{b64}"
                    _IMAGE_CACHE[product_id] = (url, fallback, file_mtime)
                    return url, fallback
                except Exception:
                    pass

    # 2. Instant vector SVG fallback poster
    _IMAGE_CACHE[product_id] = (fallback, fallback, file_mtime)
    return fallback, fallback


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

    @staticmethod
    def get_image(product_id: int, name: str, brand: str, category: str, price_inr: int = 1999, rating: float = 4.5) -> tuple:
        """Resolves local base64 product image or generated SVG fallback. Always returns self-contained Data URIs."""
        return get_product_poster(product_id, name, brand, category, price_inr, rating)

    def get_categories(self) -> list:
        """Returns sorted list of product categories."""
        return ["All"] + sorted(self.products_df["category"].dropna().unique().tolist())

    def get_brands(self) -> list:
        """Returns sorted list of brands in catalog."""
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
            p_id = int(row["product_id"])
            p_name = str(row["product_name"])
            
            raw_url = str(row.get("url", "")).strip()
            # If URL is missing, invalid, or an expired ASIN / generic brand homepage,
            # generate a verified live Amazon India product search link that displays the actual product
            if (
                not raw_url 
                or raw_url.lower() == "nan" 
                or "/dp/" in raw_url 
                or "boat-lifestyle" in raw_url 
                or "titan.co.in/shop" in raw_url 
                or "titan.co.in/collection" in raw_url
                or "skinn.in" in raw_url
                or "apple.com" in raw_url
                or "dior.com" in raw_url
                or "chanel.com" in raw_url
                or "philips-hue" in raw_url
                or not raw_url.startswith("http")
            ):
                import urllib.parse
                raw_url = f"https://www.amazon.in/s?k={urllib.parse.quote_plus(p_name)}"

            if query_text and query_text.strip():
                explanation = f"Matches '{query_text.strip()}' by {brand_name} in {cat_name} (₹{p_price:,}, {p_rating}★)."
            else:
                explanation = f"Top-rated {cat_name} product from {brand_name} at ₹{p_price:,} ({p_rating}★ customer rating)."

            img_url, fallback_img = self.get_image(
                product_id=p_id,
                name=p_name,
                brand=brand_name,
                category=cat_name,
                price_inr=p_price,
                rating=p_rating
            )

            results.append({
                "id": p_id,
                "name": p_name,
                "category": cat_name,
                "brand": brand_name,
                "price_inr": p_price,
                "rating": p_rating,
                "description": str(row["description"]),
                "features": str(row.get("features", "")),
                "url": raw_url,
                "match_score": score,
                "explanation": explanation,
                "image_url": img_url,
                "fallback_image": fallback_img
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

