# DESIGN.md — RECOM.ai (Multi-Domain Recommendation Portal) 🔮

## 1. Executive Vision & Concept

**RECOM.ai** is a state-of-the-art, non-generic Multi-Domain Recommendation Portal. Unlike traditional basic recommendation demos, RECOM.ai delivers a unified, highly polished user interface with real-time explainable recommendations across three rich domains:

1. 🎬 **Movies (Cinema Hub):** Seamless switching between **Bollywood (Hindi)**, **Tollywood (Telugu)**, **Hollywood (English)**, and **Nepali Cinema** with plot keyword search and genre vector matching.
2. 🛍️ **Products E-Commerce & Lifestyle:** Next-gen product recommendations featuring top **lifestyle, horology & electronics brands** (*Titan, HMT, Fastrack, Sonata, Titan Skinn, Bella Vita Luxury, Bombay Shaving Company, The Man Company, Villain, Forest Essentials, Phool, boAt, Noise, Boult*) across audio, watches, fragrance, and gear priced in **INR (₹)**.
3. 🎓 **Study & Career Courses:** Skill-interest matching for top professional certificates (*Google, Stanford, Meta, IBM, Harvard*) across AI, Data Science, Software Engineering, Cloud, and Cybersecurity.
4. 📊 **Evaluation & Analytics Dashboard:** Real-time holdout benchmarking metrics (*Precision@K, Recall@K, RMSE*) comparing Popularity Baseline vs. Content-Based vs. Collaborative vs. Hybrid models.

---

## 2. Design Aesthetics & Visual Tokens 🎨

### Domain-Specific Color Systems

| Domain | Primary Accent | Secondary / Balance Accent | Design Intent |
| :--- | :--- | :--- | :--- |
| 🎬 **Movies & Cinema** | **Velvet Crimson** (`#7A0C24`) | **Antique Gold & Brass** (`#C5A059`) | Classic heritage theatre ambience, cinematic dignity |
| 🛍️ **Products & Lifestyle** | **Charcoal Slate Gray** (`#1E293B` / `#0F172A`) | **Balancing Teal** (`#0D9488` / `#0F766E`) | Sophisticated slate charcoal delivers supreme contrast, rich depth, and luxury horology/tech aesthetic; Balancing Teal Buy CTA gives crisp, intentional focus |
| 🎓 **Courses & Career** | **Electric Cobalt** (`#2563EB`) | **Amber Mint** (`#10B981`) | Academic focus, skill progression, clarity |

### Typography & Component Layout

* **Paper Canvas Base:** High-contrast `#FDFBF7` canvas with stark black ink borders (`2px solid #000000`) and offset box shadows (`4px 4px 0px #000000`).
* **Navigation:** Custom styled Streamlit Tabs with custom active indicator line.
* **Product Cards (`.product-card`):**
  * Border: `2px solid #000000` with `5px solid #1E293B` charcoal slate top accent.
  * Padding: `1.15rem 1.35rem`
  * Hover state: `6px 6px 0px #0D9488` Teal glow with 2px lift transition.
* **Buy CTA (`.product-buy-btn`):** Deep Balancing Teal gradient (`#0D9488` → `#0F766E`) with white text and black ink border, casting a crisp shadow on hover.
* **Explanation Box (`.product-reason-box`):** Charcoal-accented box (`#F8FAFC`) with `5px solid #1E293B` left border explaining recommendation context and AI rationale.

---

## 3. Data Architecture & Schema Specification 🗄️

### A. Movie Entity (`movies_clean.csv`)
* `movieId` (int): Unique identifier
* `title` (str): Movie title + Year
* `industry` (str): `Bollywood` | `Tollywood` | `Hollywood` | `Nepali Cinema`
* `genres` (str): Pipe-separated list (e.g. `Action|Sci-Fi`)
* `avg_rating` (float): 1.0 – 5.0 scale
* `rating_count` (int): Number of audience reviews
* `tag` (str): Plot summary tags, actor names, director names
* `content_features` (str): Combined text vector for TF-IDF

### B. Product Entity (`products_clean.csv`)
* `product_id` (int): Unique identifier
* `product_name` (str): Full item title
* `category` (str): `Audio` | `Wearables` | `Gaming` | `Computer Accessories` | `Smart Home` | `Desk Setup`
* `brand` (str): Top Indian Brand (`boAt`, `Noise`, `Boult`, `Fire-Boltt`, `Fastrack`, etc.)
* `price_inr` (int): Price in Indian Rupees (₹)
* `rating` (float): 1.0 – 5.0 scale
* `features` (str): Keyword features (ANC, 100H playtime, AMOLED, RGB)
* `description` (str): Detailed product description
* `content_features` (str): Combined text vector for TF-IDF

