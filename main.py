import streamlit as st
import pandas as pd
import json
import os

# Initialize 'money' and 'data' in session state if they don't exist
if 'money' not in st.session_state:
    st.session_state['money'] = 0  # Set initial money to 0

if 'data' not in st.session_state:
    st.session_state['data'] = []  # Initialize data as an empty list

# Title of the app
st.title('Financial Tracker')

# Function to save data to a file
def save_to_file():
    file_path = 'financial_data.json'
    with open(file_path, 'w') as f:
        json.dump(st.session_state['data'], f)
    st.success(f"Data saved to {file_path}")
# Input fields
description = st.text_input('Enter a description/name for the item:')
cost = int(st.number_input('Enter the cost of the item'))
earn = int(st.number_input('Enter how much money you earned:'))
# Save the initial value of 'money' before the update
current_money = st.session_state['money']


# Add item to the financial tracker
if st.button('Add Item'):

    st.session_state['money'] -= cost
    st.session_state['money'] += earn

# Add item to the financial tracker
    if description and (cost or earn):  # Ensure that either cost or earn is entered
        new_item = {
            'Description': description,
            'Cost': cost,
            'Earn': earn,
            'Total Money': current_money  # Set the Total Money based on current session's money before the update
        }
        # Append the new item to the data list
        st.session_state['data'].append(new_item)
        st.success('Item added successfully')
        save_to_file()  # Save data to file after adding the item
    else:
        st.error('Please enter all the required terms!')

# Function to load data from a file
def load_from_file():
    file_path = 'financial_data.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            st.session_state['data'] = json.load(f)
        st.success(f"Data loaded from {file_path}")
    else:
        st.warning("No saved data found!")

# Button to load data from file
if st.button('Load Data'):
    load_from_file()

# Button to save data to file
if st.button('Save Data'):
    save_to_file()

# Button to reset data
if st.button('Reset Data'):
    st.session_state['money'] = 0  # Reset 'money' to initial value
    st.session_state['data'] = []  # Reset 'data' to an empty list
    st.success('Data reset successfully!')

# Display the current money
st.write(f"Total Money: ${st.session_state['money']}")

# Display the financial data in a table if it's available
if st.session_state['data']:
    # Convert the list of dictionaries directly into a DataFrame
    df = pd.DataFrame(st.session_state['data'])
    st.write(df)
