# Amsterdam Student Housing Price Predictor

Machine-learning models that predict student-rental prices in Amsterdam from location, size, room type, distance to UvA, and amenities. Random Forest beat Linear Regression and Decision Tree on a held-out test set.

| Model | R² (test) | RMSE | Notes |
|---|---|---|---|
| **Random Forest** | **0.946** | **€59.33** | Best |
| Decision Tree | 0.875 | €90.55 | Good |
| Linear Regression | 0.785 | €118.88 | Baseline |

Training set: 799 apartments · test set: 200 apartments · minimal overfitting (train R²=0.970, test R²=0.946).

> Built by [Daniel Puri](https://github.com/danielpuri1901) — applied AI engineer based in Amsterdam. See [my profile](https://github.com/danielpuri1901) for related work on multi-agent systems, Gurobi optimization, and the open-source [`optimaze-agent`](https://github.com/danielpuri1901/optimaze-agent) project.

**Stack:** Python · pandas · scikit-learn · matplotlib · seaborn · Streamlit

## Features used

Location · size (m²) · room type (studio / shared / private) · distance to UvA (km) · furnished · registration possible · engineered features (price per m², distance category, size category).

**Feature importance (Random Forest):** location 30% · size 25% · distance to UvA 20% · room type 15% · other 10%.

## Project layout

```
amsterdam-housing-predictor/
├── data/
│   ├── raw/                    # Original data
│   └── processed/              # Cleaned data ready for training
├── models/                     # Saved trained models (.pkl)
├── notebooks/                  # Jupyter analysis notebooks
├── src/
│   ├── data_preprocessing.py   # Cleaning + feature engineering
│   ├── train_models.py         # Training + evaluation
│   ├── utils.py
│   ├── scrape_funda.py         # Funda scraper
│   └── load_public_data.py     # Public dataset integration
├── demo.py                     # CLI demo
├── app.py                      # Streamlit web interface
└── run_analysis.py             # Full pipeline
```

## Run it

```bash
git clone https://github.com/danielpuri1901/amsterdam-housing-predictor.git
cd amsterdam-housing-predictor
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### CLI demo
```bash
python demo.py
```

### Full pipeline (load → preprocess → train → evaluate → save)
```bash
python run_analysis.py
```

### Streamlit web app
```bash
streamlit run app.py
```

## Data sources

Sample data was generated from Amsterdam market characteristics. For production use the same pipeline can ingest:
- Funda API (real estate)
- Kamernet (student housing)
- CBS Open Data (Statistics Netherlands)
- Amsterdam Open Data portal

## Method

- Outlier removal via IQR
- Label encoding for categoricals
- Engineered features (price per m², distance/size buckets)
- 80/20 train/test split
- `StandardScaler` normalization
- 5-fold cross-validation
- Model persistence via `joblib`

**Random Forest hyperparameters:** 100 trees · max depth 15 · min samples split 10.

Prediction and residual plots are written to the project root (`predictions_comparison.png`, `residuals_comparison.png`).

## See also

- [`TECHNICAL_NOTES.md`](TECHNICAL_NOTES.md) — implementation details
- [`USAGE.md`](USAGE.md) — extended usage guide

## License

MIT.
