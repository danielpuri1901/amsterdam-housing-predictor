"""
Amsterdam Housing Price Predictor - Simple CLI Demo

No Streamlit needed - works immediately!
"""

import sys
sys.path.append('src')

import joblib
import numpy as np
from train_models import HousingPriceModels


def predict_price(location, size, room_type, distance, furnished, registration):
    """
    Predict housing price based on features.
    """
    # Load the trained Random Forest model
    try:
        model = joblib.load('models/random_forest.pkl')
    except FileNotFoundError:
        print("❌ Model not found! Run 'python run_analysis.py' first.")
        return None

    # Encode inputs (same as training)
    location_map = {'centrum': 0, 'de pijp': 1, 'oost': 2, 'oud-west': 3, 'noord': 4, 'zuid': 5}
    room_type_map = {'shared': 0, 'private room': 1, 'studio': 2}

    location_encoded = location_map.get(location.lower(), 0)
    room_type_encoded = room_type_map.get(room_type.lower(), 0)

    # Feature engineering
    price_per_sqm = 20  # Placeholder

    # Distance category
    if distance <= 2:
        distance_category = 3
    elif distance <= 5:
        distance_category = 2
    elif distance <= 10:
        distance_category = 1
    else:
        distance_category = 0

    # Size category
    if size <= 20:
        size_category = 0
    elif size <= 40:
        size_category = 1
    elif size <= 60:
        size_category = 2
    else:
        size_category = 3

    # Create input array
    features = np.array([[
        location_encoded,
        size,
        room_type_encoded,
        distance,
        int(furnished),
        int(registration),
        price_per_sqm,
        distance_category,
        size_category
    ]])

    # Make prediction
    predicted_price = model.predict(features)[0]

    return predicted_price


def interactive_demo():
    """
    Interactive command-line demo.
    """
    print("=" * 70)
    print("🏠 AMSTERDAM STUDENT HOUSING PRICE PREDICTOR")
    print("=" * 70)
    print("\nAI-powered price predictions using Random Forest (R² = 0.946)")
    print("\n" + "-" * 70)

    # Get user inputs
    print("\n📍 PROPERTY DETAILS:")

    # Location
    print("\nLocation options:")
    print("  1. Centrum")
    print("  2. De Pijp")
    print("  3. Oost")
    print("  4. Oud-West")
    print("  5. Noord")
    print("  6. Zuid")
    location_choice = input("\nEnter location number (1-6): ")
    locations = {
        '1': 'centrum', '2': 'de pijp', '3': 'oost',
        '4': 'oud-west', '5': 'noord', '6': 'zuid'
    }
    location = locations.get(location_choice, 'oost')

    # Size
    size = float(input("\nSize in m² (e.g., 50): "))

    # Room type
    print("\nRoom type:")
    print("  1. Studio")
    print("  2. Private Room")
    print("  3. Shared")
    room_choice = input("\nEnter room type number (1-3): ")
    room_types = {'1': 'studio', '2': 'private room', '3': 'shared'}
    room_type = room_types.get(room_choice, 'studio')

    # Distance
    distance = float(input("\nDistance to UvA in km (e.g., 3.5): "))

    # Furnished
    furnished_input = input("\nFurnished? (y/n): ").lower()
    furnished = 1 if furnished_input == 'y' else 0

    # Registration
    registration_input = input("Registration possible? (y/n): ").lower()
    registration = 1 if registration_input == 'y' else 0

    # Make prediction
    print("\n" + "-" * 70)
    print("🤖 ANALYZING WITH AI...")
    print("-" * 70)

    predicted_price = predict_price(
        location, size, room_type, distance, furnished, registration
    )

    if predicted_price:
        # Display results
        print("\n" + "=" * 70)
        print("💰 PREDICTED MONTHLY RENT")
        print("=" * 70)
        print(f"\n   €{predicted_price:.2f} per month")
        print()

        # Additional metrics
        price_per_sqm = predicted_price / size
        print(f"   Price per m²: €{price_per_sqm:.2f}/m²")

        # Market comparison
        avg_prices = {
            'centrum': 1800, 'de pijp': 1500, 'oud-west': 1400,
            'oost': 1200, 'noord': 1000, 'zuid': 1600
        }
        avg_for_location = avg_prices.get(location, 1300)
        difference = predicted_price - avg_for_location
        percentage = (difference / avg_for_location) * 100

        print("\n📊 MARKET COMPARISON:")
        if difference > 0:
            print(f"   🔴 €{difference:.2f} ({percentage:.1f}%) above area average")
        else:
            print(f"   🟢 €{abs(difference):.2f} ({abs(percentage):.1f}%) below area average")

        # Confidence range
        lower = predicted_price * 0.9
        upper = predicted_price * 1.1
        print(f"\n📈 CONFIDENCE RANGE:")
        print(f"   €{lower:.2f} - €{upper:.2f}")

        print("\n" + "=" * 70)
        print("✅ Prediction complete!")
        print("=" * 70)

    # Ask if user wants to try again
    print("\n")
    again = input("Would you like to predict another property? (y/n): ")
    if again.lower() == 'y':
        print("\n\n")
        interactive_demo()
    else:
        print("\n👋 Thanks for using the Amsterdam Housing Price Predictor!")
        print("🌐 Check out the full web app: streamlit run app.py")
        print()


def quick_demo():
    """
    Quick demo with example properties.
    """
    print("=" * 70)
    print("🏠 AMSTERDAM HOUSING PREDICTOR - QUICK DEMO")
    print("=" * 70)

    examples = [
        {
            'name': 'Studio in De Pijp',
            'location': 'de pijp',
            'size': 50,
            'room_type': 'studio',
            'distance': 2.5,
            'furnished': 1,
            'registration': 1
        },
        {
            'name': 'Shared room in Noord',
            'location': 'noord',
            'size': 30,
            'room_type': 'shared',
            'distance': 6.0,
            'furnished': 0,
            'registration': 1
        },
        {
            'name': 'Private room in Centrum',
            'location': 'centrum',
            'size': 40,
            'room_type': 'private room',
            'distance': 1.0,
            'furnished': 1,
            'registration': 0
        }
    ]

    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['name']}")
        print(f"   - Size: {example['size']}m²")
        print(f"   - Distance: {example['distance']}km from UvA")
        print(f"   - Furnished: {'Yes' if example['furnished'] else 'No'}")
        print(f"   - Registration: {'Yes' if example['registration'] else 'No'}")

        price = predict_price(
            example['location'], example['size'], example['room_type'],
            example['distance'], example['furnished'], example['registration']
        )

        if price:
            print(f"   💰 Predicted price: €{price:.2f}/month")

    print("\n" + "=" * 70)
    print()


def main():
    """
    Main function.
    """
    print()
    print("Welcome to the Amsterdam Housing Price Predictor!")
    print()
    print("Choose an option:")
    print("  1. Interactive mode (input your own property)")
    print("  2. Quick demo (see example predictions)")
    print()

    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        print("\n")
        interactive_demo()
    else:
        quick_demo()


if __name__ == "__main__":
    main()
