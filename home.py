import streamlit as st
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load data from Excel file
@st.cache_data  # Cache the data for better performance
def load_data(file_path):
    return pd.read_excel(file_path)

data = load_data("your_excel_file.xlsx")

# Function to filter data based on selected feature and value
def filter_data(feature, value):
    return data[data[feature] == value]

# Main function to build the web app
def main():
    st.title('Your Company Name')
    st.write('Description of your company...')

    # Sidebar
    st.sidebar.title('Features')
    feature_select = st.sidebar.selectbox('Select Feature', ['Brand Name', 'Division', 'Prediction Model'])

    if feature_select == 'Brand Name':
        brand_name = st.sidebar.selectbox('Select Brand', data['Brand'].unique())
        filtered_data = filter_data('Brand', brand_name)

    elif feature_select == 'Division':
        division = st.sidebar.selectbox('Select Division', data['Division'].unique())
        filtered_data = filter_data('Division', division)

    else:
        st.sidebar.write('Prediction Model')
        st.sidebar.write('Enter your input data:')
        brand = st.sidebar.selectbox('Brand', data['Brand'].unique())
        address = st.sidebar.selectbox('Address', data['Address'].unique())
        pin_code = st.sidebar.selectbox('Pin Code', data['Pin Code'].unique())
        demand = st.sidebar.selectbox('Demand', ['Low', 'Medium', 'High'])
        bags_20kg = st.sidebar.slider('Quantity Available (Bags 20Kg)', 1, 100, 50)
        bags_10kg = st.sidebar.slider('Quantity Available (Bags 10Kg)', 1, 100, 50)
        delivery_time = st.sidebar.slider('Delivery Time (Days)', 1, 10, 5)
        calculate_button = st.sidebar.button('Calculate')

        prediction = None

        if calculate_button:
            # Convert 'Demand' column to numerical
            demand_mapping = {'Low': 1, 'Medium': 2, 'High': 3}

            # Predictions
            X = data[['Brand', 'Address', 'Pin Code', 'Demand', 'Quantity Available (Bags 20Kg)',
                      'Quantity Available (Bags 10Kg)', 'Delivery Time (Days)']]
            y = data['Total Quantity (30 Kg Bags)']

            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Convert 'Demand' column to numerical
            X['Demand'] = X['Demand'].map(demand_mapping)

            # Train XGBoost model
            model = xgb.XGBRegressor()
            model.fit(X_train, y_train)

            # Make prediction
            prediction = model.predict([[brand, address, pin_code, demand_mapping[demand], bags_20kg, bags_10kg, delivery_time]])

    # Display filtered data
    st.write(filtered_data)

    # Display prediction
    if prediction is not None:
        st.write('Available Quantity Totals (30 Kg Bags):', prediction[0])

if __name__ == '__main__':
    main()
