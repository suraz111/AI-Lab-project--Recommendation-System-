"""
Movie Recommendation Engine (RECOM.ai)
Supports multi-industry filtering (Bollywood, Tollywood, Hollywood, Nepali Cinema),
genre matching, TF-IDF plot search, and hybrid rating-weighted ranking.
"""

import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:
    def __init__(
        self,
        data_path: str = "data/cleaned/movies_clean.csv",
        ratings_path: str = "data/cleaned/movie_ratings_clean.csv"
    ):
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Movie dataset not found at {data_path}")
            
        self.movies_df = pd.read_csv(data_path)
        self.ratings_df = pd.read_csv(ratings_path) if os.path.exists(ratings_path) else pd.DataFrame()
        
        # Ensure default columns
        if "industry" not in self.movies_df.columns:
            self.movies_df["industry"] = "Hollywood"
            
        self.movies_df["content_features"] = self.movies_df["content_features"].fillna("")
        
        # Build TF-IDF vectorizer over content features
        self.tfidf = TfidfVectorizer(stop_words="english", max_features=5000)
        self.tfidf_matrix = self.tfidf.fit_transform(self.movies_df["content_features"])

    def get_industries(self) -> list:
        """Returns list of unique industries available in catalog."""
        return ["All"] + sorted(self.movies_df["industry"].dropna().unique().tolist())

    def get_genres(self) -> list:
        """Extracts all unique individual genres present in dataset."""
        unique_genres = set()
        for genres_str in self.movies_df["genres"].dropna():
            for g in str(genres_str).split("|"):
                cleaned = g.strip()
                if cleaned and cleaned != "(no genres listed)":
                    unique_genres.add(cleaned)
        return sorted(list(unique_genres))

    def recommend(
        self,
        selected_genres: list = None,
        industry: str = "All",
        query_text: str = "",
        top_n: int = 5,
        alpha: float = 0.6
    ) -> list:
        """
        Generates Top-N movie recommendations.
        
        Parameters:
            selected_genres: List of genre strings to filter/match.
            industry: 'All', 'Bollywood', 'Tollywood', 'Hollywood', or 'Nepali Cinema'.
            query_text: Free-text search terms (e.g. 'space mission', 'dacoit revenge').
            top_n: Number of recommendations to return.
            alpha: Weight for Content Match [0.0 - 1.0], (1 - alpha) is Rating Weight.
        """
        df = self.movies_df.copy()
        
        # 1. Filter by Industry
        if industry and industry.lower() != "all":
            df = df[df["industry"].str.lower() == industry.lower()]
            
        # 2. Filter by Genre if specified
        if selected_genres and len(selected_genres) > 0:
            genre_pattern = "|".join([g.strip() for g in selected_genres if g.strip()])
            matched_df = df[df["genres"].str.contains(genre_pattern, case=False, na=False)]
            # If strict filter produces matches, use them; otherwise keep full industry subset
            if not matched_df.empty:
                df = matched_df
                
        if df.empty:
            df = self.movies_df.copy()

        # 3. Calculate Content Match Score via TF-IDF
        query_components = []
        if industry and industry.lower() != "all":
            query_components.append(industry)
        if selected_genres:
            query_components.extend(selected_genres)
        if query_text and query_text.strip():
            query_components.append(query_text.strip())
            
        full_query = " ".join(query_components).strip()
        
        if full_query:
            query_vector = self.tfidf.transform([full_query])
            sub_tfidf = self.tfidf.transform(df["content_features"].fillna(""))
            content_sim = cosine_similarity(query_vector, sub_tfidf).flatten()
        else:
            content_sim = np.ones(len(df)) * 0.5

        # 4. Rating Score Normalization (0.0 to 1.0)
        max_rating = 5.0
        rating_score = (df["avg_rating"].fillna(3.5) / max_rating).values

        # 5. Hybrid Scoring Formula
        alpha_clamped = max(0.0, min(1.0, float(alpha)))
        hybrid_score = (alpha_clamped * content_sim) + ((1.0 - alpha_clamped) * rating_score)
        df["match_score"] = (hybrid_score * 100).round(1)

        # 6. Rank by match score and rating
        ranked_df = df.sort_values(by=["match_score", "avg_rating"], ascending=False).head(top_n)

        # 7. Format output cards with explainability
        recommendations = []
        for _, row in ranked_df.iterrows():
            genres_list = [g.strip() for g in str(row["genres"]).split("|") if g.strip()]
            ind = str(row.get("industry", "Hollywood"))
            score = float(row["match_score"])
            avg_r = float(row["avg_rating"])
            r_count = int(row.get("rating_count", 0))
            
            # Dynamic Explanation
            genre_desc = ", ".join(genres_list[:2]) if genres_list else "Popular"
            if query_text and query_text.strip():
                explanation = f"Matches '{query_text.strip()}' in {ind} cinema with {genre_desc} elements & {avg_r:.1f}/5 audience rating."
            else:
                explanation = f"Top-rated {ind} film in {genre_desc} ({avg_r:.1f}/5 audience rating) matching your preferences."

            import urllib.parse
            m_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(str(row['title']) + ' movie watch online')}"

            recommendations.append({
                "id": int(row["movieId"]),
                "title": str(row["title"]),
                "industry": ind,
                "genres": genres_list,
                "rating": avg_r,
                "rating_count": r_count,
                "url": m_url,
                "match_score": score,
                "explanation": explanation
            })

        return recommendations


if __name__ == "__main__":
    recommender = MovieRecommender()
    print("=== Testing Bollywood ===")
    for rec in recommender.recommend(industry="Bollywood", selected_genres=["Comedy"], top_n=2):
        print(f"[{rec['match_score']}%] {rec['title']} ({rec['industry']}) - {rec['explanation']}")

    print("\n=== Testing Tollywood ===")
    for rec in recommender.recommend(industry="Tollywood", selected_genres=["Action"], top_n=2):
        print(f"[{rec['match_score']}%] {rec['title']} ({rec['industry']}) - {rec['explanation']}")
