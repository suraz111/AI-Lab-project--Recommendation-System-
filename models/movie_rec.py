"""
Movie Recommendation Engine (RECOM.ai)
Supports multi-industry filtering (Bollywood, Tollywood, Hollywood, Nepali Cinema),
genre matching, TF-IDF plot search, and hybrid rating-weighted ranking.
"""

import os
import base64
import urllib.parse
import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_POSTER_CACHE = {}


def generate_svg_poster(title: str, industry: str = "Cinema", rating: float = 4.5) -> str:
    """Generates an elegant Velvet & Brass vector poster for movies lacking external artwork."""
    clean_title = re.sub(r'\s*\(\d{4}\)', '', title).strip()
    year_match = re.search(r'\((\d{4})\)', title)
    year_str = year_match.group(1) if year_match else "CLASSIC"

    # Wrap title if long
    words = clean_title.split()
    lines = []
    curr = []
    for w in words:
        if sum(len(x) for x in curr) + len(w) > 13 and curr:
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
        title_spans.append(f'<tspan x="150" y="{y_start + i * 26}">{safe_line.upper()}</tspan>')
    title_svg = "".join(title_spans)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 450" width="100%" height="100%">
  <defs>
    <linearGradient id="velvet" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#6B0F24" />
      <stop offset="50%" stop-color="#4A0817" />
      <stop offset="100%" stop-color="#24030A" />
    </linearGradient>
    <linearGradient id="brass" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#E5C07B" />
      <stop offset="50%" stop-color="#C5A059" />
      <stop offset="100%" stop-color="#8C6D2D" />
    </linearGradient>
  </defs>
  <rect width="300" height="450" fill="url(#velvet)" />
  <rect x="8" y="8" width="284" height="434" fill="none" stroke="url(#brass)" stroke-width="2.5" />
  <rect x="14" y="14" width="272" height="422" fill="none" stroke="#1A050B" stroke-width="1" opacity="0.6" />
  
  <rect x="25" y="24" width="250" height="26" fill="#1A050B" stroke="url(#brass)" stroke-width="1" />
  <text x="150" y="41" text-anchor="middle" fill="#E5C07B" font-family="'Space Grotesk', sans-serif" font-size="10" font-weight="900" letter-spacing="2">{industry.upper()} &bull; {year_str}</text>

  <circle cx="150" cy="120" r="42" fill="#1A050B" stroke="url(#brass)" stroke-width="2" />
  <text x="150" y="135" text-anchor="middle" font-size="34">🎬</text>

  <text text-anchor="middle" fill="#FAF5E8" font-family="'Space Grotesk', sans-serif" font-size="18" font-weight="900" letter-spacing="1">
    {title_svg}
  </text>
  
  <rect x="75" y="315" width="150" height="28" fill="#C5A059" stroke="#1A050B" stroke-width="1.5" />
  <text x="150" y="333" text-anchor="middle" fill="#1A050B" font-family="'Space Grotesk', sans-serif" font-size="12" font-weight="900">★ {rating:.1f} / 5.0</text>
  
  <text x="150" y="415" text-anchor="middle" fill="#C5A059" font-family="'Space Grotesk', sans-serif" font-size="9" font-weight="800" letter-spacing="3">RECOM.AI THEATRE</text>