### C. Course Entity (`courses_clean.csv`)
* `course_id` (int): Unique identifier
* `course_title` (str): Full course title
* `organization` (str): Provider (`Google`, `Stanford`, `Meta`, `IBM`, `Harvard`, etc.)
* `category` (str): `Artificial Intelligence` | `Data Science` | `Software Engineering` | `Cloud Computing` | `Cybersecurity` | `Business`
* `difficulty_level` (str): `Beginner` | `Intermediate` | `Advanced`
* `rating` (float): 1.0 – 5.0 scale
* `duration_hours` (int): Total course duration
* `skills` (str): Comma-separated target skills
* `description` (str): Detailed syllabus overview
* `url` (str): Course link
* `content_features` (str): Combined text vector for TF-IDF

---

## 4. Recommender Engine Logic 🤖

### Hybrid Scoring Formula
For an item $i$ and user query/filters $q$:

$$\text{ContentScore}(i, q) = \text{CosineSimilarity}(\text{TFIDF}(q), \text{TFIDF}(i))$$

$$\text{RatingScore}(i) = \frac{\text{Rating}(i)}{\text{MaxRating}}$$

$$\text{HybridScore}(i) = \alpha \cdot \text{ContentScore}(i, q) + (1 - \alpha) \cdot \text{RatingScore}(i)$$

$$\text{MatchPercentage}(i) = \text{Round}(\text{HybridScore}(i) \times 100, 1)$$

Where $\alpha \in [0.0, 1.0]$ is dynamically adjustable by the user via UI sliders in real-time.

---

## 5. System Architecture & Component Interaction 🏛️

```mermaid
graph TD
    subgraph UI ["User Interface Layer (Streamlit App)"]
        Sidebar["Sidebar Component (User Auth & Bookmarks)"]
        Tab1["Movies Tab (Bollywood/Tollywood/Hollywood)"]
        Tab2["Products Tab (E-Commerce & INR ₹)"]
        Tab3["Courses Tab (Skills & Certifications)"]
        Tab4["Evaluation Tab (Metrics & Charts)"]
    end

    subgraph Core ["Engine Layer (Models & Logic)"]
        MovieEng["MovieRecommender Engine"]
        ProdEng["ProductRecommender Engine"]
        CourseEng["CourseRecommender Engine"]
        EvalEng["Evaluation Engine"]
    end

    subgraph Data ["Data & Vector Storage Layer"]
        MovieCSV["movies_clean.csv & movie_ratings_clean.csv"]
        ProdCSV["products_clean.csv & product_ratings_clean.csv"]
        CourseCSV["courses_clean.csv & course_ratings_clean.csv"]
        TFIDF["TF-IDF Vector Matrices & Cosine Index"]
    end

    subgraph DB ["Persistence Layer (SQLite3)"]
        UsersTBL["Users Table (Auth & Passwords)"]
        BookmarksTBL["Saved Items Table (Bookmarks)"]
        FeedbackTBL["User Feedback Table (Likes/Stars)"]
    end

    Tab1 --> MovieEng
    Tab2 --> ProdEng
    Tab3 --> CourseEng
    Tab4 --> EvalEng

    MovieEng --> MovieCSV
    ProdEng --> ProdCSV
    CourseEng --> CourseCSV
    
    MovieEng --> TFIDF
    ProdEng --> TFIDF
    CourseEng --> TFIDF

    Sidebar --> UsersTBL
    Sidebar --> BookmarksTBL
    Tab1 & Tab2 & Tab3 --> FeedbackTBL
```

---

## 6. Folder Structure & Modular Codebase 📂

```
Recommendation-System/
├── DESIGN.md                         # Detailed design specification
├── README.md                         # Project setup & run guide
├── Recommendation_Portal_Project_Plan.pdf
├── data/
│   ├── raw/                          # Raw datasets (MovieLens, etc.)
│   └── cleaned/                      # Preprocessed CSV datasets
├── models/
│   ├── __init__.py
│   ├── movie_rec.py                  # Movie engine (Bollywood, Tollywood, Hollywood)
│   ├── product_rec.py                # Indian Brands product engine (INR ₹)
│   └── course_rec.py                 # Skill-interest course engine
├── database.py                       # SQLite user accounts, bookmarks & feedback
├── evaluation.py                     # Precision@K, Recall@K, RMSE calculation
└── app.py                            # Premium Streamlit web portal
```
