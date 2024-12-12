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
    st.image("img.png", use_column_width=True)
with title_col2:
    st.title("Enhanced Medication Query Tool 💊")

# Input Section
st.markdown("### Search Criteria")

# Select drug name
drug_name = st.selectbox("Select Drug Name (Required):", options=[""] + list(data['Drug Name'].unique()))

# Optional filters
if drug_name:
    ndc_options = data[data['Drug Name'] == drug_name]['NDC'].unique()
    selected_ndc = st.selectbox("Select NDC (Optional):", options=[""] + list(ndc_options))

    insurance_options = data['Ins'].dropna().unique()
    selected_insurance = st.selectbox("Select Insurance (Optional):", options=[""] + list(insurance_options))

    # Filter data based on selections
    filtered_data = data[data['Drug Name'] == drug_name]
    if selected_ndc:
        filtered_data = filtered_data[filtered_data['NDC'] == selected_ndc]
    if selected_insurance:
        filtered_data = filtered_data[filtered_data['Ins'] == selected_insurance]

    # Display results
    if not filtered_data.empty:
        st.subheader("Selected Drug Details")
        first_result = filtered_data.iloc[0]
        st.markdown(f"- **Copay**: {first_result['Pat Pay']}")
        st.markdown(f"- **Insurance Pay**: {first_result['Ins Pay']}")
        st.markdown(f"- **Acquisition Cost**: {first_result['ACQ']}")
        st.markdown(f"- **Net Profit**: {first_result['Net Profit']}")

        # Alternatives by Class
        st.subheader("Alternative Drugs by Class")
        if 'ClassDb' in data.columns:
            drug_class = first_result['ClassDb']
            alternatives = data[data['ClassDb'] == drug_class]

            if selected_insurance:
                alternatives = alternatives[alternatives['Ins'] == selected_insurance]

            st.markdown(f"Found {len(alternatives)} alternatives in the same class.")

            sort_option = st.radio("Sort Alternatives By:", ["Highest Net Profit", "Lowest Copay"])
            if sort_option == "Highest Net Profit":
                alternatives = alternatives.sort_values(by="Net Profit", ascending=False)
            elif sort_option == "Lowest Copay":
                alternatives = alternatives.sort_values(by="Pat Pay", ascending=True)

            for _, alt_row in alternatives.iterrows():
                st.markdown("---")
                st.markdown(f"### Alternative: {alt_row['Drug Name']}")
                st.markdown(f"- **NDC**: {alt_row['NDC']}")
                st.markdown(f"- **Copay**: {alt_row['Pat Pay']}")
                st.markdown(f"- **Insurance Pay**: {alt_row['Ins Pay']}")
                st.markdown(f"- **Acquisition Cost**: {alt_row['ACQ']}")
                st.markdown(f"- **Net Profit**: {alt_row['Net Profit']}")
    else:
        st.warning("No data matches your search criteria.")
else:
    st.info("Please select a Drug Name to begin your search.")
