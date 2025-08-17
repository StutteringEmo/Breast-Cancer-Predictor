# Breast Cancer (Original) — Predictor (ANA680)

**Live app:** https://breastcancer-predictor-app-2567fadf7e65.herokuapp.com/  
**Repo:** https://github.com/StutteringEmo/Breast-Cancer-Predictor

End-to-end ML app that predicts **benign vs. malignant** using the UCI *Breast Cancer Wisconsin (Original)* dataset.  
Notebook fetches the data, cleans it, selects the best model via 5-fold CV, trains it, and saves a pipeline used by a Flask web UI.

---

## Dataset
- **Source:** UCI ML Repository (ID 15) via `ucimlrepo`
- **Features:** 9 cytological features (integers 1–10)
- **Target mapping:** `2 → 0 (benign)`, `4 → 1 (malignant)`
- **Missing values:** imputed with `SimpleImputer(strategy="most_frequent")`

## Model
- Tried: Logistic Regression, Random Forest, Gradient Boosting, SVC (RBF)
- Selection: highest **mean CV accuracy** on train (5-fold)
- Winner in this run: **Logistic Regression** (CV ≈ 0.97, Test ≈ 0.95; exact metrics stored)
- **Artifacts:** `app/model.pkl` (pipeline), `app/schema.json` (feature order, labels, metrics)

---

## Run locally (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app/app.py
# then open http://localhost:5000

```

## CI/CD (GitHub Actions → Heroku)
Pushes to **main** auto-deploy to Heroku using `.github/workflows/deploy.yml`.

**Secrets** (Repo → Settings → Secrets and variables → Actions):
- `HEROKU_APP_NAME` = `breastcancer-predictor-app-2567fadf7e65`
- `HEROKU_API_KEY`  = (from Heroku Account Settings → API Key → Reveal)

**Procfile:** `web: gunicorn app.app:app`  
**Runtime:** `python-3.11.9`

## Repo layout
app/
  app.py
  model.pkl
  schema.json
  templates/
    index.html
    result.html
    error.html
.github/workflows/deploy.yml
Procfile
requirements.txt
runtime.txt
Agas_Week2_Assgn#4_ANA680.ipynb

## Quick test values
- Likely **benign**: `5, 1, 1, 1, 2, 1, 3, 1, 1`  
- Likely **malignant**: `10, 10, 10, 8, 7, 10, 9, 10, 7`  
*(All nine fields expect integers 1–10.)*

## Troubleshooting
- **Application error** → Check Heroku logs: Dashboard → *More* → *View logs*.  
- **Model not found** → Ensure `app/model.pkl` and `app/schema.json` are committed.  
- **Build issues** → Confirm `Procfile`, `requirements.txt`, `runtime.txt` exist at repo root.  
- **CI/CD** → Push to `main` to redeploy; Heroku app name in GitHub Secrets must be exact.
