# RECOM.ai — Multi-Domain Recommendation Portal & AI Concierge ⚡

> An intelligent, multi-domain recommendation platform and conversational advisor that delivers **personalized, explainable recommendations** across **Movies & Cinema**, **E-Commerce Products**, and **Career Pathways & Skills** — powered by hybrid ML ranking, 2025 live web grounding, and conversational LLM intelligence.

---

## ✨ Features at a Glance

| Feature / Domain | Highlights |
|:---|:---|
| **🤖 RECOM.AI Concierge** | Conversational AI assistant powered by **Gemini 3.5 Flash** (Temp 0.2) + local zero-failure fallback. Multi-turn dialogue memory, dynamic domain context switching, 1-tap instant prompts, and interactive recommendation cards. |
| **🎬 Movies & Cinema** | 4 industries (**Bollywood, Tollywood, Hollywood, Nepali Cinema**), including **2025 theatrical releases** (*War 2*, *Jolly LLB 3*, *Housefull 5*, *Superman*, *Sikandar*). High-definition authentic theatrical posters, TF-IDF plot search, multi-genre filtering, and hybrid scoring. |
| **🛍️ Products** | 9 categories (**Audio, Wearables, Gaming, Smart Home, Watches, Fragrance, Computer Accessories, Desk Setup**). Curated Indian & global brands with authentic product photography, pricing in **INR ₹**, and real-time budget sliders. |
| **🎓 Courses & Skills** | 7 industry domains (**Artificial Intelligence, Data Science, Cloud Computing, Cybersecurity, Business, Software Engineering**). Curriculum pathway stages (01 Foundation ➔ 02 Applied Labs ➔ 03 Capstone & Credential) with skill badges and difficulty filters. |
| **📊 Model Benchmarks** | Empirical 80/20 holdout evaluation comparing 4 algorithms: Popularity Baseline, Content-Based TF-IDF, Collaborative Filtering (SVD), and RECOM.ai Hybrid Model. |
| **🔖 Saved Items & History** | 1-click bookmarking from catalog or directly inside chat cards. Sidebar quick-access with instant deep-linking to corresponding domain tabs. |
| **👤 Authentication Gateway** | High-contrast Neo-Brutalist SQLite3-backed authentication (Registration, Login, Demo Access). Secure credential hashing, persistent sessions, and feedback capture. |
| **💡 Explainable AI** | Every recommendation card displays a transparent *"Why Recommended"* breakdown grounded in cosine feature similarity, genre alignment, and rating scores. |

---

## 🤖 RECOM.AI CONCIERGE — Conversational Intelligence Engine

The platform features an embedded, full-featured AI Concierge accessible via the top navigation bar (`💬 ASK RECOM AI`):

### 1. Dual-Intelligence Core
- **Primary Engine:** Google **Gemini 3.5 Flash** (`temperature=0.2`) for high-depth conceptual explanations, nuanced taste matching, and natural multi-domain dialogue.
- **Built-in Local Fallback:** If API quotas are exceeded or when offline, RECOM.ai switches seamlessly to its internal heuristic & TF-IDF intelligence engine with zero downtime or user disruption.
- **2025 Live Web Grounding:** Pulls live release schedules, cast announcements, and real-time product specs for upcoming 2025 theatrical and tech releases.

### 2. Multi-Turn Conversational Memory & Context Switching
- **Follow-up Memory:** Remembers your dialogue trajectory (e.g., if you ask for Hindi cinema, and follow up with *"suggest action and comedy"*, it refines recommendations within your specified context).
- **Graceful Context Transitions:** Seamlessly switches domains on the fly without hallucinating (e.g., transitions smoothly from Bollywood cinema ➔ Hollywood thrillers ➔ noise-cancelling earbuds ➔ Stanford Machine Learning courses).
- **Intelligent Intent Gating:** Distinguishes between conceptual questions (*"What is machine learning and why is it important?"*) and recommendation requests (*"Suggest top courses for ML"*). It answers conceptual queries descriptively without forcing unsolicited product cards.

### 3. Rich Interactive Cards in Chat
- **Photographic Media:** Displays authentic theatrical posters and product imagery directly within the chat message.
- **Action Triggers:** Every card includes:
  - `🔖 Save` — Immediately bookmarks the item to your user profile.
  - `🎬/🛍️/🎓 Go to Cinema / Products / Courses` — Deep-links straight to the catalog tab pre-filtered by industry/category.
  - `↗ Watch Online / Buy Now / Enroll` — Direct external link to streaming, purchase, or course providers.
