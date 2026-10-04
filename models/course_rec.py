"""
Study & Career Course Recommendation Engine (RECOM.ai)
Specialized for skill-interest matching, domain targeting, difficulty filtering,
and credential discovery across top organizations (Google, Stanford, Meta, etc.).
"""

import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class CourseRecommender:
    def __init__(
        self,
        data_path: str = "data/cleaned/courses_clean.csv",
        ratings_path: str = "data/cleaned/course_ratings_clean.csv"
    ):
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Course dataset not found at {data_path}")

        self.courses_df = pd.read_csv(data_path)
        self.ratings_df = pd.read_csv(ratings_path) if os.path.exists(ratings_path) else pd.DataFrame()

        self.courses_df["content_features"] = self.courses_df["content_features"].fillna("")

        # Build TF-IDF vectorizer over content features (skills, description, category)
        self.tfidf = TfidfVectorizer(stop_words="english", max_features=3000)
        self.tfidf_matrix = self.tfidf.fit_transform(self.courses_df["content_features"])

    def get_categories(self) -> list:
        """Returns sorted list of course categories/domains."""
        return ["All"] + sorted(self.courses_df["category"].dropna().unique().tolist())

    def get_difficulty_levels(self) -> list:
        """Returns list of difficulty levels."""
        return ["All", "Beginner", "Intermediate", "Advanced"]

    def recommend(
        self,
        category: str = "All",
        difficulty: str = "All",
        desired_skills: str = "",
        top_n: int = 5,
        alpha: float = 0.7
    ) -> list:
        """
        Generates Top-N course recommendations based on target domain, level, and skills.
        
        Parameters:
            category: 'All' or specific domain (e.g. 'Artificial Intelligence', 'Data Science').
            difficulty: 'All', 'Beginner', 'Intermediate', or 'Advanced'.
            desired_skills: Free-text skills string (e.g. 'Python Machine Learning SQL').
            top_n: Number of recommendations to return.
            alpha: Weight for Skill & Content Match [0.0 - 1.0].
        """
        df = self.courses_df.copy()

        # 1. Filter by Domain/Category
        if category and category.lower() != "all":
            df = df[df["category"].str.lower() == category.lower()]

        # 2. Filter by Difficulty Level
        if difficulty and difficulty.lower() != "all":
            df = df[df["difficulty_level"].str.lower() == difficulty.lower()]

        if df.empty:
            df = self.courses_df.copy()

        # 3. Compute Skill Similarity via TF-IDF
        query_elements = []
        if category and category.lower() != "all":
            query_elements.append(category)
        if difficulty and difficulty.lower() != "all":
            query_elements.append(difficulty)
        if desired_skills and desired_skills.strip():
            query_elements.append(desired_skills.strip())

        full_query = " ".join(query_elements).strip()

        if full_query:
            query_vec = self.tfidf.transform([full_query])
            sub_tfidf = self.tfidf.transform(df["content_features"].fillna(""))
            skill_sim = cosine_similarity(query_vec, sub_tfidf).flatten()
        else:
            skill_sim = np.ones(len(df)) * 0.5

        # 4. Rating Normalization
        max_rating = 5.0
        rating_score = (df["rating"].fillna(4.5) / max_rating).values

        # 5. Hybrid Scoring Formula
        alpha_clamped = max(0.0, min(1.0, float(alpha)))
        hybrid_score = (alpha_clamped * skill_sim) + ((1.0 - alpha_clamped) * rating_score)
        df["match_score"] = (hybrid_score * 100).round(1)

        # 6. Rank by match score and rating
        ranked_df = df.sort_values(by=["match_score", "rating"], ascending=False).head(top_n)

        results = []
        for _, row in ranked_df.iterrows():
            skills_raw = str(row["skills"])
            skills_list = [s.strip() for s in skills_raw.split(",") if s.strip()]
            org = str(row["organization"])
            level = str(row["difficulty_level"])
            rating_val = float(row["rating"])
            hours = int(row["duration_hours"])
            score = float(row["match_score"])

            skill_highlights = ", ".join(skills_list[:3]) if skills_list else "Core Industry Skills"
            if desired_skills and desired_skills.strip():
                explanation = f"Curated by {org} ({level} level, {hours}h). Teaches target skills: {skill_highlights}."
            else:
                explanation = f"Highly rated {level} certification by {org} ({rating_val:.1f}/5 rating, {hours}h duration) covering {skill_highlights}."

            results.append({
                "id": int(row["course_id"]),
                "title": str(row["course_title"]),
                "organization": org,
                "category": str(row["category"]),
                "difficulty": level,
                "rating": rating_val,
                "duration_hours": hours,
                "skills": skills_list,
                "description": str(row["description"]),
                "url": str(row["url"]),
                "match_score": score,
                "explanation": explanation
            })

        return results


if __name__ == "__main__":
    recommender = CourseRecommender()
    print("=== Testing Course Recommender (AI / Python) ===")
    for rec in recommender.recommend(category="Artificial Intelligence", desired_skills="Python Machine Learning Neural Networks", top_n=2):
        print(f"[{rec['match_score']}%] {rec['title']} ({rec['organization']})")

    print("\n=== Testing Data Science ===")
    for rec in recommender.recommend(category="Data Science", top_n=2):
        print(f"[{rec['match_score']}%] {rec['title']} ({rec['organization']})")

