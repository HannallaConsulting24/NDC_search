import streamlit as st
import pandas as pd
import numpy as np

# Load the primary dataset
@st.cache_data
def load_data():
    file_path = 'Updated_Insurance_Prescription_Data.xlsx'
    return pd.read_excel(file_path).drop_duplicates()

data = load_data()

# Load the alternatives dataset
@st.cache_data
def load_alternative_data():
    alternative_file_path = 'last_dance.xlsx'
    return pd.read_excel(alternative_file_path).drop_duplicates()

alternative_data = load_alternative_data()

# Ensure relevant columns are properly formatted
data['Drug Name'] = data['Drug Name'].str.strip()
data['NDC'] = data['NDC'].astype(str).str.strip()
data['Net Profit'] = (data['Pat Pay'] + data['Ins Pay']) - data['ACQ']

# Title and Logo
title_col1, title_col2 = st.columns([1, 4])
with title_col1:
    st.image("img.png", use_container_width=True)
with title_col2:
    st.title("Enhanced Medication Query Tool 💊")

# Input Section
st.markdown("### Search Criteria")

# Input all fields at once
input_col1, input_col2, input_col3 = st.columns(3)

with input_col1:
    drug_name = st.selectbox("Type or Select Drug Name:", options=["Type here..."] + list(data['Drug Name'].unique()), index=0)

with input_col2:
    ndc_options = list(data['NDC'].unique())
    selected_ndc = st.selectbox("Type or Select NDC:", options=["Type here..."] + list(ndc_options), index=0)

with input_col3:
    insurance_options = list(data['Ins'].unique())
    selected_insurance = st.selectbox("Type or Select Insurance:", options=["Type here..."] + list(insurance_options), index=0)

# Filter and display data if all fields are selected
if drug_name != "Type here..." and selected_ndc != "Type here..." and selected_insurance != "Type here...":
    filtered_data = data[(data['Drug Name'] == drug_name) & (data['NDC'] == selected_ndc) & (data['Ins'] == selected_insurance)]

    if not filtered_data.empty:
        st.subheader("Selected Drug Details")
        for _, row in filtered_data.iterrows():
            st.markdown("---")
            st.markdown(f"- **Date**: {row['Date']}")
            st.markdown(f"- **Script**: {row['Script']}")
            st.markdown(f"- **Copay**: {row['Pat Pay']}")
            st.markdown(f"- **Insurance Pay**: {row['Ins Pay']}")
            st.markdown(f"- **Acquisition Cost**: {row['ACQ']}")
            st.markdown(f"- **Net Profit**: {row['Net Profit']}")

        # Alternatives by Class from the alternative dataset
        st.subheader("Alternative Drugs by Class")
        if 'Class' in alternative_data.columns:
            drug_class = alternative_data[alternative_data['NDC'] == selected_ndc]['Class'].iloc[0]
            alternatives = alternative_data[(alternative_data['Class'] == drug_class) & (alternative_data['NDC'] != selected_ndc)]

            st.markdown(f"Found {len(alternatives)} alternatives in the same class.")

            sort_option = st.radio("Sort Alternatives By:", ["Highest Net Profit", "Lowest Copay"])
            if sort_option == "Highest Net Profit":
                alternatives = alternatives.sort_values(by="Profit", ascending=False)
            elif sort_option == "Lowest Copay":
                alternatives = alternatives.sort_values(by="ACQ_x", ascending=True)

            for _, alt_row in alternatives.iterrows():
                st.markdown("---")
                st.markdown(f"### Alternative: {alt_row['Drug Name']}")
                st.markdown(f"- **NDC**: {alt_row['NDC']}")
                st.markdown(f"- **Copay**: {alt_row['ACQ_x']}")
                st.markdown(f"- **Profit**: {alt_row['Profit']}")
                st.markdown(f"- **Class**: {alt_row['Class']}")
    else:
        st.warning("No data matches your search criteria.")
