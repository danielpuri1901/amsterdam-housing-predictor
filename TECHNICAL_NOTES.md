# Technical Notes

## Project Overview

This is a regression model that predicts monthly rental prices for student housing in Amsterdam. The project compares three machine learning approaches and demonstrates a complete ML pipeline from data preprocessing to model deployment.

## Model Performance

Testing was done on 200 apartments (20% holdout set):

- **Random Forest**: 94.6% R² (€59 average error) - Selected model
- **Decision Tree**: 87.5% R² (€90 average error)
- **Linear Regression**: 78.5% R² (€118 average error)

The Random Forest model combines 100 decision trees with a maximum depth of 15. Cross-validation confirmed the model generalizes well (5-fold CV RMSE: €69).

## Data Pipeline

Raw data contains apartment listings with categorical and numerical features. The preprocessing steps:

1. Outlier removal using IQR method (removed 1 outlier from 1000 samples)
2. Label encoding for categorical variables (location, room type)
3. Feature engineering (price per m², distance categories, size categories)
4. Train/test split (799/200)

## Feature Engineering

Created three derived features that improved model accuracy:

- **Price per m²**: Normalizes price by apartment size
- **Distance category**: Bins distance to university into ranges (< 2km, 2-5km, 5-10km, > 10km)
- **Size category**: Bins apartment size into ranges (< 20m², 20-40m², 40-60m², > 60m²)

These features helped the model capture non-linear relationships better than raw features alone.

## Implementation Details

**Random Forest Configuration**:
```python
RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42
)
```

The model was not further tuned with GridSearchCV to keep training time reasonable for the dataset size. Training takes approximately 10 seconds on standard hardware.

## Code Structure

Main modules:

- `data_preprocessing.py`: Handles data loading, cleaning, and transformation
- `train_models.py`: Implements model training and evaluation
- `utils.py`: Helper functions for data generation and visualization
- `demo.py`: CLI interface for predictions
- `app.py`: Streamlit web interface

The trained models are serialized using joblib and can be loaded for inference without retraining.

## Data Sources

Currently uses synthetic data generated to match Amsterdam housing market characteristics. For production use, the code includes templates for:

- Funda API integration (requires API key)
- Web scraping (with rate limiting and robots.txt compliance)
- Public dataset integration (CBS, Kaggle)

## Limitations

- Training data is synthetic, generated based on typical Amsterdam market patterns
- Model assumes stable market conditions (doesn't account for seasonal variations)
- Limited feature set (doesn't include amenities like balcony, garden, etc.)
- No handling of unseen categorical values (would need retraining or one-hot encoding)

## Extensions

Potential improvements if this were deployed:

- Hyperparameter tuning with GridSearchCV or RandomizedSearchCV
- Additional features (public transport accessibility, neighborhood safety ratings)
- Time-series component for seasonal price variations
- Ensemble of multiple model types (stacking)
- API endpoint for real-time predictions

## Performance Considerations

Current implementation loads the full model into memory. For high-traffic applications, consider:

- Model quantization for smaller memory footprint
- Caching predictions for common property types
- Batch prediction for bulk requests
- Model serving with TensorFlow Serving or similar

## Dependencies

Core requirements:
- Python 3.11+ (3.14 has compatibility issues with some packages)
- scikit-learn 1.3+
- pandas 2.0+
- numpy 1.24+

Optional for visualization and web interface:
- matplotlib 3.7+
- seaborn 0.12+
- streamlit 1.28+
- jupyter 1.0+

Total package size: ~350MB installed
