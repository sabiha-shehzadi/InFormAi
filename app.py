import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ===========================
# PAGE CONFIG
# ===========================
st.set_page_config(page_title="Smart Form Automation", layout="wide")
st.title("📄 Smart Form Automation")

st.markdown("""
Upload your file → auto-generate form → collect responses → email the form link to colleagues 🚀
""")

# ===========================
# STEP 1 — Upload File
# ===========================
uploaded_file = st.file_uploader("📤 Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ File uploaded successfully!")
    st.write("**Detected Columns:**", list(df.columns))

    # ===========================
    # STEP 2 — Owner & Colleagues
    # ===========================
    st.subheader("👤 Owner Details")
    owner_email = st.text_input("Owner Email")
    colleagues = st.text_area("Colleagues' emails (comma-separated)")

    # ===========================
    # STEP 3 — Email Setup
    # ===========================
    st.subheader("📧 Email Setup")
    sender_email = st.text_input("Sender Gmail address")
    sender_password = st.text_input("App Password (from Gmail)", type="password")

    # ===========================
    # STEP 4 — Auto Form
    # ===========================
    st.subheader("📝 Fill Form")
    responses = {}
    for col in df.columns:
        responses[col] = st.text_input(f"Enter value for '{col}'", key=col)

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

    if st.button("📊 View All Responses"):
        file_path = "data/responses.csv"
        if os.path.exists(file_path):
            responses_df = pd.read_csv(file_path)
            st.dataframe(responses_df)
            st.download_button("⬇️ Download CSV", responses_df.to_csv(index=False), "responses.csv")
        else:
            st.warning("⚠️ No responses yet!")

    # ===========================
    # STEP 5 — Email Sending
    # ===========================
    st.subheader("📨 Send Form Link to Colleagues")

    if st.button("✉️ Send Emails"):
        if not sender_email or not sender_password:
            st.error("⚠️ Please enter sender email and app password.")
        elif not colleagues.strip():
            st.warning("⚠️ Please enter colleagues' emails.")
        else:
            # Compose and send email
            subject = "New Form to Fill"
            form_link = "http://localhost:8501"  # Change this to your deployed Streamlit link later
            body = f"""
            Hi there,

            You've been invited to fill out a new form.

            👉 Click here to fill the form: {form_link}

            Thanks,
            {owner_email or 'Form Automation System'}
            """

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            try:
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)
                    for email in [e.strip() for e in colleagues.split(',') if e.strip()]:
                        msg['To'] = email
                        server.sendmail(sender_email, email, msg.as_string())
                        st.write(f"✅ Sent to {email}")
                st.success("All emails sent successfully!")
            except Exception as e:
                st.error(f"❌ Error sending emails: {e}")
else:
    st.info("⬆️ Upload a CSV or Excel file to begin.")
