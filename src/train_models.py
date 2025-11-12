"""
Model Training Module for Amsterdam Housing Price Predictor

Implements and compares Linear Regression, Decision Tree, and Random Forest models.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import cross_val_score
import joblib
import os


class HousingPriceModels:
    """Train and evaluate multiple regression models for housing price prediction."""

    def __init__(self):
        self.models = {}
        self.results = {}

    def initialize_models(self):
        """Initialize all regression models."""
        print("=== Initializing Models ===")

        # 1. Linear Regression
        self.models['Linear Regression'] = LinearRegression()

        # 2. Decision Tree Regressor
        self.models['Decision Tree'] = DecisionTreeRegressor(
            max_depth=10,
            min_samples_split=20,
            min_samples_leaf=10,
            random_state=42
        )

        # 3. Random Forest Regressor
        self.models['Random Forest'] = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1
        )

        print(f"Initialized {len(self.models)} models:")
        for name in self.models.keys():
            print(f"  - {name}")

    def train_model(self, model_name, X_train, y_train):
        """
        Train a specific model.

        Args:
            model_name (str): Name of the model
            X_train: Training features
            y_train: Training target

        Returns:
            Trained model
        """
        print(f"\nTraining {model_name}...")
        model = self.models[model_name]
        model.fit(X_train, y_train)
        print(f"{model_name} training completed")
        return model

    def evaluate_model(self, model_name, model, X_train, y_train, X_test, y_test):
        """
        Evaluate model performance on training and testing sets.

        Args:
            model_name (str): Name of the model
            model: Trained model
            X_train: Training features
            y_train: Training target
            X_test: Testing features
            y_test: Testing target

        Returns:
            dict: Dictionary containing evaluation metrics
        """
        print(f"\nEvaluating {model_name}...")

        # Predictions
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)

        # Metrics for training set
        train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
        train_mae = mean_absolute_error(y_train, y_train_pred)
        train_r2 = r2_score(y_train, y_train_pred)

        # Metrics for testing set
        test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
        test_mae = mean_absolute_error(y_test, y_test_pred)
        test_r2 = r2_score(y_test, y_test_pred)

        # Cross-validation score
        cv_scores = cross_val_score(
            model, X_train, y_train,
            cv=5,
            scoring='neg_mean_squared_error'
        )
        cv_rmse = np.sqrt(-cv_scores.mean())

        results = {
            'train_rmse': train_rmse,
            'train_mae': train_mae,
            'train_r2': train_r2,
            'test_rmse': test_rmse,
            'test_mae': test_mae,
            'test_r2': test_r2,
            'cv_rmse': cv_rmse,
            'predictions': y_test_pred
        }

        # Print results
        print(f"\n{model_name} Performance:")
        print(f"  Training RMSE: €{train_rmse:.2f}")
        print(f"  Training R²: {train_r2:.4f}")
        print(f"  Testing RMSE: €{test_rmse:.2f}")
        print(f"  Testing MAE: €{test_mae:.2f}")
        print(f"  Testing R²: {test_r2:.4f}")
        print(f"  Cross-Val RMSE: €{cv_rmse:.2f}")

        return results

    def train_all_models(self, X_train, y_train, X_test, y_test):
        """
        Train and evaluate all models.

        Args:
            X_train: Training features
            y_train: Training target
            X_test: Testing features
            y_test: Testing target
        """
        print("\n" + "=" * 60)
        print("Training All Models")
        print("=" * 60)

        for model_name in self.models.keys():
            # Train
            model = self.train_model(model_name, X_train, y_train)

            # Evaluate
            results = self.evaluate_model(
                model_name, model, X_train, y_train, X_test, y_test
            )
            self.results[model_name] = results

        # Print comparison
        self.print_model_comparison()

    def print_model_comparison(self):
        """Print comparison table of all models."""
        print("\n" + "=" * 60)
        print("MODEL COMPARISON")
        print("=" * 60)

        comparison_df = pd.DataFrame({
            'Model': list(self.results.keys()),
            'Test RMSE': [self.results[m]['test_rmse'] for m in self.results],
            'Test R²': [self.results[m]['test_r2'] for m in self.results],
            'CV RMSE': [self.results[m]['cv_rmse'] for m in self.results]
        })

        comparison_df = comparison_df.sort_values('Test RMSE')
        print(comparison_df.to_string(index=False))

        best_model = comparison_df.iloc[0]['Model']
        print(f"\n🏆 Best Model: {best_model}")

    def plot_predictions(self, y_test, save_path=None):
        """
        Plot predicted vs actual prices for all models.

        Args:
            y_test: Actual test target values
            save_path (str): Path to save the plot
        """
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))

        for idx, (model_name, results) in enumerate(self.results.items()):
            ax = axes[idx]
            y_pred = results['predictions']

            ax.scatter(y_test, y_pred, alpha=0.5)
            ax.plot([y_test.min(), y_test.max()],
                   [y_test.min(), y_test.max()],
                   'r--', lw=2)
            ax.set_xlabel('Actual Price (€)')
            ax.set_ylabel('Predicted Price (€)')
            ax.set_title(f'{model_name}\nR² = {results["test_r2"]:.3f}')
            ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"\nPlot saved to: {save_path}")
        else:
            plt.show()

    def plot_residuals(self, y_test, save_path=None):
        """
        Plot residuals for all models.

        Args:
            y_test: Actual test target values
            save_path (str): Path to save the plot
        """
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))

        for idx, (model_name, results) in enumerate(self.results.items()):
            ax = axes[idx]
            y_pred = results['predictions']
            residuals = y_test - y_pred

            ax.scatter(y_pred, residuals, alpha=0.5)
            ax.axhline(y=0, color='r', linestyle='--', lw=2)
            ax.set_xlabel('Predicted Price (€)')
            ax.set_ylabel('Residuals (€)')
            ax.set_title(f'{model_name} Residuals')
            ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Residuals plot saved to: {save_path}")
        else:
            plt.show()

    def save_models(self, save_dir='models'):
        """
        Save all trained models to disk.

        Args:
            save_dir (str): Directory to save models
        """
        os.makedirs(save_dir, exist_ok=True)

        for model_name, model in self.models.items():
            filename = model_name.lower().replace(' ', '_') + '.pkl'
            filepath = os.path.join(save_dir, filename)
            joblib.dump(model, filepath)
            print(f"Saved: {filepath}")

    def load_model(self, model_path):
        """
        Load a trained model from disk.

        Args:
            model_path (str): Path to the model file

        Returns:
            Loaded model
        """
        model = joblib.load(model_path)
        print(f"Model loaded from: {model_path}")
        return model

    def feature_importance(self, X, model_name='Random Forest', top_n=10):
        """
        Display feature importance for tree-based models.

        Args:
            X: Feature dataframe
            model_name (str): Name of the model
            top_n (int): Number of top features to display
        """
        if model_name not in ['Decision Tree', 'Random Forest']:
            print(f"Feature importance not available for {model_name}")
            return

        model = self.models[model_name]
        feature_names = X.columns if hasattr(X, 'columns') else [f'Feature_{i}' for i in range(X.shape[1])]

        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=False)

        print(f"\n{model_name} - Top {top_n} Important Features:")
        print(importance_df.head(top_n).to_string(index=False))

        # Plot
        plt.figure(figsize=(10, 6))
        plt.barh(importance_df['Feature'].head(top_n)[::-1],
                importance_df['Importance'].head(top_n)[::-1])
        plt.xlabel('Importance')
        plt.title(f'{model_name} - Feature Importance')
        plt.tight_layout()
        plt.show()


def main():
    """
    Main function to demonstrate model training pipeline.
    """
    print("Amsterdam Student Housing Price Predictor - Model Training")
    print("=" * 60)

    print("\nNote: This script requires preprocessed data from data_preprocessing.py")
    print("Expected files in data/processed/:")
    print("  - X_train.csv, X_test.csv, y_train.csv, y_test.csv")

    # Example workflow (uncomment when you have preprocessed data):
    # # Load preprocessed data
    # X_train = pd.read_csv('data/processed/X_train.csv')
    # X_test = pd.read_csv('data/processed/X_test.csv')
    # y_train = pd.read_csv('data/processed/y_train.csv').squeeze()
    # y_test = pd.read_csv('data/processed/y_test.csv').squeeze()
    #
    # # Initialize and train models
    # housing_models = HousingPriceModels()
    # housing_models.initialize_models()
    # housing_models.train_all_models(X_train, y_train, X_test, y_test)
    #
    # # Plot results
    # housing_models.plot_predictions(y_test, 'predictions_comparison.png')
    # housing_models.plot_residuals(y_test, 'residuals_comparison.png')
    #
    # # Feature importance
    # housing_models.feature_importance(X_train, 'Random Forest')
    #
    # # Save models
    # housing_models.save_models('models')


if __name__ == "__main__":
    main()
