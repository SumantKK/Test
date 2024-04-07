import streamlit as st
import pandas as pd

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
        # Add code for prediction model here

if __name__ == '__main__':
    main()
