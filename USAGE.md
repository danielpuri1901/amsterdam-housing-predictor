# Usage Guide

## Running the Predictor

### Command-Line Demo

The simplest way to test the model:

```bash
python demo.py
```

Choose option 1 for interactive input or option 2 to see example predictions.

### Web Interface

Launch the Streamlit web app:

```bash
streamlit run app.py
```

Note: Requires Streamlit installation. If you encounter dependency issues with Python 3.14, use Python 3.11 or 3.12 instead.

### Full Pipeline

Run the complete analysis pipeline:

```bash
python run_analysis.py
```

This will:
- Load and preprocess data
- Train all three models
- Generate evaluation metrics
- Save trained models to `models/`
- Create visualization plots

## Working with Data

### Using Sample Data

The project includes a sample data generator:

```bash
python src/utils.py
```

This creates `data/raw/sample_housing_data.csv` with 1000 sample apartments.

### Using Real Data

**Public Datasets**

Check `src/load_public_data.py` for integration with:
- CBS Open Data (Statistics Netherlands)
- Amsterdam Open Data portal
- Kaggle datasets

**Web Scraping**

The `src/scrape_funda.py` file provides a template for scraping Funda listings. Note that web scraping should respect robots.txt and terms of service.

**API Integration**

For production use, register for Funda's Partner API at https://www.funda.nl/api for official data access.

## Jupyter Notebook

For detailed analysis and visualization:

```bash
jupyter notebook notebooks/housing_analysis.ipynb
```

The notebook includes:
- Exploratory data analysis
- Feature correlation analysis
- Model training and comparison
- Residual analysis
- Feature importance visualization

## Model Files

Trained models are saved in `models/` as pickle files:
- `random_forest.pkl` (best performer)
- `decision_tree.pkl`
- `linear_regression.pkl`

Load a saved model:

```python
import joblib
model = joblib.load('models/random_forest.pkl')
prediction = model.predict(features)
```

## Deployment

### Local Development

The current setup works for local testing and development.

### Cloud Deployment

**Streamlit Cloud (Free)**
1. Push code to GitHub
2. Visit https://streamlit.io/cloud
3. Connect repository
4. Deploy `app.py`

**API Deployment**

For REST API deployment, Flask or FastAPI can be used. The model files are portable and can be loaded in any Python environment.

## Troubleshooting

**Import Errors**

Ensure virtual environment is activated:
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

**Model Not Found**

Run the analysis pipeline first:
```bash
python run_analysis.py
```

**Streamlit Issues with Python 3.14**

PyArrow (Streamlit dependency) doesn't support Python 3.14 yet. Use Python 3.11 or 3.12, or deploy to Streamlit Cloud which handles dependencies automatically.

## Data Format

Input data should be CSV format with these columns:

```
location,size,room_type,distance_to_uva,furnished,registration_possible,price
Centrum,45,Studio,2.5,1,1,1450
Noord,35,Shared,6.0,0,1,950
```

Categorical values:
- `location`: Centrum, De Pijp, Oost, Oud-West, Noord, Zuid
- `room_type`: Studio, Private Room, Shared
- `furnished`: 0 (no) or 1 (yes)
- `registration_possible`: 0 (no) or 1 (yes)
