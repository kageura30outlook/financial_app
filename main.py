import streamlit as st
import pandas as pd
money = 0
# Title of the app
st.title('Financial Tracker')

description = st.text_input('Enter a description for the item:')
cost = st.number_input('Enter the cost of the item', min_value=0.0, format="%.2f")
if 'data' not in st.session_state:
    st.session_state.data = []

if st.button('Add Item'):
    if description and cost:
        st.session_state.data.append({'Description': description, 'Cost': cost, 'Total Money':money})
        st.success('Item added succsesfully')
    else:
        st.error('Please enter all the terms!')
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)
    st.table(df)