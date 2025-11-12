# Amsterdam Student Housing Price Predictor

Machine learning models to predict rental prices for student housing in Amsterdam.

## Overview

This project builds predictive models to estimate Amsterdam student housing rental prices based on location, size, amenities, and distance to University of Amsterdam (UvA). Three regression models were compared: Linear Regression, Decision Tree, and Random Forest.

**Tech Stack:** Python, pandas, scikit-learn, matplotlib, seaborn

## Model Performance

| Model | R² Score | RMSE | Status |
|-------|----------|------|--------|
| Random Forest | 0.946 | €59.33 | Best |
| Decision Tree | 0.875 | €90.55 | Good |
| Linear Regression | 0.785 | €118.88 | Baseline |

The Random Forest model achieved the highest accuracy with an R² of 0.946 and average prediction error of €59.33.

## Project Structure

```
amsterdam-housing-predictor/
├── data/
│   ├── raw/                    # Original data
│   └── processed/              # Cleaned data ready for training
├── models/                     # Saved trained models (.pkl files)
├── notebooks/                  # Jupyter analysis notebooks
├── src/
│   ├── data_preprocessing.py   # Data cleaning and feature engineering
│   ├── train_models.py         # Model training and evaluation
│   ├── utils.py                # Helper functions
│   ├── scrape_funda.py         # Web scraper for Funda data
│   └── load_public_data.py     # Public dataset integration
├── demo.py                     # Command-line demo
├── app.py                      # Streamlit web interface
└── run_analysis.py             # Full pipeline execution
```

## Features

The models use these input features:
- Location (neighborhood/district)
- Size (square meters)
- Room type (studio, shared, private room)
- Distance to UvA (kilometers)
- Furnished (yes/no)
- Registration possible (yes/no)
- Engineered features (price per m², distance category, size category)

## Installation

```bash
git clone https://github.com/danielpuri1901/amsterdam-housing-predictor.git
cd amsterdam-housing-predictor
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Quick Demo

```bash
python demo.py
```

Runs an interactive command-line interface where you can input apartment details and get price predictions.

### Full Analysis Pipeline

```bash
python run_analysis.py
```

Executes the complete pipeline: data loading, preprocessing, model training, evaluation, and saves results.

### Jupyter Notebook

```bash
jupyter notebook notebooks/housing_analysis.ipynb
```

Interactive analysis with visualizations and detailed model comparisons.

### Web Application

```bash
streamlit run app.py
```

Launches a web interface for the price predictor (requires Streamlit installation).

## Data Sources

Sample data was generated based on Amsterdam housing market characteristics. For production use, data can be sourced from:
- Funda API (official real estate data)
- Kamernet (student housing listings)
- CBS Open Data (Statistics Netherlands)
- Amsterdam Open Data portal

## Model Implementation

**Random Forest (Best Performer)**
- 100 decision trees
- Max depth: 15
- Min samples split: 10
- 5-fold cross-validation
- RMSE: €59.33

**Feature Importance**
1. Location (30%)
2. Size (25%)
3. Distance to UvA (20%)
4. Room type (15%)
5. Other features (10%)

## Results

Training set: 799 apartments
Test set: 200 apartments

The Random Forest model shows strong generalization with minimal overfitting (training R²: 0.970, test R²: 0.946).

Prediction visualizations and residual plots are generated in the project root:
- `predictions_comparison.png`
- `residuals_comparison.png`

## Technical Details

**Data Preprocessing**
- Outlier removal using IQR method
- Label encoding for categorical variables
- Feature engineering (derived metrics)
- Train/test split (80/20)
- StandardScaler normalization

**Model Training**
- Hyperparameters tuned for optimal performance
- Cross-validation for robust evaluation
- Model persistence using joblib

## Future Enhancements

- Integration with real-time Funda/Kamernet APIs
- Hyperparameter optimization (GridSearchCV)
- Additional models (XGBoost, neural networks)
- Time-series analysis for price trends
- Deployment to cloud platform
- Mobile application

## License

MIT License