</svg>'''
    b64_svg = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    return f"data:image/svg+xml;base64,{b64_svg}"


def _download_wiki_movie_poster(title: str, target_path: str) -> bool:
    """Downloads official movie theatrical poster from Wikipedia API and caches as clean JPEG."""
    import urllib.request
    import urllib.parse
    import json
    from PIL import Image
    import io

    clean_t = re.sub(r'\s*\(\d{4}\)', '', str(title)).strip()
    year_match = re.search(r'\((\d{4})\)', str(title))
    year = year_match.group(1) if year_match else ""

    queries = [
        f"{clean_t} {year} film" if year else f"{clean_t} film",
        f"{clean_t} film",
        f"{clean_t}"
    ]

    for q in queries:
        try:
            q_enc = urllib.parse.quote_plus(q)
            s_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={q_enc}&utf8=&format=json&srlimit=2"
            req = urllib.request.Request(s_url, headers={"User-Agent": "RecomAI-PosterFetcher/2.0 (contact@recom.ai)"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode())
                results = data.get("query", {}).get("search", [])
                if not results:
                    continue
                for r in results:
                    page_title = r["title"]
                    p_enc = urllib.parse.quote(page_title.replace(" ", "_"))
                    summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{p_enc}"
                    req2 = urllib.request.Request(summary_url, headers={"User-Agent": "RecomAI-PosterFetcher/2.0 (contact@recom.ai)"})
                    try:
                        with urllib.request.urlopen(req2, timeout=4) as resp2:
                            d = json.loads(resp2.read().decode())
                            img_url = d.get("originalimage", {}).get("source") or d.get("thumbnail", {}).get("source")
                            if img_url and ("poster" in img_url.lower() or "film" in page_title.lower() or not any(x in img_url.lower() for x in ["flag", "logo", "icon"])):
                                img_req = urllib.request.Request(img_url, headers={"User-Agent": "RecomAI-PosterFetcher/2.0 (contact@recom.ai)"})
                                with urllib.request.urlopen(img_req, timeout=6) as img_resp:
                                    img_data = img_resp.read()
                                    im = Image.open(io.BytesIO(img_data)).convert("RGB")
                                    w, h = im.size
                                    if w > 600:
                                        im = im.resize((600, int(h * (600 / w))), Image.Resampling.LANCZOS)
                                    im.save(target_path, "JPEG", quality=90)
                                    return True
                    except Exception:
                        continue
        except Exception:
            continue
    return False


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

        # Merge with links dataset if available for IMDB IDs
        links_path = "data/raw/ml-latest-small/links.csv"
        if os.path.exists(links_path):
            try:
                links_df = pd.read_csv(links_path)
                self.movies_df = self.movies_df.merge(links_df[["movieId", "imdbId"]], on="movieId", how="left")
            except Exception:
                self.movies_df["imdbId"] = np.nan
        else:
            self.movies_df["imdbId"] = np.nan
            
        # Ensure default columns
        if "industry" not in self.movies_df.columns:
            self.movies_df["industry"] = "Hollywood"
            
        self.movies_df["content_features"] = self.movies_df["content_features"].fillna("")
        
        # Extract release year as integer column for temporal filtering & sorting
        self.movies_df["year"] = self.movies_df["title"].str.extract(r'\((\d{4})\)')[0].fillna(2000).astype(int)

        # Build TF-IDF vectorizer over content features
        self.tfidf = TfidfVectorizer(stop_words="english", max_features=5000)
        self.tfidf_matrix = self.tfidf.fit_transform(self.movies_df["content_features"])


    def get_poster(self, movie_id: int, title: str, industry: str, rating: float = 4.5, imdb_id=None):
        """Resolves local base64 poster, downloads missing poster from Wikipedia, or authentic theatrical fallback."""
        if movie_id in _POSTER_CACHE:
            cached = _POSTER_CACHE[movie_id]
            if isinstance(cached, tuple) and not str(cached[0]).startswith("data:image/svg"):
                return cached

        posters_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "posters"))

        # 1. Local disk cached poster
        for ext in [".jpg", ".jpeg", ".png", ".webp"]:
            local_path = os.path.join(posters_dir, f"{movie_id}{ext}")
            if os.path.exists(local_path) and os.path.getsize(local_path) > 100:
                try:
                    with open(local_path, "rb") as f:
                        b64 = base64.b64encode(f.read()).decode("utf-8")
                    mime = "image/png" if ext == ".png" else "image/jpeg"
                    url = f"data:{mime};base64,{b64}"
                    _POSTER_CACHE[movie_id] = (url, url)
                    return url, url
                except Exception:
                    pass

        # 2. Try on-demand download of the genuine Wikipedia poster
        clean_target = os.path.join(posters_dir, f"{movie_id}.jpg")
        try:
            if _download_wiki_movie_poster(title, clean_target):
                with open(clean_target, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode("utf-8")
                url = f"data:image/jpeg;base64,{b64}"
                _POSTER_CACHE[movie_id] = (url, url)
                return url, url
        except Exception:
            pass

        # 3. Fallback to an authentic photographic cinema poster from our verified library
        ind_str = str(industry or "").lower()
        if "bollywood" in ind_str or "hindi" in ind_str:
            fallback_id = "90055"  # 12th Fail
        elif "tollywood" in ind_str or "telugu" in ind_str or "tamil" in ind_str or "south" in ind_str:
            fallback_id = "100022"  # Kantara
        elif "nepal" in ind_str:
            fallback_id = "200021"  # Purna Bahadur Ko Sarangi
        else:
            fallback_id = "300001"  # Oppenheimer

        fb_path = os.path.join(posters_dir, f"{fallback_id}.jpg")
        if not os.path.exists(fb_path):
            fb_path = os.path.join(posters_dir, "2571.jpg")

        try:
            with open(fb_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            url = f"data:image/jpeg;base64,{b64}"
            _POSTER_CACHE[movie_id] = (url, url)
            return url, url
        except Exception:
            fallback = generate_svg_poster(title, industry, rating)
            _POSTER_CACHE[movie_id] = (fallback, fallback)
            return fallback, fallback

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
        alpha: float = 0.6,
        min_year: int = None,
        sort_by_year: bool = False
    ) -> list:
        """
        Generates Top-N movie recommendations with genre filtering and temporal intelligence.
        
        Parameters:
            selected_genres: List of genre strings to filter/match.
            industry: 'All', 'Bollywood', 'Tollywood', 'Hollywood', or 'Nepali Cinema'.
            query_text: Free-text search terms (e.g. 'space mission', 'dacoit revenge').
            top_n: Number of recommendations to return.
            alpha: Weight for Content Match [0.0 - 1.0], (1 - alpha) is Rating Weight.
            min_year: Minimum release year filter (e.g., 2015).
            sort_by_year: Whether to prioritize newer movies.
        """
        df = self.movies_df.copy()
        q_low = (query_text or "").lower()

        # Detect temporal desire from query if not explicitly passed
        is_new_query = bool(re.search(r'\b(new|latest|recent|current|modern|fresh|202[0-9]|201[8-9])\b', q_low))
        is_classic_query = bool(re.search(r'\b(classic|vintage|old|golden|90s|80s|70s)\b', q_low))
        if is_new_query and not sort_by_year:
            sort_by_year = True

        # Detect genre from free text query if not explicitly selected
        if not selected_genres and query_text:
            detected_genres = []
            genre_map = {
                "Comedy": ["comedy", "comedies", "funny", "hilarious", "humor"],
                "Action": ["action"],
                "Thriller": ["thriller", "suspense"],
                "Horror": ["horror", "scary", "spooky"],
                "Romance": ["romance", "romantic", "love"],
                "Sci-Fi": ["sci-fi", "science fiction", "scifi", "space"],
                "Crime": ["crime", "dacoit", "gangster", "heist", "mafia"],
                "Drama": ["drama"],
                "Adventure": ["adventure"],
                "Animation": ["animation", "animated", "anime"],
                "Mystery": ["mystery"],
                "Fantasy": ["fantasy"]
            }
            for g_name, kws in genre_map.items():
                if any(re.search(rf"\b{kw}\b", q_low) for kw in kws):
                    detected_genres.append(g_name)
            if detected_genres:
                selected_genres = detected_genres
        
        # 1. Filter by Industry
        if industry and industry.lower() != "all":
            df = df[df["industry"].str.lower() == industry.lower()]
            
        # 2. Filter by Genre if specified
        if selected_genres and len(selected_genres) > 0:
            genre_pattern = "|".join([g.strip() for g in selected_genres if g.strip()])
            matched_df = df[df["genres"].str.contains(genre_pattern, case=False, na=False)]
            if not matched_df.empty:
                df = matched_df
                
        # 3. Filter by Release Year if temporal constraints are active
        if min_year:
            year_sub = df[df["year"] >= min_year]
            if not year_sub.empty:
                df = year_sub
        elif is_new_query or sort_by_year:
            # Try filtering for recent movies (>= 2015); if too few, fall back to >= 2005
            recents = df[df["year"] >= 2015]
            if len(recents) >= top_n:
                df = recents
            else:
                recents_05 = df[df["year"] >= 2005]
                if len(recents_05) >= top_n:
                    df = recents_05
        elif is_classic_query:
            classics = df[df["year"] <= 2005]
            if not classics.empty:
                df = classics

        if df.empty:
            df = self.movies_df.copy()
        else:
            df = df.copy()

        # 4. Calculate Content Match Score via TF-IDF
        query_components = []
        if selected_genres:
            query_components.extend(selected_genres)
        if query_text and query_text.strip():
            # Clean stop words so they don't drown content features
            cleaned_q = re.sub(r'\b(new|latest|recent|good|best|top|movies?|films?|to|watch|in|from|please)\b', '', query_text, flags=re.I).strip()
            if cleaned_q:
                query_components.append(cleaned_q)
            
        full_query = " ".join(query_components).strip()
        
        if full_query:
            query_vector = self.tfidf.transform([full_query])
            sub_tfidf = self.tfidf.transform(df["content_features"].fillna(""))
            content_sim = cosine_similarity(query_vector, sub_tfidf).flatten()
        else:
            content_sim = np.ones(len(df)) * 0.5

        # 5. Rating Score Normalization (0.0 to 1.0) with Bayesian Weighted Rating
        max_rating = 5.0
        v = df["rating_count"].fillna(0)
        R = df["avg_rating"].fillna(3.5)
        m_thresh = 50.0
        C_mean = 3.5
        weighted_rating = (v / (v + m_thresh)) * R + (m_thresh / (v + m_thresh)) * C_mean
        rating_score = (weighted_rating / max_rating).values

        # 6. Hybrid Scoring Formula
        alpha_clamped = max(0.0, min(1.0, float(alpha)))
        hybrid_score = (alpha_clamped * content_sim) + ((1.0 - alpha_clamped) * rating_score)
        df["match_score"] = (hybrid_score * 100).round(1)

        # 7. Rank by temporal priority or hybrid score
        if sort_by_year or is_new_query:
            ranked_df = df.sort_values(by=["year", "avg_rating", "rating_count", "match_score"], ascending=[False, False, False, False]).head(top_n)
        else:
            ranked_df = df.sort_values(by=["match_score", "avg_rating", "rating_count"], ascending=[False, False, False]).head(top_n)

        # 8. Format output cards with explainability
        recommendations = []
        for _, row in ranked_df.iterrows():
            genres_list = [g.strip() for g in str(row["genres"]).split("|") if g.strip()]
            ind = str(row.get("industry", "Hollywood"))
            score = float(row["match_score"])
            avg_r = float(row["avg_rating"])
            r_count = int(row.get("rating_count", 0))
            yr = int(row.get("year", 2000))
            
            # Dynamic Explanation
            genre_desc = ", ".join(genres_list[:2]) if genres_list else "Popular"
            if is_new_query or sort_by_year:
                explanation = f"Recent {ind} release ({yr}) in {genre_desc} ({avg_r:.1f}/5 audience rating) matching your preferences."
            elif query_text and query_text.strip():
                clean_exp_q = re.sub(r'[\r\n]+', ' ', query_text.strip()[:60])
                explanation = f"Matches '{clean_exp_q}' in {ind} cinema with {genre_desc} elements & {avg_r:.1f}/5 rating."
            else:
                explanation = f"Top-rated {ind} film in {genre_desc} ({avg_r:.1f}/5 audience rating) matching your preferences."

            import urllib.parse
            m_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(str(row['title']) + ' movie watch online')}"

            poster_url, fallback_poster = self.get_poster(
                int(row["movieId"]),
                str(row["title"]),
                ind,
                avg_r,
                row.get("imdbId")
            )

            recommendations.append({
                "id": int(row["movieId"]),
                "title": str(row["title"]),
                "industry": ind,
                "genres": genres_list,
                "year": yr,
                "rating": avg_r,
                "rating_count": r_count,
                "url": m_url,
                "match_score": score,
                "explanation": explanation,
                "poster_url": poster_url,
                "fallback_poster": fallback_poster
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
