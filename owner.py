import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Restrict access
if "user_role" not in st.session_state or st.session_state.user_role != "owner":
    st.error("🚫 Access denied. Only the owner can view this page.")
    st.stop()

st.title("👤 Owner Dashboard")

uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])
if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
    st.success("✅ File uploaded successfully!")
    st.write("Detected columns:", list(df.columns))

    owner_email = "owner@gmail.com"  # your static email
    colleagues = st.text_area("Colleagues' emails (comma-separated)")
    sender_email = st.text_input("Sender Gmail address")
    sender_password = st.text_input("App Password", type="password")

    # Save unique form template
    os.makedirs("data/forms", exist_ok=True)
    form_name = uploaded_file.name.split('.')[0]
    df.head(0).to_csv(f"data/forms/{form_name}.csv", index=False)

    # Email form link
    if st.button("✉️ Send Form Link"):
        subject = f"Please fill out the form '{form_name}'"
        form_link = f"http://localhost:8501/Form?form={form_name}"
        body = f"""
Hi there,

You've been invited to fill out a new form: **{form_name}**

👉 Click here to fill the form: {form_link}

Thanks,
{owner_email}
"""
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                for email in [e.strip() for e in colleagues.split(',') if e.strip()]:
                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = email
                    msg['Subject'] = subject
                    msg.attach(MIMEText(body, 'plain'))
                    server.sendmail(sender_email, email, msg.as_string())
                    st.write(f"✅ Sent to {email}")
            st.success("All emails sent successfully!")
        except Exception as e:
            st.error(f"❌ Error sending emails: {e}")

# Owner always sees all responses
st.subheader("📊 View All Responses")
os.makedirs("data/responses", exist_ok=True)
response_files = os.listdir("data/responses")

if response_files:
    selected = st.selectbox("Select a form to view responses:", response_files)
    df = pd.read_csv(f"data/responses/{selected}")
    st.dataframe(df)
    st.download_button("⬇️ Download CSV", df.to_csv(index=False), file_name=selected)
else:
    st.info("No responses yet.")
