import os
import sys
import re
import urllib.request
import urllib.parse
import json
import time
from PIL import Image
import io
import pandas as pd

def search_wiki_poster_url(title_str):
    """Searches Wikipedia API for the official movie theatrical poster."""
    clean_t = re.sub(r'\s*\(\d{4}\)', '', title_str).strip()
    year_match = re.search(r'\((\d{4})\)', title_str)
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
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                results = data.get("query", {}).get("search", [])
                if not results:
                    continue
                
                # Try the results to find a page with a poster/image
                for r in results:
                    page_title = r["title"]
                    p_enc = urllib.parse.quote(page_title.replace(" ", "_"))
                    summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{p_enc}"
                    req2 = urllib.request.Request(summary_url, headers={"User-Agent": "RecomAI-PosterFetcher/2.0 (contact@recom.ai)"})
                    try:
                        with urllib.request.urlopen(req2, timeout=5) as resp2:
                            d = json.loads(resp2.read().decode())
                            img_url = d.get("originalimage", {}).get("source") or d.get("thumbnail", {}).get("source")
                            if img_url and ("poster" in img_url.lower() or "film" in page_title.lower() or not any(x in img_url.lower() for x in ["flag", "logo", "icon"])):
                                return img_url
                    except Exception:
                        continue
        except Exception as e:
            continue
    return None

def download_image_to_jpeg(url, target_path):
    """Downloads an image from URL, converts to clean RGB JPEG, and saves to target_path."""
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "RecomAI-PosterFetcher/2.0 (contact@recom.ai)"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read()
                img = Image.open(io.BytesIO(content))
                img = img.convert("RGB")
                # Resize if overly huge (max 600 width, maintain aspect ratio)
                w, h = img.size
                if w > 600:
                    new_h = int(h * (600 / w))
                    img = img.resize((600, new_h), Image.Resampling.LANCZOS)
                img.save(target_path, "JPEG", quality=90)
                return True
        except Exception as e:
            if attempt < 2:
                time.sleep(1.5 * (attempt + 1))
            else:
                print(f"Failed to download {url}: {e}")
                return False
    return False

def main():
    movies_csv = "data/cleaned/movies_clean.csv"
    posters_dir = "assets/posters"
    os.makedirs(posters_dir, exist_ok=True)

    df = pd.read_csv(movies_csv)
    existing_ids = set(f.split(".")[0] for f in os.listdir(posters_dir) if f.endswith((".jpg", ".jpeg", ".png", ".webp")))

    # 1. Target all regional movies (Bollywood, Tollywood, Nepali) missing posters
    regional_missing = df[
        (df["industry"].isin(["Bollywood", "Tollywood", "Nepali Cinema"])) &
        (~df["movieId"].astype(str).isin(existing_ids))
    ]

    # 2. Target top modern Hollywood movies missing posters
    top_hollywood = df[df["industry"] == "Hollywood"].sort_values(by=["rating_count", "avg_rating"], ascending=[False, False]).head(50)
    hollywood_missing = top_hollywood[~top_hollywood["movieId"].astype(str).isin(existing_ids)]

    target_movies = pd.concat([regional_missing, hollywood_missing]).drop_duplicates(subset=["movieId"])
    print(f"Total target movies to download official posters for: {len(target_movies)}")

    success_count = 0
    for idx, row in target_movies.iterrows():
        mid = str(row["movieId"])
        title = str(row["title"])
        industry = str(row.get("industry", "Cinema"))
        target_file = os.path.join(posters_dir, f"{mid}.jpg")

        print(f"[{industry}] {mid}: Searching poster for '{title}'...")
        img_url = search_wiki_poster_url(title)
        if img_url:
            ok = download_image_to_jpeg(img_url, target_file)
            if ok:
                print(f"  --> SUCCESS: Saved {mid}.jpg ({os.path.getsize(target_file)} bytes)")
                success_count += 1
            else:
                print(f"  --> FAILED to download image from {img_url}")
        else:
            print(f"  --> No Wikipedia poster found for '{title}'")
        time.sleep(0.3)

    print(f"\nCompleted! Successfully downloaded {success_count}/{len(target_movies)} official posters.")

if __name__ == "__main__":
    main()
