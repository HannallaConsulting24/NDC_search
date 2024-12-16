import streamlit as st
import pandas as pd
import numpy as np

# تحميل البيانات
@st.cache_data
def load_data():
    file_path = 'Final_Updated_Classifications.csv'
    return pd.read_csv(file_path).drop_duplicates()

@st.cache_data
def load_reclassified_data():
    file_path = 'Updated_Reclassified_DrugDatabase.csv'
    return pd.read_csv(file_path).drop_duplicates()

# تحميل البيانات
df = load_data()
reclassified_df = load_reclassified_data()

# تنظيف الأعمدة والتأكد من التنسيقات
df['NDC'] = df['NDC'].astype(str).str.strip()
df['Drug Name'] = df['Drug Name'].astype(str).str.strip()
reclassified_df['NDC'] = reclassified_df['ndc'].astype(str).str.strip()
reclassified_df['drug_name'] = reclassified_df['drug_name'].astype(str).str.strip()

# حساب الربح الصافي إذا كانت الأعمدة المطلوبة موجودة
if {'Pat Pay', 'Ins Pay', 'ACQ'}.issubset(df.columns):
    df['Net Profit'] = ((df['Pat Pay'] + df['Ins Pay']) - df['ACQ']).round(2)

# واجهة التطبيق
logo_path = 'img.png'  # ضع مسار الشعار هنا
col1, col2 = st.columns([1, 4])
with col1:
    st.image(logo_path, use_container_width=True)
with col2:
    st.title("أداة مساعدة محدثة للأدوية 💊")

st.markdown("### أدخل معايير البحث الخاصة بك:")

# إدخال الـ NDC
ndc_input = st.text_input("أدخل NDC:", value="")

if ndc_input:
    # البحث عن NDC في ملف Final_Updated_Classifications
    filtered_df = df[df['NDC'] == ndc_input]

    if not filtered_df.empty:
        st.subheader(f"تفاصيل الفواتير للـ NDC: {ndc_input}")
        first_result = filtered_df.iloc[0]
        st.markdown(f"- **اسم الدواء**: {first_result['Drug Name']}")
        st.markdown(f"- **الربح الصافي**: {first_result['Net Profit']:.2f}")
        st.markdown(f"- **Copay**: {first_result['Pat Pay']}")
        st.markdown(f"- **Insurance Pay**: {first_result['Ins Pay']}")
        st.markdown(f"- **تكلفة الاستحواذ**: {first_result['ACQ']}")
        st.markdown(f"- **التاريخ**: {first_result['Date'].strftime('%m/%d/%Y') if pd.notnull(first_result['Date']) else 'غير متاح'}")
        st.markdown("---")

        # عرض البدائل
        st.subheader("البدائل من نفس الفئة")
        drug_class = first_result['class']
        alternatives = df[(df['class'] == drug_class) & (df['NDC'] != ndc_input)]
        if not alternatives.empty:
            sort_option = st.selectbox("رتب البدائل حسب:", ["أعلى ربح صافي", "أقل Copay"])
            if sort_option == "أعلى ربح صافي":
                alternatives = alternatives.sort_values(by="Net Profit", ascending=False)
            elif sort_option == "أقل Copay":
                alternatives = alternatives.sort_values(by="Pat Pay", ascending=True)

            for _, alt_row in alternatives.iterrows():
                st.markdown("---")
                st.markdown(f"- **اسم الدواء**: {alt_row['Drug Name']}")
                st.markdown(f"- **الربح الصافي**: {alt_row['Net Profit']:.2f}")
                st.markdown(f"- **Copay**: {alt_row['Pat Pay']}")
                st.markdown(f"- **Insurance Pay**: {alt_row['Ins Pay']}")
                st.markdown(f"- **تكلفة الاستحواذ**: {alt_row['ACQ']}")
        else:
            st.info("لا توجد بدائل متاحة في نفس الفئة.")

    else:
        # إذا لم يتم العثور على الـ NDC، البحث في Updated_Reclassified_DrugDatabase
        reclassified_details = reclassified_df[reclassified_df['NDC'] == ndc_input]
        if not reclassified_details.empty:
            st.subheader(f"تفاصيل إضافية للـ NDC: {ndc_input}")
            first_reclassified_result = reclassified_details.iloc[0]
            st.markdown(f"- **اسم الدواء**: {first_reclassified_result['drug_name']}")
            st.markdown(f"- **الشركة المصنعة (MFG)**: {first_reclassified_result['mfg']}")
            st.markdown(f"- **تكلفة الاستحواذ (ACQ)**: {first_reclassified_result['acq']}")
            st.markdown(f"- **السعر الإجمالي (AWP)**: {first_reclassified_result['awp']}")
            st.markdown(f"- **RxCui**: {first_reclassified_result['rxcui']}")
        else:
            st.warning("لم يتم العثور على بيانات لهذا الـ NDC في أي قاعدة بيانات.")
