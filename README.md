# RECOM.ai — Multi-Domain Recommendation Portal ⚡

> An AI-powered, multi-domain recommendation system that delivers **personalized suggestions** across Movies, Products, and Courses — with explainable hybrid scoring, user authentication, and real-time benchmarking.

---

## ✨ Features at a Glance

| Domain | Highlights |
|:---|:---|
| **🎬 Movies & Cinema** | 4 industries — Bollywood, Tollywood, Hollywood & Nepali Cinema. Multi-genre filtering, TF-IDF plot search, and tunable hybrid scoring (Content vs. Rating). |
| **🛍️ Indian Brands** | 9 categories — Audio, Wearables, Gaming, Smart Home, Watches, Fragrance & more. 20+ Indian brands with prices in **INR ₹** and budget sliders. |
| **🎓 Courses & Skills** | 6 domains — AI, Data Science, Cloud, Cybersecurity, Business & Software Engineering. Skill-interest matching with difficulty filtering. |
| **📊 Model Benchmarks** | 80/20 holdout evaluation comparing 4 algorithms: Popularity Baseline, Content-Based TF-IDF, Collaborative Filtering (SVD), and Hybrid Model. |
| **🔖 Saved Items** | Bookmark any recommendation. Click a saved item to jump directly to its tab. Remove items with a single click. |
| **👤 Authentication** | SQLite3-backed registration, login, and demo access. Sessions always start on the Overview page. |
| **💡 Explainable AI** | Every recommendation card shows a *"Why Recommended"* explanation based on feature similarity and rating. |

---

## 🏛️ Architecture

```
Recommendation-System/
│
├── app.py                            # Streamlit web portal (main entry point)
├── database.py                       # SQLite3 — auth, bookmarks, feedback
├── evaluation.py                     # Precision@K, Recall@K, RMSE benchmarks
│
├── models/                           # Recommendation engines
│   ├── __init__.py                   # Unified exports
│   ├── movie_rec.py                  # Movie engine (TF-IDF + hybrid scoring)
│   ├── product_rec.py                # Product engine (Indian brands, INR ₹)
│   └── course_rec.py                 # Course engine (skill-interest matching)
│
├── components/                       # Custom Streamlit components
│   ├── __init__.py                   # Component loader
│   └── habit_auth/                   # Authentication UI component
│       └── index.html                # Custom HTML/JS auth form
│
├── data/
│   ├── raw/                          # Raw source datasets
│   │   └── ml-latest-small/          # MovieLens dataset
│   └── cleaned/                      # Preprocessed CSV files
│       ├── movies_clean.csv          # 9,798 movies (Bollywood, Tollywood, Hollywood, Nepali)
│       ├── movie_ratings_clean.csv   # 100,836 ratings (MovieLens)
│       ├── products_clean.csv        # 41 Indian brand products
│       ├── product_ratings_clean.csv # 628 product ratings
│       ├── courses_clean.csv         # 13 curated courses
│       └── course_ratings_clean.csv  # 458 course ratings
│
├── assets/
│   └── login_cards/                  # Login page showcase images
│
├── tests/
│   └── test_all.py                   # Comprehensive test suite (72 tests)
│
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore rules
├── ARCHITECTURE.md                   # Detailed system architecture & ER diagrams
├── DESIGN.md                         # UI design specification & visual tokens
└── README.md                         # This file
```

---

## ⚡ Quick Start

### Option A: Run in GitHub Codespaces (One-Click)

Click the button below to open this project directly in a cloud environment where all dependencies are pre-installed:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/suraz111/AI-Lab-project--Recommendation-System-)

Once the Codespace loads, run:
```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

---

### Option B: Local Setup

#### Prerequisites
- **Python 3.9+** (tested on Python 3.11 & 3.14)
- **pip** (Python package manager)

#### 1. Clone the Repository
```bash
git clone https://github.com/suraz111/AI-Lab-project--Recommendation-System-.git
cd AI-Lab-project--Recommendation-System-
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

### 4. Run Tests (Optional)

```bash
python tests/test_all.py
```

Expected output: **72/72 tests passed**.

---

## 🔑 How to Use

1. **Login / Sign Up** — Create an account or click **Demo Access** to explore instantly.
2. **Overview** — Browse spotlight recommendations across all domains.
3. **Navigate Tabs** — Switch between Movies, Products, Courses, and Model Benchmarks.
4. **Filter & Search** — Use genre filters, budget sliders, skill inputs, and text search.
5. **Tune Alpha (α)** — Slide between content-based matching (α → 1.0) and popularity-based ranking (α → 0.0).
6. **Save & Bookmark** — Click 🔖 to save any recommendation to your sidebar.
7. **Jump to Saved** — Click any saved item in the sidebar to navigate directly to its tab.

---

## 📐 How the Algorithm Works

Each recommender uses a **Hybrid Scoring Model** that blends content similarity with community ratings:

```
ContentScore(i, q)  = CosineSimilarity(TF-IDF(query), TF-IDF(item))
RatingScore(i)      = item_rating / 5.0
HybridScore(i)      = α × ContentScore + (1 - α) × RatingScore
MatchPercentage(i)  = Round(HybridScore × 100, 1)
```

| Parameter | Description |
|:---|:---|
| **α = 1.0** | Pure content-based matching (genre, keywords, features) |
| **α = 0.0** | Pure popularity-based ranking (community ratings) |
| **α = 0.6** | Default — balanced hybrid (60% content, 40% ratings) |

---

## 📊 Evaluation Results

Benchmarked on **MovieLens Latest Small** (610 users, 100,836 ratings) with 80/20 per-user holdout:

| Algorithm | Precision@5 | Recall@5 | RMSE |
|:---|:---:|:---:|:---:|
| Popularity Baseline | 0.120 | 0.090 | 1.052 |
| Content-Based (TF-IDF) | 0.285 | 0.210 | 0.940 |
| Collaborative Filtering (SVD) | 0.340 | 0.290 | 0.880 |
| **Hybrid Model (RECOM.ai)** | **0.415** | **0.365** | **0.842** |

---

## 🛠️ Tech Stack

| Layer | Technology |
|:---|:---|
| **Frontend** | Streamlit, Custom HTML/CSS Components |
| **ML Engine** | Scikit-Learn (TF-IDF, Cosine Similarity) |
| **Data** | Pandas, NumPy |
| **Database** | SQLite3 (user auth, bookmarks, feedback) |
| **Language** | Python 3.9+ |

---

## 📄 License

This project is built for academic and educational purposes.

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
