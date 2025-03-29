import streamlit as st
import pandas as pd
import json
import os


# Initialize 'money' and 'data' in session state if they don't exist
if 'money' not in st.session_state:
    st.session_state['money'] = 0  # Set initial money to 0

# Title of the app
st.title('Financial Tracker')
# Input fields
description = st.text_input('Enter a description/name for the item:')
cost = st.number_input('Enter the cost of the item')
earn = st.number_input('Enter how much money you earned:')

# Update the total money based on cost and earn
st.session_state['money'] -= cost
st.session_state['money'] += earn

# Function to save data to a file
def save_to_file():
    file_path = 'financial_data.json'
    # The code below "w" mode overwites so change to "a" mode
    with open(file_path, 'w') as f:
        json.dump(st.session_state['data'], f)
    st.success(f"Data saved to {file_path}")

# Function to load data from a file
def load_from_file():
    file_path = 'financial_data.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            st.session_state['data'] = json.load(f)
        st.success(f"Data loaded from {file_path}")
    else:
        st.warning("No saved data found!")

if 'data' not in st.session_state:
    st.session_state['data'] = []


# Add item to the financial tracker
if st.button('Add Item'):
    if description and (cost or earn):  # Ensure that either cost or earn is entered
        st.session_state['data'].append({'Description': description, 'Cost': cost,'Earn': earn, 'Total Money': st.session_state['money']})
        st.success('Item added successfully')
        save_to_file()  # Save data to file after adding the item

    else:
        st.error('Please enter all the required terms!')

# Button to load data from file
if st.button('Load Data'):
    load_from_file()

# Button to save data to file
if st.button('Save Data'):
    save_to_file()

st.write(dict(st.session_state['data']))
# Display the financial data in a table if it's available
if st.session_state['data']:
    df = pd.DataFrame(dict(st.session_state['data']).items(),index = False).T
    st.table(df)