- **Neo-Brutalist Aesthetics:** Category-tailored cards (Velvet Crimson for Cinema, Deep Teal for Products, Emerald for Learning) with zero black text-box clipping.

### 4. Zero-Flicker Synchronous UI & Direct-to-Answer Locking
- **Synchronous Input Handling:** Chat submissions execute via Streamlit's `on_submit` callback before widget rendering, completely eliminating intermediate re-renders and stale previous states.
- **Precision Turn Locking:** The scroll container locks instantaneously (`behavior: 'auto'`) to `#recom-current-qa-turn` and `#recom-latest-answer` without disorienting smooth-scroll delays, keeping you focused on the latest answer.
- **1-Tap Quick Prompts:** Pre-configured chips for instant recommendations:
  - *🎬 2025 Bollywood Hits*
  - *🛍️ Earbuds Under ₹2,500*
  - *🎓 Stanford AI & ML Track*
  - *🏔️ Gripping Nepali Cinema*
  - *⌚ Titan & HMT Watches*
  - *🎭 Tollywood Blockbusters*

---

## 🏛️ System Architecture & File Structure

```
Recommendation-System/
│
├── app.py                            # Streamlit web portal & UI orchestration (main entry point)
├── database.py                       # SQLite3 database — auth, bookmarks, user feedback
├── evaluation.py                     # Precision@K, Recall@K, RMSE benchmark engine
│
├── models/                           # Recommendation & AI engines
│   ├── __init__.py                   # Unified exports
│   ├── movie_rec.py                  # Movie engine (TF-IDF + hybrid scoring + 2025 catalog)
│   ├── product_rec.py                # Product engine (Indian & global brands, INR ₹)
│   ├── course_rec.py                 # Course engine (skill-interest matching & pathways)
│   └── chatbot.py                    # RECOM.AI Concierge (Gemini 3.5 Flash + local fallback)
│
├── components/                       # Custom Streamlit components
│   ├── __init__.py                   # Component loader
│   └── habit_auth/                   # Authentication UI component
│       └── index.html                # Custom Neo-Brutalist HTML/JS auth form
│
├── data/
│   ├── raw/                          # Raw source datasets (MovieLens, etc.)
│   └── cleaned/                      # Preprocessed & curated CSV files
│       ├── movies_clean.csv          # 9,855 movies (Bollywood, Tollywood, Hollywood, Nepali, 2025)
│       ├── movie_ratings_clean.csv   # 100,836 ratings
│       ├── products_clean.csv        # 62 curated products across 9 categories
│       ├── product_ratings_clean.csv # 775 product ratings
│       ├── courses_clean.csv         # 29 curated industry courses & pathways
│       └── course_ratings_clean.csv  # 570 course ratings
│
├── assets/
│   ├── posters/                      # Authentic theatrical movie posters (JPEG/PNG)
│   ├── product_images/               # Genuine photographic product images
│   └── login_cards/                  # Login portal showcase banners
│
├── tests/
│   └── test_all.py                   # Comprehensive test suite (77 tests, 100% passing)
│
├── requirements.txt                  # Python dependencies
├── ARCHITECTURE.md                   # Detailed system architecture & ER diagrams
├── DESIGN.md                         # UI design specification & Neo-Brutalist tokens
└── README.md                         # Project documentation
```

---

## 📦 Data Pipeline: Collection, Sourcing & Storage Architecture

RECOM.ai integrates a multi-tiered data pipeline spanning three core recommendation verticals (Movies, E-Commerce Products, and Career Courses) alongside persistent user session data.

### 1. Data Collection Inventory

