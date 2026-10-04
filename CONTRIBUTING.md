# Contributing to RECOM.ai

Thank you for considering contributing to RECOM.ai! Here's how you can help.

---

## Getting Started

1. **Fork** the repository and clone your fork locally.
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app** to verify everything works:
   ```bash
   streamlit run app.py
   ```
4. **Run tests** before making changes:
   ```bash
   python tests/test_all.py
   ```

---

## Making Changes

1. Create a new branch for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes in the appropriate files.
3. Run the test suite to confirm nothing is broken:
   ```bash
   python tests/test_all.py
   ```
4. Verify the app still runs correctly:
   ```bash
   streamlit run app.py
   ```

---

## Project Structure

| Directory / File | Purpose |
|:---|:---|
| `app.py` | Main Streamlit application |
| `models/` | Recommendation engine classes |
| `database.py` | SQLite3 database operations |
| `evaluation.py` | Model benchmarking logic |
| `components/` | Custom Streamlit components |
| `data/cleaned/` | Preprocessed CSV datasets |
| `tests/` | Test suite |

---

## Adding a New Domain

To add a new recommendation domain (e.g., Books, Restaurants):

1. **Create the dataset** in `data/cleaned/` following the existing CSV schema pattern (must include `content_features` column for TF-IDF).
2. **Create the engine** in `models/` following the pattern in `movie_rec.py` or `product_rec.py`.
3. **Export it** in `models/__init__.py`.
4. **Add a tab** in `app.py` with filters and card rendering.
5. **Add tests** in `tests/test_all.py`.

---

## Code Style

- Use clear, descriptive variable names.
- Add docstrings to all public functions and classes.
- Keep functions focused — one responsibility per function.
- Preserve existing comments and docstrings when editing.

---

## Submitting a Pull Request

1. Push your branch to your fork.
2. Open a Pull Request against the `main` branch.
3. Describe your changes clearly in the PR description.
4. Ensure all 72+ tests pass before requesting review.

---

Thank you for helping improve RECOM.ai! 🚀
