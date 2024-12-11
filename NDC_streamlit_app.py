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

# Streamlit app starts here
st.title("Medication Search Tool 💊")
st.markdown("### Search by NDC Code")

# Search input
ndc_input = st.text_input("Enter NDC Code:", placeholder="Type NDC Code here...")

if ndc_input:
    # Filter data based on NDC
    filtered_data = data[data['NDC'] == ndc_input]

    if not filtered_data.empty:
        st.success(f"Found {len(filtered_data)} result(s) for NDC: {ndc_input}")

        # Display main details
        st.subheader("Drug Details")
        for _, row in filtered_data.iterrows():
            st.markdown(f"- **Drug Name**: {row['Drug Name']}")
            st.markdown(f"- **NDC**: {row['NDC']}")
            st.markdown(f"- **Form**: {row['Form']}")
            st.markdown(f"- **Strength**: {row['Strength']}")
            st.markdown(f"- **Manufacturer**: {row['MFG']}")
            st.markdown(f"- **Patient Pay**: {row['Pat Pay']}")
            st.markdown(f"- **Insurance Pay**: {row['Ins Pay']}")
            st.markdown(f"- **Acquisition Cost**: {row['ACQ_y']}")
            st.markdown(f"- **Class**: {row['Class']}")
            st.markdown(f"- **Insurance**: {row['Ins']}")
            st.markdown("---")

        # Display alternatives based on RxCui
        rxcui_value = filtered_data.iloc[0]['RxCui']
        alternatives = data[(data['RxCui'] == rxcui_value) & (data['NDC'] != ndc_input)]

        if not alternatives.empty:
            st.subheader("Alternative Medications")
            for _, alt_row in alternatives.iterrows():
                st.markdown(f"- **Drug Name**: {alt_row['Drug Name']}")
                st.markdown(f"- **NDC**: {alt_row['NDC']}")
                st.markdown(f"- **Form**: {alt_row['Form']}")
                st.markdown(f"- **Strength**: {alt_row['Strength']}")
                st.markdown(f"- **Manufacturer**: {alt_row['MFG']}")
                st.markdown(f"- **Patient Pay**: {alt_row['Pat Pay']}")
                st.markdown(f"- **Insurance Pay**: {alt_row['Ins Pay']}")
                st.markdown(f"- **Acquisition Cost**: {alt_row['ACQ_y']}")
                st.markdown(f"- **Class**: {alt_row['Class']}")
                st.markdown(f"- **Insurance**: {alt_row['Ins']}")
                st.markdown("---")
        else:
            st.warning("No alternatives found for this RxCui.")
    else:
        st.error(f"No results found for NDC: {ndc_input}")
else:
    st.info("Please enter an NDC code to search.")
