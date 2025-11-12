"""
Utility functions for Amsterdam Housing Price Predictor
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def plot_price_distribution(df, price_col='price'):
    """
    Plot the distribution of housing prices.

    Args:
        df (pd.DataFrame): Housing dataframe
        price_col (str): Name of price column
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Histogram
    axes[0].hist(df[price_col], bins=50, edgecolor='black', alpha=0.7)
    axes[0].set_xlabel('Price (€)')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Price Distribution')
    axes[0].axvline(df[price_col].mean(), color='r', linestyle='--', label='Mean')
    axes[0].axvline(df[price_col].median(), color='g', linestyle='--', label='Median')
    axes[0].legend()

    # Box plot
    axes[1].boxplot(df[price_col])
    axes[1].set_ylabel('Price (€)')
    axes[1].set_title('Price Box Plot')

    plt.tight_layout()
    plt.show()


def plot_correlation_matrix(df, figsize=(12, 10)):
    """
    Plot correlation matrix heatmap.

    Args:
        df (pd.DataFrame): Dataframe with numeric columns
        figsize (tuple): Figure size
    """
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr()

    plt.figure(figsize=figsize)
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, square=True, linewidths=1)
    plt.title('Feature Correlation Matrix')
    plt.tight_layout()
    plt.show()


def get_summary_statistics(df):
    """
    Get summary statistics for the dataframe.

    Args:
        df (pd.DataFrame): Housing dataframe

    Returns:
        pd.DataFrame: Summary statistics
    """
    print("=== Summary Statistics ===")
    print(df.describe())
    print("\n=== Data Types ===")
    print(df.dtypes)
    print(f"\n=== Missing Values ===")
    print(df.isnull().sum())
    print(f"\nTotal rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")


def plot_feature_vs_price(df, feature_col, price_col='price'):
    """
    Plot relationship between a feature and price.

    Args:
        df (pd.DataFrame): Housing dataframe
        feature_col (str): Name of feature column
        price_col (str): Name of price column
    """
    plt.figure(figsize=(10, 6))

    if df[feature_col].dtype == 'object' or df[feature_col].nunique() < 10:
        # Categorical or few unique values - use box plot
        df.boxplot(column=price_col, by=feature_col, figsize=(12, 6))
        plt.xlabel(feature_col)
        plt.ylabel(price_col)
        plt.title(f'{price_col} by {feature_col}')
        plt.suptitle('')
    else:
        # Continuous - use scatter plot
        plt.scatter(df[feature_col], df[price_col], alpha=0.5)
        plt.xlabel(feature_col)
        plt.ylabel(price_col)
        plt.title(f'{price_col} vs {feature_col}')
        plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def calculate_price_metrics_by_location(df, location_col='location', price_col='price'):
    """
    Calculate price metrics grouped by location.

    Args:
        df (pd.DataFrame): Housing dataframe
        location_col (str): Name of location column
        price_col (str): Name of price column

    Returns:
        pd.DataFrame: Price metrics by location
    """
    metrics = df.groupby(location_col)[price_col].agg([
        ('count', 'count'),
        ('mean', 'mean'),
        ('median', 'median'),
        ('std', 'std'),
        ('min', 'min'),
        ('max', 'max')
    ]).round(2)

    return metrics.sort_values('mean', ascending=False)


def create_sample_dataset(n_samples=1000, save_path=None):
    """
    Create a sample housing dataset for testing.

    Args:
        n_samples (int): Number of samples to generate
        save_path (str): Path to save CSV (optional)

    Returns:
        pd.DataFrame: Sample housing dataframe
    """
    np.random.seed(42)

    locations = ['Centrum', 'De Pijp', 'Oud-West', 'Oost', 'Noord', 'Zuid']
    room_types = ['Studio', 'Shared', 'Private Room']

    data = {
        'location': np.random.choice(locations, n_samples),
        'size': np.random.randint(15, 100, n_samples),
        'room_type': np.random.choice(room_types, n_samples),
        'distance_to_uva': np.random.uniform(0.5, 15, n_samples).round(2),
        'furnished': np.random.choice([0, 1], n_samples),
        'registration_possible': np.random.choice([0, 1], n_samples, p=[0.3, 0.7])
    }

    df = pd.DataFrame(data)

    # Generate realistic prices based on features
    base_price = 500
    location_premium = {'Centrum': 300, 'De Pijp': 200, 'Oud-West': 150,
                       'Oost': 100, 'Noord': 50, 'Zuid': 180}
    type_premium = {'Studio': 200, 'Private Room': 100, 'Shared': 0}

    df['price'] = (
        base_price +
        df['location'].map(location_premium) +
        df['room_type'].map(type_premium) +
        df['size'] * 8 +
        (15 - df['distance_to_uva']) * 10 +
        df['furnished'] * 100 +
        df['registration_possible'] * 50 +
        np.random.normal(0, 100, n_samples)
    ).round(2)

    # Ensure positive prices
    df['price'] = df['price'].clip(lower=400)

    if save_path:
        df.to_csv(save_path, index=False)
        print(f"Sample dataset saved to: {save_path}")

    return df


if __name__ == "__main__":
    print("Utility Functions Module")
    print("=" * 60)
    print("\nAvailable functions:")
    print("  - plot_price_distribution()")
    print("  - plot_correlation_matrix()")
    print("  - get_summary_statistics()")
    print("  - plot_feature_vs_price()")
    print("  - calculate_price_metrics_by_location()")
    print("  - create_sample_dataset()")

    # Create sample dataset for testing
    print("\nCreating sample dataset...")
    sample_df = create_sample_dataset(
        n_samples=1000,
        save_path='data/raw/sample_housing_data.csv'
    )
    print(f"\nSample data shape: {sample_df.shape}")
    print("\nFirst few rows:")
    print(sample_df.head())
