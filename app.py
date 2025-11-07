import streamlit as st
import pandas as pd
import os

# ================================
# ⚙️ Streamlit App Configuration
# ================================
st.set_page_config(page_title="Smart Form Automation", layout="wide")

st.title("📄 Smart Form Automation")

st.markdown("""
Welcome!  
This tool helps you:
1. Upload a CSV or Excel file  
2. Automatically generate a form based on its headers  
3. Collect and save responses  
4. View or download all responses  
""")

# ================================
# 📤 Step 1: File Upload
# ================================
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ File uploaded successfully!")
    st.write("**Detected columns:**", list(df.columns))

    # ================================
    # 👤 Step 2: Owner Details
    # ================================
    st.subheader("👤 Owner Details")
    owner_email = st.text_input("Owner Email")
    colleagues = st.text_area("Colleagues' emails (comma-separated)")

    # ================================
    # 📝 Step 3: Auto-Generated Form
    # ================================
    st.subheader("📝 Fill Out a Sample Form")

    responses = {}
    for col in df.columns:
        responses[col] = st.text_input(f"Enter value for **{col}**", key=col)

    # ================================
    # 💾 Step 4: Save Response
    # ================================
    if st.button("💾 Save Response"):
        os.makedirs("data", exist_ok=True)
        file_path = "data/responses.csv"
        new_data = pd.DataFrame([responses])

        if os.path.exists(file_path):
            existing = pd.read_csv(file_path)
            final_df = pd.concat([existing, new_data], ignore_index=True)
        else:
            final_df = new_data

        final_df.to_csv(file_path, index=False)
        st.success("✅ Response saved successfully!")

    # ================================
    # 📊 Step 5: View Responses
    # ================================
    if st.button("📊 View All Responses"):
        file_path = "data/responses.csv"
        if os.path.exists(file_path):
            responses_df = pd.read_csv(file_path)
            st.dataframe(responses_df)
            st.download_button(
                "⬇️ Download Responses CSV",
                responses_df.to_csv(index=False),
                "responses.csv",
                "text/csv"
            )
        else:
            st.warning("⚠️ No responses found yet!")

    # ================================
    # 📨 Step 6: Simulate Sending Form Links
    # ================================
    if st.button("📨 Simulate Sending Form Links"):
        if colleagues.strip():
            st.info("Simulated sending form links to:")
            for email in [e.strip() for e in colleagues.split(",") if e.strip()]:
                st.write(f"✅ {email} — https://your-app-link.streamlit.app")
        else:
            st.warning("Please enter at least one colleague email.")
else:
    st.info("⬆️ Please upload a CSV or Excel file to begin.")
