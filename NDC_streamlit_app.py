import streamlit as st
import pandas as pd
import numpy as np

# Load the primary dataset
@st.cache_data
def load_data():
    file_path = 'Updated_Dataset_with_Net_Columns.csv'
    return pd.read_csv(file_path).drop_duplicates()

data = load_data()

# Load the alternatives dataset
@st.cache_data
def load_alternative_data():
    alternative_file_path = 'updated_dataset_with_net_columns (1).csv'
    return pd.read_csv(alternative_file_path).drop_duplicates()

alternative_data = load_alternative_data()

# Ensure relevant columns are properly formatted
data['Drug Name'] = data['Drug Name'].str.strip()
data['NDC'] = data['NDC'].astype(str).str.strip()

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
    drug_name = st.selectbox("Type or Select Drug Name:", options=list(data.dropna(subset=['Drug Name'])['Drug Name'].unique()) + ["Type here..."], index=0)

with input_col2:
    ndc_options = data['NDC'].unique()
    selected_ndc = st.selectbox("Type or Select NDC:", options=list(data.dropna(subset=['NDC'])['NDC'].unique()) + ["Type here..."], index=0)

with input_col3:
    insurance_options = list(data['Ins'].unique())
    selected_insurance = st.selectbox("Type or Select Insurance:", options=list(data.dropna(subset=['Ins'])['Ins'].unique()) + ["Type here..."], index=0)

# Filter and display data if all fields are selected
if drug_name != "Type here..." and selected_ndc != "Type here..." and selected_insurance != "Type here...":
    filtered_data = data[(data['Drug Name'] == drug_name) & (data['NDC'] == selected_ndc) & (data['Ins'] == selected_insurance)]
    filtered_data = filtered_data.sort_values(by='Date', ascending=False).head(1)

    if not filtered_data.empty:
        st.subheader("Selected Drug Details")
        for _, row in filtered_data.iterrows():
            st.markdown("---")
            st.markdown(f"- **Date**: {row['Date']}")
            st.markdown(f"- **Script**: {row['Script']}")
            st.markdown(f"- **Copay**: {row['Pat Pay']}")
            st.markdown(f"- **Insurance Pay**: {row['Ins Pay']}")
            st.markdown(f"- **Acquisition Cost**: {row['ACQ']}")
            st.markdown(f"- **Net Profit**: {row['net_2']}")

        # Alternatives by Class from the alternative dataset
        st.subheader("Alternative Drugs by Class")
        if 'Class' in alternative_data.columns:
            if not alternative_data[alternative_data['NDC'] == selected_ndc].empty:
                drug_class = alternative_data[alternative_data['NDC'] == selected_ndc]['Class'].iloc[0]
            else:
                drug_class = None
            if drug_class is not None:
                alternatives = alternative_data[(alternative_data['Class'] == drug_class) & (alternative_data['NDC'] != selected_ndc)]
            else:
                alternatives = pd.DataFrame()

            st.markdown(f"Found {len(alternatives)} alternatives in the same class.")

            sort_option = st.radio("Sort Alternatives By:", ["Highest Net Profit", "Lowest Copay"])
            if sort_option == "Highest Net Profit":
                if 'net_2' in alternatives.columns and alternatives['net_2'].notnull().any() and alternatives['net_2'].dtype in [np.float64, np.int64]:
                    alternatives = alternatives[alternatives['net_2'].notnull()]
                    alternatives = alternatives.sort_values(by="net_2", ascending=False)
                else:
                    st.warning("Column 'net_2' is missing, contains invalid data, or has an unsupported type in the alternatives dataset.")
            elif sort_option == "Lowest Copay":
                if 'Pat Pay' in alternatives.columns:
                    alternatives = alternatives.sort_values(by="Pat Pay", ascending=True)
                else:
                    st.warning("Column 'Pat Pay' not found in alternatives dataset.")

            for _, alt_row in alternatives.iterrows():
                st.markdown("---")
                st.markdown(f"### Alternative: {alt_row['Drug Name']}")
                st.markdown(f"- **NDC**: {alt_row['NDC']}")
                st.markdown(f"- **Class**: {alt_row['Class']}")
                st.markdown(f"- **RxCui**: {alt_row['RxCui']}")
                st.markdown(f"- **Copay**: {alt_row['Pat Pay']}")
                st.markdown(f"- **Net Profit**: {alt_row['net_2']}")
    else:
        st.warning("No data matches your search criteria.")
