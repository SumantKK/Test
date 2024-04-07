import streamlit as st
import pandas as pd

# Load data from Excel file
@st.cache_data  # Cache the data for better performance
def load_data(file_path):
    return pd.read_excel(file_path)

data = load_data("Survey.xlsx")

# Main function to build the web app
def main():
    st.title('Your Company Name')
    st.write('Description of your company...')

    # Sidebar
    st.sidebar.title('Features')
    feature_select = st.sidebar.selectbox('Select Feature', ['Brand Name', 'Division', 'Prediction Model'])

    if feature_select == 'Brand Name':
        if 'Brand' in data.columns:
            brand_name = st.sidebar.selectbox('Select Brand', data['Brand'].unique())
            filtered_data = data[data['Brand'] == brand_name]
            st.write(filtered_data)
        else:
            st.sidebar.write("Brand data not found.")

    elif feature_select == 'Division':
        if 'Division' in data.columns:
            pin_code = st.sidebar.selectbox('Select Division', data['Division'].unique())
            filtered_data = data[data['Pin Code'] == pin_code]
            st.write(filtered_data)
        else:
            st.sidebar.write("Division data not found.")

    else:
        st.sidebar.write('Prediction Model')
        # Add code for prediction model here

if __name__ == '__main__':
    main()
