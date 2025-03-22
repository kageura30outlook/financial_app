import streamlit as st
import pandas as pd
import json
import os


#if 'money' not in st.session_state:
    #st.session_state.money = 0

st.title('Financial Tracker')

description = st.text_input('Enter a description for the item:')
cost = st.number_input('Enter the cost of the item' )
earn = st.number_input('Enter how much money you earned:')
#st.session_state.money -= cost
#st.session_state.money += earn

#if 'data' not in st.session_state:  
    #st.session_state.data = []


def save_to_file():
    file_path = 'financial_data.json'
    with open(file_path, 'w') as f:
        json.dump(st.session_state.data, f)
    st.success(f"Data saved to {file_path}")

def load_from_file():
    file_path = 'financial_data.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            st.session_state.data = json.load(f)
        st.success(f"Data loaded from {file_path}")
    else:
        st.warning("No saved data found!")


if st.button('Add Item'):
    if description and (cost or earn):
        st.session_state.data.append({'Description': description, 'Cost': cost, 'Total Money':st.session_state.money})
        st.success('Item added succsesfully')
        save_to_file()

    else:
        st.error('Please enter all the terms!')

if st.button('Load Data'):
    load_from_file()

if st.button('Save Data'):
    save_to_file()

if st.session_state:
    df = pd.DataFrame(st.session_state)
    st.table(df)