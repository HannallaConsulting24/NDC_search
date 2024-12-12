import streamlit as st
import pandas as pd
import numpy as np

# Load the dataset
@st.cache_data
def load_data():
    file_path = 'Updated_Insurance_Prescription_Data.xlsx'
    return pd.read_excel(file_path).drop_duplicates()

data = load_data()

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

# Input drug name
drug_name = st.selectbox("Type or Select Drug Name (Required):", options=["Type here..."] + list(data['Drug Name'].unique()), index=0)

if drug_name != "Type here...":
    # Input NDC
    ndc_options = list(data['NDC'].unique())
    selected_ndc = st.selectbox("Type or Select NDC (Required):", options=["Type here..."] + list(ndc_options), index=0)

    if selected_ndc != "Type here...":
        # Input insurance
        insurance_options = list(data['Ins'].unique())
        selected_insurance = st.selectbox("Type or Select Insurance (Required):", options=["Type here..."] + list(insurance_options), index=0)

        if selected_insurance != "Type here...":
            # Filter data
            filtered_data = data[(data['Drug Name'] == drug_name) & (data['NDC'] == selected_ndc) & (data['Ins'] == selected_insurance)]

            # Display results
            if not filtered_data.empty:
                st.subheader("Selected Drug Details")
                for _, row in filtered_data.iterrows():
                    st.markdown("---")
                    st.markdown(f"- **NDC**: {row['NDC']}")
                    st.markdown(f"- **Date**: {row['Date']}")
                    st.markdown(f"- **Script**: {row['Script']}")
                    st.markdown(f"- **Copay**: {row['Pat Pay']}")
                    st.markdown(f"- **Insurance Pay**: {row['Ins Pay']}")
                    st.markdown(f"- **Acquisition Cost**: {row['ACQ']}")
                    st.markdown(f"- **Net Profit**: {row['Net Profit']}\")
            else:
                st.warning("No data matches your search criteria.")