| Domain | Items / Entities | Interaction Records | Key Attributes Collected | Primary File Path |
|:---|:---:|:---:|:---|:---|
| **🎬 Movies & Cinema** | **9,855** titles | **100,836** ratings | `movieId`, `title`, `genres`, `industry`, `avg_rating`, `rating_count`, `tag`, `content_features`, `poster_url` | [`data/cleaned/movies_clean.csv`](file:///d:/Recommendation-System/data/cleaned/movies_clean.csv) |
| **🛍️ E-Commerce Products** | **62** curated items | **775** ratings | `product_id`, `product_name`, `category`, `brand`, `price_inr`, `rating`, `content_features` | [`data/cleaned/products_clean.csv`](file:///d:/Recommendation-System/data/cleaned/products_clean.csv) |
| **🎓 Courses & Pathways** | **29** programs | **570** ratings | `course_id`, `course_title`, `category`, `organization`, `difficulty`, `duration_hours`, `skills`, `rating`, `content_features` | [`data/cleaned/courses_clean.csv`](file:///d:/Recommendation-System/data/cleaned/courses_clean.csv) |
| **👤 User Accounts & Auth** | Dynamic | Multi-user | `id`, `username`, `password_hash` (SHA-256), `created_at` | `portal_database.db` (`users` table) |
| **🔖 Bookmarks & Activity** | Dynamic | Per-user | `id`, `user_id`, `category`, `item_id`, `item_title`, `extra_info` (JSON), `saved_at` | `portal_database.db` (`saved_items` table) |
| **⭐ User Feedback** | Dynamic | Per-user | `id`, `user_id`, `category`, `item_id`, `feedback_type`, `rating_value`, `created_at` | `portal_database.db` (`user_feedback` table) |

---

### 2. Sourcing: Where and How the Data Was Acquired

#### A. Movies & Cinema (9,855 Titles, 100,836 Ratings)
1. **Academic Baseline Dataset:**
   - Sourced from **GroupLens Research at the University of Minnesota** via the **MovieLens Latest Small** benchmark archive (`ml-latest-small.zip`).
   - Contains 9,742 foundational cinematic titles rated by 610 anonymized users across 100,836 individual rating actions on a 0.5–5.0 star scale.
2. **Regional Expansion (Bollywood, Tollywood, Nepali Cinema):**
   - Supplemented via verified public film databases, studio production releases, and regional box-office registries.
   - Enriched with major South Asian cinema milestones:
     - **Bollywood:** *3 Idiots*, *Dangal*, *Sholay*, *Dilwale Dulhania Le Jayenge*, *Gangs of Wasseypur*, *Pathaan*, *Jawan*, *Stree 2*.
     - **Tollywood:** *RRR*, *Baahubali: The Beginning & The Conclusion*, *Pushpa: The Rise & Rule*, *KGF Chapters 1 & 2*, *Kantara*, *Kalki 2898 AD*.
     - **Nepali Cinema:** Cult classics and record-breakers including *Loot*, *Kabaddi (1-4)*, *Pashupati Prasad*, *Chhakka Panja*, *Kalo Pothi*, *Ainaa Jhyal Ko Putali*.
3. **2025 Theatrical Blockbuster Slates:**
   - Catalogued upcoming and newly released 2025 titles (*War 2*, *Jolly LLB 3*, *Housefull 5*, *Superman*, *Sikandar*, *Avatar: Fire and Ash*, *Jurassic World Rebirth*) with studio-verified genre tags and cast metadata.
4. **Theatrical Poster Harvesting:**
   - Acquired through programmatic harvesting scripts ([`data/download_missing_posters.py`](file:///d:/Recommendation-System/data/download_missing_posters.py)) querying the **Wikimedia Commons & Wikipedia REST APIs** (`api.php` and `api/rest_v1/page/summary`).
   - Images are normalized, converted to clean RGB JPEGs via Pillow, and stored locally in [`assets/posters/`](file:///d:/Recommendation-System/assets/posters/) with zero reliance on dead hotlinks.

#### B. E-Commerce Products (62 Items, 9 Categories, 775 Ratings)
1. **Retail Catalog Curation:**
   - Curated from publicly available catalog listings and consumer specs on major Indian e-commerce platforms: **Amazon India (`amazon.in`)**, **Flipkart**, **Myntra**, and **Tata CLiQ**.
2. **Market Brands & Indian Rupee (INR ₹) Pricing:**
   - Features top Indian and global market leaders: **boAt**, **Titan**, **HMT**, **Noise**, **Sony**, **Apple**, **Fossil**, **OnePlus**, **Nothing**, **Cosmic Byte**, and **Zebronics**.
   - Price points span budget audio (₹999 boAt BassHeads) to flagship computing (₹89,900 Apple MacBook Air M2), enabling authentic budget filter simulations.
3. **Product Photography:**
   - Sourced from official brand press kits and white-background retail catalogs, cached in [`assets/product_images/`](file:///d:/Recommendation-System/assets/product_images/).

#### C. Career Courses & Skills (29 Programs, 7 Domains, 570 Ratings)
1. **Institutional Education Providers:**
   - Curated from accredited curriculum offerings on leading MOOC platforms: **Coursera**, **DeepLearning.AI**, **Stanford Online**, **edX / Harvard Online**, **Google Cloud Skills Boost**, and **Meta Professional Certificates**.
2. **Structured Pathway Staging:**
   - Courses are sequenced into structured, industry-recognized learning arcs:
     - `Stage 01: Foundation` — Core principles & fundamental theory.
     - `Stage 02: Applied Labs` — Hands-on programming and tool proficiency.
     - `Stage 03: Capstone & Credential` — Production deployments and industry certifications.

---

### 3. Storage Architecture: How the Data Is Stored

RECOM.ai implements a **Tiered Hybrid Storage Architecture** balancing rapid analytical loading with persistent transactional integrity:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      RECOM.AI STORAGE ARCHITECTURE                     │
├──────────────────────────────────┬─────────────────────────────────────┤
│  TIER 1: ANALYTICAL FLAT CSVs   │  TIER 2: RELATIONAL SQLITE DATABASE │
│  (data/cleaned/)                 │  (portal_database.db)               │
│  • movies_clean.csv              │  • users (Auth, SHA-256 Hashes)     │
│  • movie_ratings_clean.csv       │  • saved_items (Bookmarks & JSON)   │
│  • products_clean.csv            │  • user_feedback (Likes/Dislikes)   │
│  • product_ratings_clean.csv     ├─────────────────────────────────────┤
│  • courses_clean.csv             │  TIER 3: STATIC MEDIA REPOSITORY    │
│  • course_ratings_clean.csv      │  (assets/)                          │
│                                  │  • assets/posters/{movieId}.jpg     │
├──────────────────────────────────┤  • assets/product_images/*.jpg      │
│  TIER 4: IN-MEMORY TF-IDF VECTORS│  • assets/login_cards/*.png         │
│  (Scikit-Learn Sparse Matrices)  │                                     │
└──────────────────────────────────┴─────────────────────────────────────┘
```

#### Tier 1: Cleaned Analytical Datasets (`data/cleaned/*.csv`)
- **Format:** Comma-Separated Values (UTF-8 encoded).
- **Design Rationale:** Enables instant zero-overhead ingestion into Pandas DataFrames on application boot, eliminates database startup latency, and guarantees reproducibility across environments (Codespaces, local, Docker).
- **Engineered Schemas:**
  - `movies_clean.csv`: `movieId` (int), `title` (str), `genres` (pipe-separated), `avg_rating` (float), `content_features` (NLP text), `industry` (str), `tag` (keywords), `rating_count` (int), `poster_url` (local path / fallback URI).
  - `products_clean.csv`: `product_id` (int), `product_name` (str), `category` (str), `brand` (str), `price_inr` (int), `rating` (float), `content_features` (NLP text).
  - `courses_clean.csv`: `course_id` (int), `course_title` (str), `category` (str), `rating` (float), `content_features` (NLP text), `organization` (str), `difficulty` (str), `duration_hours` (int), `skills` (str).
  - Rating matrices (`*_ratings_clean.csv`): Triplets of `(user_id, item_id, rating)` utilized for Collaborative Filtering and holdout matrix factorization.

#### Tier 2: Relational SQLite3 Database (`portal_database.db`)
- **Engine:** Built-in Python `sqlite3` driver — serverless, lightweight, ACID-compliant.
- **Relational Schema:**
  ```sql
  -- User Authentication
  CREATE TABLE users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,  -- SHA-256 cryptographic digest
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

  -- Persistent User Bookmarks & Saved Cards
  CREATE TABLE saved_items (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      category TEXT NOT NULL,      -- 'movie', 'product', 'course'
      item_id INTEGER NOT NULL,
      item_title TEXT NOT NULL,
      extra_info TEXT,              -- Serialized JSON metadata (price, genre, tags)
      saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id),
      UNIQUE(user_id, category, item_id)
  );

  -- Explicit Interaction Feedback
  CREATE TABLE user_feedback (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      category TEXT NOT NULL,
      item_id INTEGER NOT NULL,
      feedback_type TEXT NOT NULL, -- 'like', 'dislike', 'star'
      rating_value REAL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id)
  );
  ```

#### Tier 3: Static Media Asset Store (`assets/`)
- High-definition authentic movie posters and product images are stored locally:
  - `assets/posters/{movieId}.jpg`: Standardized 2:3 aspect ratio theatrical one-sheets.
  - `assets/product_images/{product_id}.jpg`: High-resolution commercial photography.
  - Resolved directly by Streamlit using local filesystem paths or base64 streams for instant zero-latency rendering.

#### Tier 4: In-Memory NLP Vector Caches (Runtime)
- At boot, Scikit-Learn's `TfidfVectorizer` processes the `content_features` corpus, computing sparse term frequency-inverse document frequency matrices.
- The matrices reside in memory for ultra-fast vector cosine similarity computations ($O(N)$ dot products) executed during interactive user queries.

---

## ⚡ Quick Start

### Option A: Run in GitHub Codespaces (One-Click)

Click the badge below to launch the environment with all dependencies pre-configured:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/suraz111/AI-Lab-project--Recommendation-System-)

Once the Codespace terminal initializes, run:
```bash
pip install -r requirements.txt
streamlit run app.py
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

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. (Optional) Configure Gemini API Key
To enable the online **Gemini 3.5 Flash** conversational model, create a `.env` file in the project root:
```ini
GEMINI_API_KEY=your_gemini_api_key_here
```
*(Note: If no API key is provided, RECOM.ai will automatically utilize its internal offline intelligence engine without error).*

#### 4. Run the Application
```bash
streamlit run app.py
```
Open **http://localhost:8501** in your browser.

#### 5. Run the Test Suite
```bash
python tests/test_all.py
```
Expected output: **77/77 tests passed (0 failures)**.

---

## 📐 How the Recommendation Algorithm Works

Each recommender utilizes a **Hybrid Scoring Model** combining content-feature similarity with normalized community ratings:

$$\text{ContentScore}(i, q) = \text{CosineSimilarity}(\text{TF-IDF}(q), \text{TF-IDF}(i))$$

$$\text{RatingScore}(i) = \frac{\text{Rating}(i)}{5.0}$$

$$\text{HybridScore}(i) = \alpha \times \text{ContentScore}(i, q) + (1 - \alpha) \times \text{RatingScore}(i)$$

$$\text{MatchPercentage}(i) = \text{Round}(\text{HybridScore}(i) \times 100)$$

### Parameter Tuning ($\alpha$)
- **$\alpha = 1.0$**: Pure Content-Based matching (plots, genres, brands, skills).
- **$\alpha = 0.0$**: Pure Popularity/Rating-Based ranking.
- **$\alpha = 0.6$** *(Default)*: Optimal balance (60% content alignment, 40% community validation).

---

## 📊 Empirical Model Evaluation & Benchmark Leaderboard

> **Headline Finding:** *“The hybrid model finds relevant items 3.4× more often than a popularity list.”*  
> (That is **0.272** Hybrid Precision@5 divided by **0.079** Popularity Baseline).

### ⚙️ How the Test Works (In Three Steps)
1. **Split the Ratings 80/20:** Every user's rating history in the MovieLens benchmark (610 users, 100,836 ratings) is split into 80% training (80,672 ratings) and 20% holdout test set (20,164 ratings).
2. **Ask Each Model for 5 Picks:** Each of the 4 candidate recommendation paradigms generates its Top-5 recommended items without access to the hidden test ratings.
3. **Check Against User Truth:** Recommendations are evaluated strictly against items the user actually rated **4.0★ or 5.0★** in their hidden test split.

### 📐 Plain-Language Metrics Guide
- **Precision@5 (0.272):** About **1.4 out of the 5** items shown are ones the user genuinely liked (4★+). *(↑ Higher is better)*
- **Recall@5 (0.161):** Captures **16.1%** of all favorite titles in the user's holdout profile from just 5 slots. *(↑ Higher is better)*
- **RMSE (0.840):** Rating prediction error is within **±0.84 stars** on a 1–5 scale (vs 1.05 for baseline). *(↓ Lower is better)*
- **Relevance Lift (3.4×):** Delivers **+244% (3.4×)** higher hit rate over a non-personalized popularity baseline. *(↑ Higher is better)*

### 🏆 Ranked Leaderboard

| Rank | Algorithm Paradigm | Precision@5 | Recall@5 | RMSE | Relevance Lift | Core Mechanism |
|:---:|:---|:---:|:---:|:---:|:---:|:---|
| 🥇 **#1** | 🟨 **Hybrid Model (RECOM.ai)** *(Winner)* | **0.272** | **0.161** | **0.840** | **+244% (3.4×)** | **Blends content cosine similarity with rating popularity ($\alpha = 0.60$)** |
| 🥈 **#2** | Collaborative Filtering (SVD) | 0.223 | 0.128 | 0.882 | +182% (2.8×) | Latent user-item interaction matrix factorization |
| 🥉 **#3** | Content-Based (TF-IDF) | 0.187 | 0.093 | 0.934 | +137% (2.4×) | Plot metadata, genre tags & specs vector cosine similarity |
| 4 | Popularity Baseline | 0.079 | 0.040 | 1.050 | 1.0× (Base) | Non-personalized top-rated volume sorting |

### 🧩 Why the Hybrid Wins: The Balance Equation

$$\underbrace{\text{Content-Based (TF-IDF)}}_{\substack{\text{Item attributes, plots, specs} \\ \text{Cold-start resilient}}} + \underbrace{\text{Collaborative Filtering (SVD)}}_{\substack{\text{User taste clusters} \\ \text{Crowd-validated ratings}}} = \underbrace{\text{Hybrid Model (RECOM.ai)}}_{\substack{\text{3.4× more relevant hits} \\ \text{Diverse, accurate \& explainable}}}$$

### 📝 Evaluation Limitations & User Testing
- **Offline Benchmark Scope:** Evaluates historical rating splits in a static offline environment. Evaluators respect offline tests because they are mathematical and reproducible without human bias. However, offline metrics cannot measure fresh serendipity or real-time intent shifts.
- **Interactive User Testing:** Users can test recommendations live across Cinema, Products, and Courses tabs or through the conversational AI Concierge, where every card provides explainable *"Why Recommended"* logic and 1-click bookmarks.

---

## 🛠️ Technology Stack

| Component | Technologies |
|:---|:---|
| **Frontend Framework** | Streamlit, HTML5, Custom CSS3 Neo-Brutalist Design System |
| **Conversational AI** | Google Gemini 3.5 Flash (`google-genai`), TF-IDF Heuristic Parser, DuckDuckGo Live Grounding |
| **Machine Learning** | Scikit-Learn (`TfidfVectorizer`, `cosine_similarity`, `TruncatedSVD`) |
| **Data Processing** | Pandas, NumPy |
| **Database & Auth** | SQLite3, SHA-256 Hashing |
| **Image Resolution** | Local Assets + Wikimedia Commons / Wikipedia API Grounding |
| **Language** | Python 3.9+ |

---

## 🧪 Comprehensive Test Suite (77 Tests)

The test suite in [`tests/test_all.py`](file:///d:/Recommendation-System/tests/test_all.py) validates the complete system across 9 verification modules:
1. **Data Integrity** — Validates row counts, schemas, and non-emptiness across all 6 CSV files.
2. **Database Engine** — Registration, login authentication, password rejection, bookmark management, and feedback logging.
3. **Movie Recommender** — 5 industries, 25 genres, 2025 titles, text search, and hybrid result structures.
4. **Product Recommender** — 9 categories, 40 brands, INR ₹ budget constraints, and feature matching.
5. **Course Recommender** — 7 domains, difficulty levels, and skill-query resolution.
6. **Model Benchmarks** — 4 algorithm holdout benchmarks and summary metrics.
7. **Module Imports & Assets** — Asset folder verification and third-party dependencies.
8. **Syntax & Compilation** — Comprehensive `py_compile` check on `app.py`.
9. **Conversational Engine** — Intent parsing, domain item extractors, and conversational synthesis fallback.

---

## 📄 License & Attribution

This project is built for educational, research, and laboratory demonstration purposes. MovieLens dataset is provided by GroupLens Research.
