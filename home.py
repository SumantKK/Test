import streamlit as st
import pandas as pd

# Load data from Excel file
@st.cache  # Cache the data for better performance
def load_data(file_path):
    return pd.read_excel(file_path)

data = load_data("Survey.xlsx")

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
        brand = st.sidebar.text_input('Brand')
        address = st.sidebar.text_input('Address')
        pin_code = st.sidebar.text_input('Pin Code')
        demand = st.sidebar.number_input('Demand')
        bags_20kg = st.sidebar.number_input('Quantity Available (Bags 20Kg)')
        bags_10kg = st.sidebar.number_input('Quantity Available (Bags 10Kg)')
        delivery_time = st.sidebar.number_input('Delivery Time (Days)')

        # Predictions can be made here using the input data

    # Display filtered data
    st.write(filtered_data)

if __name__ == '__main__':
    main()
