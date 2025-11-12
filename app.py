"""
Amsterdam Student Housing Price Predictor - Web App

A simple Streamlit web app for predicting housing prices.

To run:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import sys
sys.path.append('src')

from data_preprocessing import HousingDataPreprocessor


# Page configuration
st.set_page_config(
    page_title="Amsterdam Housing Predictor",
    layout="wide"
)


@st.cache_resource
def load_model():
    """Load the trained Random Forest model"""
    try:
        model = joblib.load('models/random_forest.pkl')
        return model
    except:
        st.error("⚠️ Model not found! Run 'python run_analysis.py' first.")
        return None


@st.cache_resource
def load_preprocessor():
    """Load the preprocessor with encoders"""
    preprocessor = HousingDataPreprocessor()
    # Load or recreate label encoders if needed
    return preprocessor


def main():
    """Main app function"""

    # Header
    st.title("Amsterdam Student Housing Price Predictor")
    st.markdown("---")

    # Sidebar - About
    with st.sidebar:
        st.header("About")
        st.write("""
        This app predicts rental prices for student housing in Amsterdam
        using machine learning.

        **Models Used:**
        - Random Forest Regressor
        - Decision Tree
        - Linear Regression

        **Best Model:** Random Forest (R² = 0.946)
        """)

        st.markdown("---")
        st.write("**Data Source:** Sample data + Real market insights")
        st.write("**Built with:** Python, scikit-learn, Streamlit")

    # Main content - Two columns
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("Property Details")

        # Input fields
        location = st.selectbox(
            "Location",
            ["Centrum", "De Pijp", "Oud-West", "Oost", "Noord", "Zuid"],
            help="Choose the neighborhood"
        )

        size = st.slider(
            "Size (m²)",
            min_value=15,
            max_value=120,
            value=50,
            help="Square meters of the property"
        )

        room_type = st.selectbox(
            "Room Type",
            ["Studio", "Shared", "Private Room"],
            help="Type of accommodation"
        )

        distance_to_uva = st.slider(
            "Distance to UvA (km)",
            min_value=0.5,
            max_value=15.0,
            value=3.0,
            step=0.5,
            help="Distance to University of Amsterdam"
        )

        furnished = st.checkbox("Furnished", value=True)
        registration = st.checkbox("Registration Possible", value=True)

    with col2:
        st.header("Prediction")

        # Predict button
        if st.button("💰 Predict Price", type="primary"):
            model = load_model()

            if model is not None:
                # Prepare input data
                input_data = prepare_input(
                    location, size, room_type,
                    distance_to_uva, furnished, registration
                )

                # Make prediction
                predicted_price = model.predict(input_data)[0]

                # Display result
                st.success(f"### Predicted Monthly Rent: €{predicted_price:.2f}")

                # Additional metrics
                st.write("---")
                st.write("**Price Breakdown:**")

                price_per_sqm = predicted_price / size
                st.metric("Price per m²", f"€{price_per_sqm:.2f}/m²")

                # Comparison with averages
                st.write("---")
                st.write("**Market Comparison:**")

                avg_prices = {
                    "Centrum": 1800,
                    "De Pijp": 1500,
                    "Oud-West": 1400,
                    "Oost": 1200,
                    "Noord": 1000,
                    "Zuid": 1600
                }

                avg_for_location = avg_prices.get(location, 1300)
                difference = predicted_price - avg_for_location
                percentage = (difference / avg_for_location) * 100

                if difference > 0:
                    st.write(f"€{difference:.2f} ({percentage:.1f}%) above area average")
                else:
                    st.write(f"€{abs(difference):.2f} ({abs(percentage):.1f}%) below area average")

                # Confidence interval (rough estimate)
                st.write("---")
                st.write("**Confidence Range:**")
                lower = predicted_price * 0.9
                upper = predicted_price * 1.1
                st.write(f"€{lower:.2f} - €{upper:.2f}")

        # Show example data
        st.write("---")
        st.subheader("Example Listings")

        example_data = pd.DataFrame({
            'Location': ['Centrum', 'De Pijp', 'Oost'],
            'Size': [45, 60, 50],
            'Type': ['Studio', 'Private Room', 'Shared'],
            'Avg Price': ['€1,800', '€1,500', '€1,200']
        })

        st.dataframe(example_data, use_container_width=True)

    # Footer - Statistics
    st.markdown("---")
    st.header("Model Performance")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("R² Score", "0.946", help="How well the model fits the data")

    with col2:
        st.metric("RMSE", "€59.33", help="Average prediction error")

    with col3:
        st.metric("Training Samples", "799", help="Number of properties used for training")

    # Show model comparison
    st.write("---")
    st.subheader("Model Comparison")

    comparison_df = pd.DataFrame({
        'Model': ['Random Forest', 'Decision Tree', 'Linear Regression'],
        'R² Score': [0.946, 0.875, 0.785],
        'RMSE (€)': [59.33, 90.55, 118.88],
        'Status': ['✅ Best', '✓ Good', '○ Baseline']
    })

    st.dataframe(comparison_df, use_container_width=True)


def prepare_input(location, size, room_type, distance, furnished, registration):
    """
    Prepare input data for prediction.

    This needs to match the format used during training.
    """

    # Encode categorical variables (same as training)
    location_map = {'Centrum': 0, 'De Pijp': 1, 'Oost': 2, 'Oud-West': 3, 'Noord': 4, 'Zuid': 5}
    room_type_map = {'Shared': 0, 'Private Room': 1, 'Studio': 2}

    location_encoded = location_map.get(location, 0)
    room_type_encoded = room_type_map.get(room_type, 0)

    # Feature engineering (same as training)
    price_per_sqm = 20  # Placeholder (not used for prediction)

    # Distance category
    if distance <= 2:
        distance_category = 3  # Very Close
    elif distance <= 5:
        distance_category = 2  # Close
    elif distance <= 10:
        distance_category = 1  # Moderate
    else:
        distance_category = 0  # Far

    # Size category
    if size <= 20:
        size_category = 0  # Small
    elif size <= 40:
        size_category = 1  # Medium
    elif size <= 60:
        size_category = 2  # Large
    else:
        size_category = 3  # Very Large

    # Create input array (must match training feature order!)
    input_data = np.array([[
        location_encoded,
        size,
        room_type_encoded,
        distance,
        int(furnished),
        int(registration),
        price_per_sqm,  # Will be ignored but needs to be there
        distance_category,
        size_category
    ]])

    return input_data


if __name__ == "__main__":
    main()
