import streamlit as st
import pandas as pd
import numpy as np

# Load the datasets
@st.cache_data
def load_data():
    file_path = 'Final_Updated_Classifications.csv'
    return pd.read_csv(file_path).drop_duplicates()

# Load the data
df = load_data()

# Ensure the NDC and Drug Name columns are strings for comparison and strip whitespace
df['NDC'] = df['NDC'].astype(str).str.strip()
df['Drug Name'] = df['Drug Name'].astype(str).str.strip()
df['class'] = df['class'].astype(str).str.strip()

# Ensure Date column is parsed as datetime for sorting
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Calculate Net Profit dynamically
df['Net Profit'] = (df['Pat Pay'] + df['Ins Pay']) - df['ACQ']

# Insurance mapping (short to full name)
insurance_mapping = {
    'AL': 'Aetna (AL)',
    'BW': 'aetna (BW)',
    'AD': 'Aetna Medicare (AD)',
    'AF': 'Anthem BCBS (AF)',
    'DS': 'Blue Cross Blue Shield (DS)',
    'CA': 'blue shield medicare (CA)',
    'FQ': 'Capital Rx (FQ)',
    'BF': 'Caremark (BF)',
    'ED': 'CatalystRx (ED)',
    'AM': 'Cigna (AM)',
    'BO': 'Default Claim Format (BO)',
    'AP': 'Envision Rx Options (AP)',
    'CG': 'Express Scripts (CG)',
    'BI': 'Horizon (BI)',
    'AJ': 'Humana Medicare (AJ)',
    'BP': 'informedRx (BP)',
    'AO': 'MEDCO HEALTH (AO)',
    'AC': 'MEDCO MEDICARE PART D (AC)',
    'AQ': 'MEDGR (AQ)',
    'CC': 'MY HEALTH LA (CC)',
    'AG': 'Navitus Health Solutions (AG)',
    'AH': 'OptumRx (AH)',
    'AS': 'PACIFICARE LIFE AND H (AS)',
    'FJ': 'Paramount Rx (FJ)',
    'X ': 'PF - DEFAULT (X )',
    'EA': 'Pharmacy Data Management (EA)',
    'DW': 'phcs (DW)',
    'AX': 'PINNACLE (AX)',
    'BN': 'Prescription Solutions (BN)',
    'AA': 'Tri-Care Express Scripts (AA)',
    'AI': 'United Healthcare (AI)'
}

df['Ins Full Name'] = df['Ins'].map(insurance_mapping).fillna(df['Ins'])

# Display logo and title
logo_path = 'img.png'  # Replace with the actual path to your logo
col1, col2 = st.columns([1, 4])
with col1:
    st.image(logo_path, use_container_width=True)
with col2:
    st.title("Enhanced Medication Guiding Tool 💊")

st.markdown("### Input your search criteria below:")

# Input Fields
drug_name_input = st.selectbox("Search for a Drug Name:", options=[""] + list(df['Drug Name'].unique()), format_func=lambda x: x if x else "Type to search...")

if drug_name_input:
    ndcs_for_drug = df[df['Drug Name'] == drug_name_input]['NDC'].unique()
    ndc_input = st.selectbox("Select an NDC:", options=ndcs_for_drug, format_func=lambda x: x if x else "Type to search...")
else:
    ndc_input = None

insurance_input = st.selectbox("Select Insurance:", options=[""] + list(insurance_mapping.values()), format_func=lambda x: x if x else "Type to search...")

# Map insurance input back to short code
insurance_code = [k for k, v in insurance_mapping.items() if v == insurance_input]
insurance_code = insurance_code[0] if insurance_code else None

# Filter data based on inputs
filtered_df = df[df['Drug Name'].str.contains(drug_name_input, na=False, case=False)] if drug_name_input else df
if ndc_input:
    filtered_df = filtered_df[filtered_df['NDC'] == ndc_input]
if insurance_code:
    filtered_df = filtered_df[filtered_df['Ins'] == insurance_code]

# Sort filtered data by latest date
filtered_df = filtered_df.sort_values(by='Date', ascending=False)

if drug_name_input and insurance_code and not filtered_df.empty:
    st.subheader(f"Latest Billing Details :")

    # Display selected drug details
    first_valid_result = filtered_df.iloc[0]
    st.markdown(f"### Drug Name: **{first_valid_result['Drug Name']}**")
    st.markdown(f"- **NDC**: {first_valid_result['NDC']}")
    st.markdown(f"- **Insurance**: {insurance_mapping.get(first_valid_result['Ins'], first_valid_result['Ins'])}")
    st.markdown(f"- **Quantity**: {first_valid_result['Qty']}")
    st.markdown(f"- **Net Profit**: {first_valid_result['Net Profit']}")
    st.markdown(f"- **Copay**: {first_valid_result['Pat Pay']}")
    st.markdown(f"- **Insurance Pay**: {first_valid_result['Ins Pay']}")
    st.markdown(f"- **Acquisition Cost**: {first_valid_result['ACQ']}")
    st.markdown(f"- **Class**: {first_valid_result['class']}")
    st.markdown(f"- **Script**: {first_valid_result['Script']}")
    st.markdown(f"- **Date**: {first_valid_result['Date'].strftime('%m/%d/%Y')}")
    st.markdown("---")

    # Find alternatives by class
    drug_class = first_valid_result['class']
    if drug_class.lower() != 'other':
        # Get the latest entry for each alternative drug name
        alternatives = (df[(df['class'] == drug_class) & (df['Drug Name'] != first_valid_result['Drug Name'])]
                        .sort_values(by='Date', ascending=False)
                        .drop_duplicates(subset=['Drug Name']))

        st.subheader("Alternative Drugs in the Same Class")
        st.markdown(f"**Found {len(alternatives)} alternatives in the same class.**")

        # Sorting options
        sort_option = st.selectbox("Sort Alternatives By:", ["Highest Net Profit", "Lowest Copay"])
        if sort_option == "Highest Net Profit":
            alternatives = alternatives.sort_values(by="Net Profit", ascending=False)
        elif sort_option == "Lowest Copay":
            alternatives = alternatives.sort_values(by="Pat Pay", ascending=True)

        # Display alternatives
        for _, alt_row in alternatives.iterrows():
            st.markdown("---")
            st.markdown(f"### Alternative Drug Name: **{alt_row['Drug Name']}**")
            st.markdown(f"- **Class**: {alt_row['class']}")
            st.markdown(f"- **Copay**: {alt_row['Pat Pay']}")
            st.markdown(f"- **Insurance Pay**: {alt_row['Ins Pay']}")
            st.markdown(f"- **Acquisition Cost**: {alt_row['ACQ']}")
            st.markdown(f"- **Net Profit**: {alt_row['Net Profit']}")
    else:
        st.info("No alternatives available for drugs in the 'Other' class.")
else:
    st.warning("No results found for the selected criteria.")
