import streamlit as st
import pandas as pd
import numpy as np

# Load the datasets
@st.cache_data
def load_data():
    file_path = 'Final_Updated_Classifications.csv'
    return pd.read_csv(file_path).drop_duplicates()

@st.cache_data
def load_reclassified_data():
    file_path = 'Updated_Reclassified_DrugDatabase.csv'
    return pd.read_csv(file_path).drop_duplicates()

# Load the data
df = load_data()
reclassified_df = load_reclassified_data()

# Ensure the NDC and Drug Name columns are strings for comparison and strip whitespace
df['NDC'] = df['NDC'].astype(str).str.strip()
df['Drug Name'] = df['Drug Name'].astype(str).str.strip()
df['class'] = df['class'].astype(str).str.strip()
reclassified_df['NDC'] = reclassified_df['ndc'].astype(str).str.strip()
reclassified_df['drug_name'] = reclassified_df['drug_name'].astype(str).str.strip()

# Ensure Date column is parsed as datetime for sorting
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Calculate Net Profit dynamically
df['Net Profit'] = ((df['Pat Pay'] + df['Ins Pay']) - df['ACQ']).round(2)

# Input Fields
st.title("Enhanced Medication Guiding Tool 💊")
drug_name_input = st.selectbox("Search for a Drug Name:", options=[""] + list(df['Drug Name'].unique()), format_func=lambda x: x if x else "Type to search...")

if drug_name_input:
    ndcs_for_drug = df[df['Drug Name'] == drug_name_input]['NDC'].unique()
    ndc_input = st.selectbox("Select an NDC:", options=[""] + list(ndcs_for_drug), format_func=lambda x: x if x else "Type to search...")

    if ndc_input:
        # Check if NDC exists in Final_Updated_Classifications
        filtered_df = df[df['NDC'] == ndc_input]

        if not filtered_df.empty:
            st.subheader("Billing Details")
            first_valid_result = filtered_df.iloc[0]
            st.markdown(f"### Drug Name: **{first_valid_result['Drug Name']}**")
            st.markdown(f"- **NDC**: {first_valid_result['NDC']}")
            st.markdown(f"- **Net Profit**: {first_valid_result['Net Profit']:.2f}")
            st.markdown(f"- **Copay**: {first_valid_result['Pat Pay']}")
            st.markdown(f"- **Insurance Pay**: {first_valid_result['Ins Pay']}")
            st.markdown(f"- **Acquisition Cost**: {first_valid_result['ACQ']}")

            # Find alternatives in the same class
            drug_class = first_valid_result['class']
            alternatives = df[(df['class'] == drug_class) & (df['Drug Name'] != first_valid_result['Drug Name'])]

            if not alternatives.empty:
                st.subheader("Alternative Drugs in the Same Class")
                sort_option = st.selectbox("Sort Alternatives By:", ["Lowest Acquisition Cost", "Alphabetical Drug Name"])
                
                if sort_option == "Lowest Acquisition Cost":
                    alternatives = alternatives.sort_values(by="ACQ")
                elif sort_option == "Alphabetical Drug Name":
                    alternatives = alternatives.sort_values(by="Drug Name")

                for _, alt_row in alternatives.iterrows():
                    st.markdown("---")
                    st.markdown(f"### Alternative Drug Name: **{alt_row['Drug Name']}**")
                    st.markdown(f"- **NDC**: {alt_row['NDC']}")
                    st.markdown(f"- **Acquisition Cost**: {alt_row['ACQ']}")
                    st.markdown(f"- **Net Profit**: {alt_row['Net Profit']:.2f}")
            else:
                st.info("No alternatives available for this class.")

        else:
            # Fetch details from Updated_Reclassified_DrugDatabase
            formatted_ndc = f"{ndc_input[:5]}-{ndc_input[5:9]}-{ndc_input[9:]}"
            reclassified_details = reclassified_df[reclassified_df['ndc'] == formatted_ndc]

            if not reclassified_details.empty:
                st.subheader("Reclassified Drug Details")
                first_reclassified_result = reclassified_details.iloc[0]
                st.markdown(f"### Drug Name: **{first_reclassified_result['drug_name']}**")
                st.markdown(f"- **Manufacturer (MFG)**: {first_reclassified_result['mfg']}")
                st.markdown(f"- **Acquisition Cost (ACQ)**: {first_reclassified_result['acq']}")
                st.markdown(f"- **Average Wholesale Price (AWP)**: {first_reclassified_result['awp']}")
                st.markdown(f"- **RxCui**: {first_reclassified_result['rxcui']}")

                # Find alternatives in Updated_Reclassified_DrugDatabase
                reclassified_alternatives = reclassified_df[reclassified_df['epc_class'] == first_reclassified_result['epc_class']]

                if not reclassified_alternatives.empty:
                    st.subheader("Alternative Drugs in the Same Class (Reclassified Database)")
                    sort_option = st.selectbox("Sort Alternatives By:", ["Lowest Acquisition Cost", "Alphabetical Drug Name"])

                    if sort_option == "Lowest Acquisition Cost":
                        reclassified_alternatives = reclassified_alternatives.sort_values(by="acq")
                    elif sort_option == "Alphabetical Drug Name":
                        reclassified_alternatives = reclassified_alternatives.sort_values(by="drug_name")

                    for _, alt_row in reclassified_alternatives.iterrows():
                        st.markdown("---")
                        st.markdown(f"### Alternative Drug Name: **{alt_row['drug_name']}**")
                        st.markdown(f"- **NDC**: {alt_row['ndc']}")
                        st.markdown(f"- **Manufacturer (MFG)**: {alt_row['mfg']}")
                        st.markdown(f"- **Acquisition Cost (ACQ)**: {alt_row['acq']}")
                else:
                    st.info("No alternatives available in the reclassified database.")
            else:
                st.warning("No data found for this NDC in either database.")
