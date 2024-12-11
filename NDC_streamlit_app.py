import streamlit as st
import pandas as pd

# Load the dataset
@st.cache_data
def load_data():
    file_path = 'last_dance.xlsx'
    return pd.read_excel(file_path)

# Load the data
data = load_data()

# Ensure the NDC column is string for consistent search
data['NDC'] = data['NDC'].astype(str).str.strip()

# Sort NDC options by their frequency of occurrence
ndc_frequency = data['NDC'].value_counts()
dc_options = sorted(data['NDC'].unique(), key=lambda x: -ndc_frequency.get(x, 0))

# Streamlit app starts here
st.title("Medication Search Tool 💊")
st.markdown("### Search by NDC Code and Insurance")

# Fetch unique values for dropdowns and sort Insurance options based on the selected NDC
ndc_input = st.selectbox("Select NDC Code:", options=[""] + dc_options, format_func=lambda x: x if x else "Type or select an NDC Code...")

if ndc_input:
    related_insurance = data[data['NDC'] == ndc_input]['Ins'].value_counts()
    insurance_options = sorted(data['Ins'].unique(), key=lambda x: -related_insurance.get(x,0) etc .....
    insure_option=st.text_filed
