import streamlit as st
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load data from Excel file
@st.cache  # Cache the data for better performance
def load_data(file_path):
    return pd.read_excel(file_path)

data = load_data("Survey.xlsx")

# Function to filter data based on selected feature and value
def filter_data(feature, value):
    return data[data[feature] == value]

# Function to convert demand values to categorical
def convert_demand(value):
    if value > 75:
        return 'High'
    elif value > 50:
        return 'Medium'
    else:
        return 'Low'

# Main function to build the web app
def main():
    st.title('Your Company Name')
    st.write('Description of your company...')

    # Sidebar
    st.sidebar.title('Features')
    feature_select = st.sidebar.selectbox('Select Feature', ['Brand Name', 'Division', 'Prediction Model'])

    filtered_data = data  # Initialize filtered_data with original data

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
        demand = st.sidebar.selectbox('Demand', ['High', 'Medium', 'Low'])
        bags_20kg = st.sidebar.select_slider('Quantity Available (Bags 20Kg)', options=range(1, 101), value=50)
        bags_10kg = st.sidebar.select_slider('Quantity Available (Bags 10Kg)', options=range(1, 101), value=50)
        delivery_time = st.sidebar.select_slider('Delivery Time (Days)', options=range(1, 11), value=5)

        # Convert categorical variables to numerical
        label_encoder = LabelEncoder()
        demand = label_encoder.fit_transform([demand])[0]

        # Predictions
        st.sidebar.write('Predictions:')
        if st.sidebar.button('Calculate'):
            X = data[['Brand', 'Address', 'Pin Code', 'Demand', 'Quantity Available (Bags 20Kg)',
                      'Quantity Available (Bags 10Kg)', 'Delivery Time (Days)']]
            y = data['Total Quantity (30 Kg Bags)']
            
            # Splitting data for training and testing
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Convert categorical variables to numerical
            X['Demand'] = label_encoder.fit_transform(X['Demand'])

            # Train XGBoost model
            model = xgb.XGBRegressor()
            model.fit(X_train, y_train)
            
            # Make prediction
            prediction = model.predict([[brand, address, pin_code, demand, bags_20kg, bags_10kg, delivery_time]])
            
            st.write('Available Quantity Totals (30 Kg Bags):', prediction[0])

    # Display filtered data
    st.write(filtered_data)

if __name__ == '__main__':
    main()
