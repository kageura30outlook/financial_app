import streamlit as st
import pandas as pd
import json
import os
money = 0
# Title of the app
st.title('Financial Tracker')

description = st.text_input('Enter a description for the item:')
cost = st.number_input('Enter the cost of the item' )
earn = st.number_input('Enter how much money you earned:')
money -= cost
money += earn

def save_to_file():
    file_path = 'financial_data.json'
    with open(file_path, 'w') as f:
        json.dump(st.session_state.data, f)
    st.success(f"Data saved to{file_path}")

def load_from_file():
    file_path = 'financial_data.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f;
            st.session_state =  json.load(f)
        st.success(f"Data loaded from{file_path}")
    else:
        st.warning("No saved data found!")
if 'data' not in st.session_state:
    st.session_state.data = []

if st.button('Add Item'):
    if description and cost or earn:
        st.session_state.data.append({'Description': description, 'Cost': cost, 'Total Money':money})
        st.success('Item added succsesfully')
        save_to_file()

    else:
        st.error('Please enter all the terms!')

if st.button('Load Data'):
    load_from_file()
        
if st.button('Save Data'):
    save_to_file()

if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)
    st.table(df)