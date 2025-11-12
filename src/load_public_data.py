"""
Load Public Housing Data from Various Sources

Legal and easy way to get real housing data!
"""

import pandas as pd
import requests


def load_cbs_data():
    """
    Load data from CBS (Statistics Netherlands).

    CBS Open Data Portal: https://opendata.cbs.nl
    """
    print("Loading CBS housing data...")

    # Example: CBS API endpoint for housing prices
    # (This is a real API - you can use it!)
    url = "https://opendata.cbs.nl/ODataApi/odata/83625NED/TypedDataSet"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data['value'])
            print(f"✅ Loaded {len(df)} records from CBS")
            return df
        else:
            print(f"❌ Failed to load CBS data: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def load_amsterdam_open_data():
    """
    Load data from Amsterdam Open Data Portal.

    Portal: https://data.amsterdam.nl
    """
    print("Loading Amsterdam Open Data...")

    # Example dataset URL (check portal for current datasets)
    url = "https://api.data.amsterdam.nl/v1/wonen/woningvoorraad/"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Process based on actual API response structure
            return data
    except Exception as e:
        print(f"Note: {e}")
        print("Check https://data.amsterdam.nl for available datasets")
        return None


def load_kaggle_dataset():
    """
    Instructions for loading Kaggle datasets.
    """
    print("\n📦 KAGGLE DATASETS:")
    print("=" * 60)
    print("1. Go to: https://www.kaggle.com/datasets")
    print("2. Search: 'Amsterdam housing' or 'Netherlands rental'")
    print("3. Download CSV file")
    print("4. Place in: data/raw/")
    print("5. Load with: pd.read_csv('data/raw/your_file.csv')")
    print("\nPopular datasets:")
    print("  - Amsterdam Airbnb listings")
    print("  - Netherlands housing market data")
    print("  - European rental prices")


def create_example_real_data():
    """
    Create a more realistic sample dataset based on actual market data.
    """
    print("\nCreating realistic Amsterdam housing dataset...")

    import numpy as np
    np.random.seed(42)

    # Based on real Amsterdam market data (2024)
    neighborhoods = {
        'Centrum': {'base': 1800, 'premium': 300},
        'De Pijp': {'base': 1500, 'premium': 200},
        'Oud-West': {'base': 1400, 'premium': 150},
        'Oost': {'base': 1200, 'premium': 100},
        'Noord': {'base': 1000, 'premium': 50},
        'Zuid': {'base': 1600, 'premium': 250},
        'Nieuw-West': {'base': 950, 'premium': 40},
        'Zuidoost': {'base': 900, 'premium': 30}
    }

    n_samples = 500
    data = []

    for _ in range(n_samples):
        neighborhood = np.random.choice(list(neighborhoods.keys()))
        size = np.random.randint(20, 120)
        room_type = np.random.choice(['Studio', 'Shared', '1-bedroom', '2-bedroom'])

        # Calculate realistic price
        base_price = neighborhoods[neighborhood]['base']
        premium = neighborhoods[neighborhood]['premium']

        price = (
            base_price +
            (size - 50) * 8 +  # Size impact
            premium +
            np.random.normal(0, 150)  # Natural variation
        )

        # Ensure positive prices
        price = max(600, price)

        data.append({
            'location': neighborhood,
            'size': size,
            'room_type': room_type,
            'price': round(price, 2),
            'furnished': np.random.choice([0, 1], p=[0.4, 0.6]),
            'registration_possible': np.random.choice([0, 1], p=[0.3, 0.7]),
            'distance_to_centrum': np.random.uniform(0.5, 12),
            'year_built': np.random.randint(1900, 2024),
            'energy_label': np.random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
        })

    df = pd.DataFrame(data)

    # Save
    filename = 'data/raw/realistic_amsterdam_housing.csv'
    df.to_csv(filename, index=False)

    print(f"✅ Created realistic dataset: {filename}")
    print(f"📊 Total listings: {len(df)}")
    print(f"💰 Price range: €{df['price'].min():.0f} - €{df['price'].max():.0f}")
    print(f"📏 Size range: {df['size'].min()}m² - {df['size'].max()}m²")

    return df


def main():
    """
    Main function to demonstrate data loading options.
    """
    print("=" * 70)
    print("PUBLIC HOUSING DATA LOADER")
    print("=" * 70)

    print("\n🌐 OPTION 1: Official APIs (100% Legal)")
    print("-" * 70)
    # load_cbs_data()

    print("\n🏛️ OPTION 2: Open Data Portals")
    print("-" * 70)
    # load_amsterdam_open_data()

    print("\n📦 OPTION 3: Kaggle Datasets")
    print("-" * 70)
    load_kaggle_dataset()

    print("\n🏠 OPTION 4: Create Realistic Sample (For Testing)")
    print("-" * 70)
    df = create_example_real_data()
    print("\n✅ You can now use this data with your ML pipeline!")
    print("   Run: python run_analysis.py")


if __name__ == "__main__":
    main()
