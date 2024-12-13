# Alternatives by RxCui from the alternative dataset
        st.subheader("Alternative Drugs by RxCui")
        if 'RxCui' in alternative_data.columns:
            if not alternative_data[alternative_data['NDC'] == selected_ndc].empty:
                drug_rxcui = alternative_data[alternative_data['NDC'] == selected_ndc]['RxCui'].iloc[0]
            else:
                drug_rxcui = None
            if drug_rxcui is not None:
                alternatives = alternative_data[(alternative_data['RxCui'] == drug_rxcui) & (alternative_data['NDC'] != selected_ndc)]
            else:
                alternatives = pd.DataFrame()

            st.markdown(f"Found {len(alternatives)} alternatives with the same RxCui.")

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
                st.markdown(f"- **RxCui**: {alt_row['RxCui']}")
                st.markdown(f"- **Copay**: {alt_row['Pat Pay']}")
                st.markdown(f"- **Net Profit**: {alt_row['net_2']}")
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
