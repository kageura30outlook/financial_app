import streamlit as st
import pandas as pd
import json
import os
import datetime

today = datetime.date.today()  # Correct way to get today's date

formatted_date = today.strftime("%d-%m-%Y")  # Format the date as "day-month-year"
formatted_month = today.strftime("%m")  # Format the date as "month"
formatted_year = today.strftime("%Y")  # Format the year
formatted_week = today.isocalendar()[1]  # Get the ISO week number


# Initialize 'money' and 'data' in session state if they don't exist
if 'money' not in st.session_state:
    st.session_state['money'] = 0  # Set initial money to 0

if 'money_month' not in st.session_state:
    st.session_state['money_month'] = 0  # Set initial money to 0

if 'money_week' not in st.session_state:
    st.session_state['money_week'] = 0  # Set initial money to 0

if 'data' not in st.session_state:
    st.session_state['data'] = []  # Initialize data as an empty list

if 'show_button' not in st.session_state:
    st.session_state.show_button = False

if 'show_frame' not in st.session_state:
    st.session_state.show_frame = False


if 'show_week' not in st.session_state:
    st.session_state.show_week = False


if 'monthly_summary' not in st.session_state:
    st.session_state['monthly_summary'] = []

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
cost = int(st.number_input('Enter the cost of the item', format="%d", step=1))
earn = int(st.number_input('Enter how much money you earned:', format="%d", step=1))
# Save the initial value of 'money' before the update
current_money = st.session_state['money']

# Add item to the financial tracker
if st.button('Add Item'):
    st.session_state['money'] -= cost
    st.session_state['money'] += earn
    change = earn - cost

    # Add item to the financial tracker
    if description and (cost or earn):  # Ensure that either cost or earn is entered
        new_item = {
            'Description': description,
            'Cost': cost,
            'Earn': earn,
            'Change Of Money': change,  # Add the week number here
            'Date': formatted_date,
            'Month': formatted_month,
            'Year': formatted_year,
            'Week': formatted_week,  # Add the week number here
            'Total Money': st.session_state['money']  # Set the Total Money based on current session's money before the update
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
    st.warning('Are you sure you want to perform this action?')
    st.session_state.show_button = not st.session_state.show_button
    if st.session_state.show_button:
        confirm = st.checkbox('Yes I am sure')
    if confirm:
        st.session_state['money'] = 0  # Reset 'money' to initial value
        st.session_state['data'] = []  # Reset 'data' to an empty list
        st.success('Data reset successfully!')

# Button to show data for this month
if st.button('Show Data For This Month'):
    st.session_state.show_frame = not st.session_state.show_frame

if st.button('Show Data For This Week'):
    st.session_state.show_week = not st.session_state.show_week

# Calculate total money, total earn, and total cost for the current month
if st.session_state.show_frame:
    total_cost = 0
    total_earn = 0
    for item in st.session_state['data']:
        if item['Month'] == formatted_month and item['Year'] == formatted_year:
            total_cost += item['Cost']
            total_earn += item['Earn']
            st.session_state['money_month'] = total_earn - total_cost

    st.write(f"Total Cost for this Month: ￥{total_cost}")
    st.write(f"Total Earn for this Month: ￥{total_earn}")
    if st.session_state['money_month'] >= 0:
        st.write(f"Total Change for this Month: +￥{st.session_state['money_month']}")
    else:
        st.write(f"Total Change for this Month: -￥{st.session_state['money_month']}")

if st.session_state.show_week:
    total_cost = 0
    total_earn = 0
    for item in st.session_state['data']:
        if item['Week'] == formatted_week and item['Year'] == formatted_year:
            total_cost += item['Cost']
            total_earn += item['Earn']
            st.session_state['money_week'] = total_earn - total_cost
    # Display the calculated values for the current week
    st.write(f"Total Cost for this Week: ￥{total_cost}")
    st.write(f"Total Earn for this Week: ￥{total_earn}")
    if st.session_state['money_week'] >= 0:
        st.write(f"Total Change for this Week: +￥{st.session_state['money_week']}")
    else:
        st.write(f"Total Change for this Week: -￥{st.session_state['money_week']}")

    # Display the calculated values for the current month

if st.button('Show Data Per Month'):
    per_month = {}
    for item in st.session_state['data']:
        month = item.get('Month')
        year = item.get('Year')
        if month is None or year is None:
            continue  # Skip any entries that are malformed
        month_year = month+'-'+year
        if month_year not in per_month:
            per_month[month_year] = {
                'Month_Year' : month_year,
                'Total Earn' : 0,
                'Total Cost' : 0,
                'Total Change': 0
            }
        per_month[month_year]['Total Earn'] += item.get('Earn',0)
        per_month[month_year]['Total Cost'] += item.get('Cost',0)
        per_month[month_year]['Total Change'] += item.get('Change Of Money',0)
    
    st.session_state['monthly_summary'] = list(per_month.values())
    summary_df = pd.DataFrame(st.session_state['monthly_summary'])
    st.write(summary_df) 

# Display the financial data in a table if it's available
if st.session_state['data']:
    # Convert the list of dictionaries directly into a DataFrame
    df = pd.DataFrame(st.session_state['data'])
    df = df.drop(columns=['Month', 'Year','Week'])
    st.session_state['money_month'] = 0  # Set initial money to 0
    st.write(df)
