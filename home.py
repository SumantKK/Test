import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb

# Load data from Excel file
@st.cache_data  # Cache the data for better performance
def load_data(file_path):
    return pd.read_excel(file_path)

data = load_data("Survey.xlsx")

# Main function to build the web app
def main():
    st.title('Tile Adhesive Solution')
    st.write('Check availability for available materials of different brands and areas')

    # Sidebar
    st.sidebar.title('Features')
    feature_select = st.sidebar.selectbox('Select Feature', ['Shop Name', 'Brand Name', 'Address', 'Prediction Model'])

    if feature_select == 'Shop Name':
        if 'Shop Name' in data.columns:
            shop_name = st.sidebar.selectbox('Select Shop Name', data['Shop Name'].unique())
            filtered_data = data[data['Shop Name'] == shop_name]
            st.write(filtered_data)
        else:
            st.sidebar.write("Shop Name data not found.")

    elif feature_select == 'Brand Name':
        if 'Brand' in data.columns:
            brand_name = st.sidebar.selectbox('Select Brand', data['Brand'].unique())
            filtered_data = data[data['Brand'] == brand_name]
            st.write(filtered_data)
        else:
            st.sidebar.write("Brand data not found.")

    elif feature_select == 'Address':
        if 'Address' in data.columns:
            address = st.sidebar.selectbox('Select Address', data['Address'].unique())
            filtered_data = data[data['Address'] == address]
            st.write(filtered_data)
        else:
            st.sidebar.write("Address data not found.")

    else:
        st.sidebar.write('Prediction Model')
        st.sidebar.write('Enter input data:')
        address = st.sidebar.selectbox('Address', data['Address'].unique())
        bags_20kg = st.sidebar.selectbox('Quantity Available (Bags 20Kg)', [i for i in range(1, 101)])
        bags_10kg = st.sidebar.selectbox('Quantity Available (Bags 10Kg)', [i for i in range(1, 101)])
        delivery_time = st.sidebar.selectbox('Delivery Time (Days)', [i for i in range(1, 11)])
        calculate_button = st.sidebar.button('Calculate')

        prediction = None

        if calculate_button:
            # Define X and y for prediction
            X = data[['Address', 'Quantity Available (Bags 20Kg)', 'Quantity Available (Bags 10Kg)', 'Delivery Time (Days)']]
            y = data['Total Quantity (30 Kg Bags)']

            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Train XGBoost model
            model = xgb.XGBRegressor()
            model.fit(X_train, y_train)

            # Make prediction
            prediction = model.predict([[address, bags_20kg, bags_10kg, delivery_time]])

            # Display prediction
            if prediction is not None:
                st.write('Total Quantity (30 Kg Bags):', prediction[0])

if __name__ == '__main__':
    main()
