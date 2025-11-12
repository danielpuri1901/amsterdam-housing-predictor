"""
Data Preprocessing Module for Amsterdam Housing Price Predictor

This module handles data loading, cleaning, and feature engineering.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import os


class HousingDataPreprocessor:
    """Preprocesses housing data for model training."""

    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()

    def load_data(self, filepath):
        """
        Load housing data from CSV file.

        Args:
            filepath (str): Path to the CSV file

        Returns:
            pd.DataFrame: Loaded dataframe
        """
        try:
            df = pd.read_csv(filepath)
            print(f"Data loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
        except FileNotFoundError:
            print(f"Error: File not found at {filepath}")
            return None

    def clean_data(self, df):
        """
        Clean the housing data by handling missing values and outliers.

        Args:
            df (pd.DataFrame): Input dataframe

        Returns:
            pd.DataFrame: Cleaned dataframe
        """
        print("\n=== Data Cleaning ===")
        print(f"Initial shape: {df.shape}")
        print(f"Missing values:\n{df.isnull().sum()}")

        # Remove duplicates
        df = df.drop_duplicates()
        print(f"After removing duplicates: {df.shape}")

        # Handle missing values
        # For numerical columns: fill with median
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].median(), inplace=True)

        # For categorical columns: fill with mode
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].mode()[0], inplace=True)

        # Remove outliers using IQR method for price
        if 'price' in df.columns:
            Q1 = df['price'].quantile(0.25)
            Q3 = df['price'].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df = df[(df['price'] >= lower_bound) & (df['price'] <= upper_bound)]
            print(f"After removing price outliers: {df.shape}")

        print(f"Final cleaned shape: {df.shape}")
        return df

    def feature_engineering(self, df):
        """
        Create new features from existing ones.

        Args:
            df (pd.DataFrame): Input dataframe

        Returns:
            pd.DataFrame: Dataframe with engineered features
        """
        print("\n=== Feature Engineering ===")

        # Price per square meter
        if 'price' in df.columns and 'size' in df.columns:
            df['price_per_sqm'] = df['price'] / df['size']

        # Distance category (if distance_to_uva exists)
        if 'distance_to_uva' in df.columns:
            df['distance_category'] = pd.cut(
                df['distance_to_uva'],
                bins=[0, 2, 5, 10, 100],
                labels=['Very Close', 'Close', 'Moderate', 'Far']
            )

        # Size category
        if 'size' in df.columns:
            df['size_category'] = pd.cut(
                df['size'],
                bins=[0, 20, 40, 60, 1000],
                labels=['Small', 'Medium', 'Large', 'Very Large']
            )

        print(f"Features after engineering: {df.columns.tolist()}")
        return df

    def encode_categorical(self, df, categorical_cols):
        """
        Encode categorical variables using Label Encoding.

        Args:
            df (pd.DataFrame): Input dataframe
            categorical_cols (list): List of categorical column names

        Returns:
            pd.DataFrame: Dataframe with encoded categorical variables
        """
        print("\n=== Encoding Categorical Variables ===")

        for col in categorical_cols:
            if col in df.columns:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le
                print(f"Encoded: {col}")

        return df

    def prepare_features(self, df, target_col='price'):
        """
        Prepare features and target for model training.

        Args:
            df (pd.DataFrame): Input dataframe
            target_col (str): Name of target column

        Returns:
            tuple: (X, y) features and target
        """
        print(f"\n=== Preparing Features ===")
        print(f"Target column: {target_col}")

        # Separate features and target
        X = df.drop(columns=[target_col])
        y = df[target_col]

        # Remove any remaining non-numeric columns
        non_numeric = X.select_dtypes(include=['object']).columns
        if len(non_numeric) > 0:
            print(f"Warning: Removing non-numeric columns: {non_numeric.tolist()}")
            X = X.drop(columns=non_numeric)

        print(f"Feature shape: {X.shape}")
        print(f"Target shape: {y.shape}")

        return X, y

    def split_data(self, X, y, test_size=0.2, random_state=42):
        """
        Split data into training and testing sets.

        Args:
            X: Features
            y: Target
            test_size (float): Proportion of test set
            random_state (int): Random seed

        Returns:
            tuple: (X_train, X_test, y_train, y_test)
        """
        print(f"\n=== Splitting Data ===")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        print(f"Training set: {X_train.shape[0]} samples")
        print(f"Testing set: {X_test.shape[0]} samples")

        return X_train, X_test, y_train, y_test

    def scale_features(self, X_train, X_test):
        """
        Scale features using StandardScaler.

        Args:
            X_train: Training features
            X_test: Testing features

        Returns:
            tuple: (X_train_scaled, X_test_scaled)
        """
        print("\n=== Scaling Features ===")

        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        print("Features scaled successfully")

        return X_train_scaled, X_test_scaled


def main():
    """
    Main function to demonstrate preprocessing pipeline.
    """
    print("Amsterdam Student Housing Price Predictor - Data Preprocessing")
    print("=" * 60)

    # Initialize preprocessor
    preprocessor = HousingDataPreprocessor()

    # Note: This is a template. Replace with actual data loading
    print("\nNote: Add your housing data CSV file to data/raw/ directory")
    print("Expected columns: price, size, location, amenities, distance_to_uva, etc.")

    # Example workflow (uncomment when you have data):
    # df = preprocessor.load_data('data/raw/housing_data.csv')
    # df = preprocessor.clean_data(df)
    # df = preprocessor.feature_engineering(df)
    # df = preprocessor.encode_categorical(df, ['location', 'room_type'])
    # X, y = preprocessor.prepare_features(df)
    # X_train, X_test, y_train, y_test = preprocessor.split_data(X, y)
    # X_train_scaled, X_test_scaled = preprocessor.scale_features(X_train, X_test)
    #
    # # Save processed data
    # pd.DataFrame(X_train_scaled).to_csv('data/processed/X_train.csv', index=False)
    # pd.DataFrame(X_test_scaled).to_csv('data/processed/X_test.csv', index=False)
    # pd.Series(y_train).to_csv('data/processed/y_train.csv', index=False)
    # pd.Series(y_test).to_csv('data/processed/y_test.csv', index=False)


if __name__ == "__main__":
    main()
