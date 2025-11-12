"""
Run complete housing price prediction analysis
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

import sys
sys.path.append('src')

from data_preprocessing import HousingDataPreprocessor
from train_models import HousingPriceModels
from utils import *
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("AMSTERDAM STUDENT HOUSING PRICE PREDICTOR - COMPLETE ANALYSIS")
print("=" * 70)

# Load data
print("\n### STEP 1: Loading Data ###")
df = pd.read_csv('data/raw/sample_housing_data.csv')
print(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")
print("\nFirst few rows:")
print(df.head())

# Initialize preprocessor
print("\n### STEP 2: Data Preprocessing ###")
preprocessor = HousingDataPreprocessor()

# Clean data
df_clean = preprocessor.clean_data(df.copy())

# Feature engineering
df_engineered = preprocessor.feature_engineering(df_clean)

# Encode categorical variables (including engineered features)
categorical_cols = ['location', 'room_type', 'distance_category', 'size_category']
df_encoded = preprocessor.encode_categorical(df_engineered.copy(), categorical_cols)

# Prepare features and target
X, y = preprocessor.prepare_features(df_encoded, target_col='price')

# Split data
X_train, X_test, y_train, y_test = preprocessor.split_data(X, y, test_size=0.2, random_state=42)

# Save processed data
print("\nSaving processed data...")
pd.DataFrame(X_train).to_csv('data/processed/X_train.csv', index=False)
pd.DataFrame(X_test).to_csv('data/processed/X_test.csv', index=False)
pd.Series(y_train).to_csv('data/processed/y_train.csv', index=False, header=True)
pd.Series(y_test).to_csv('data/processed/y_test.csv', index=False, header=True)
print("Processed data saved to data/processed/")

# Model Training and Evaluation
print("\n### STEP 3: Model Training and Evaluation ###")
housing_models = HousingPriceModels()
housing_models.initialize_models()
housing_models.train_all_models(X_train, y_train, X_test, y_test)

# Save models
print("\n### STEP 4: Saving Models ###")
housing_models.save_models('models')

# Generate visualizations
print("\n### STEP 5: Generating Visualizations ###")

# Predictions plot
print("Creating predictions comparison plot...")
housing_models.plot_predictions(y_test, 'predictions_comparison.png')

# Residuals plot
print("Creating residuals plot...")
housing_models.plot_residuals(y_test, 'residuals_comparison.png')

# Feature importance for Random Forest (skipped to avoid plot display issues)
# Can be explored in the Jupyter notebook
print("\nFeature importance analysis available in Jupyter notebook")

# Final summary
print("\n" + "=" * 70)
print("ANALYSIS COMPLETE!")
print("=" * 70)
print("\nGenerated Files:")
print("  - data/processed/X_train.csv, X_test.csv, y_train.csv, y_test.csv")
print("  - models/linear_regression.pkl")
print("  - models/decision_tree.pkl")
print("  - models/random_forest.pkl")
print("  - predictions_comparison.png")
print("  - residuals_comparison.png")
print("\nYou can now open the Jupyter notebook to explore the results interactively!")
