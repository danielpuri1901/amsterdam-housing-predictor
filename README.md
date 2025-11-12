# Amsterdam Student Housing Price Predictor

Predicts rental prices for student housing in Amsterdam using machine learning algorithms.

## Overview
This project analyzes Amsterdam student housing data and builds predictive models to estimate rental prices based on various features such as location, size, amenities, and distance to University of Amsterdam (UvA).

**Tech Stack:** Python, pandas, scikit-learn, matplotlib, seaborn
**Models:** Linear Regression, Decision Tree, Random Forest
**Algorithms:** Feature selection, decision tree traversal, ensemble methods

## Project Structure
```
amsterdam-housing-predictor/
├── data/
│   ├── raw/              # Raw data files
│   └── processed/        # Cleaned and processed data
├── models/               # Saved trained models
├── notebooks/            # Jupyter notebooks for analysis
├── src/                  # Source code
│   ├── data_preprocessing.py
│   ├── train_models.py
│   └── utils.py
├── requirements.txt
└── README.md
```

## Features
The model considers the following features:
- **Location**: Neighborhood/district in Amsterdam
- **Size**: Square meters
- **Room Type**: Studio, shared apartment, private room
- **Amenities**: Furnished, utilities included, internet, etc.
- **Distance to UvA**: Proximity to university campuses
- **Registration**: Whether official registration (inschrijving) is possible

## Models Implemented

### 1. Linear Regression
Baseline model using linear relationships between features and price.

### 2. Decision Tree Regressor
Non-linear model that captures complex relationships through tree-based splits.

### 3. Random Forest Regressor
Ensemble method combining multiple decision trees for improved accuracy and reduced overfitting.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/amsterdam-housing-predictor.git
cd amsterdam-housing-predictor

# Install dependencies
pip install -r requirements.txt
```

## Usage

### 1. Data Preprocessing
```bash
python src/data_preprocessing.py
```

### 2. Train Models
```bash
python src/train_models.py
```

### 3. Jupyter Notebook Analysis
```bash
jupyter notebook notebooks/housing_analysis.ipynb
```

## Model Performance
Models are evaluated using:
- **RMSE (Root Mean Squared Error)**: Measures prediction accuracy
- **R² Score**: Explains variance in the data
- **Cross-validation**: 5-fold CV for robust performance estimates

## Key Learnings
- Implemented supervised learning algorithms from scratch
- Performed exploratory data analysis on Amsterdam housing data
- Compared model performance using RMSE and cross-validation
- Handled real-world data challenges (missing values, outliers, categorical encoding)
- Applied feature engineering to improve model accuracy
- Understood trade-offs between model complexity and interpretability

## Data Sources
- Kamernet (student housing platform)
- Funda (Dutch real estate platform)
- Public datasets on Amsterdam housing

## Future Improvements
- Add neural network models (MLP)
- Implement hyperparameter tuning (GridSearchCV)
- Create web interface for predictions
- Add time-series analysis for price trends
- Include more features (public transport access, safety ratings)

## Author
Created as part of a portfolio project demonstrating machine learning and data science skills.

## License
MIT License
