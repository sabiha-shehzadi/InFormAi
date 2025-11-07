import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- Restrict Access to Owner Only ---
if "user_role" not in st.session_state or st.session_state.user_role != "owner":
    st.error("🚫 Access denied. Only the owner can view this page.")
    st.stop()

st.title("👤 Owner Dashboard")

# --- Upload File ---
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ File uploaded successfully!")
    st.write("Detected columns:", list(df.columns))

    # Static owner email
    owner_email = "owner@gmail.com"  # 👈 replace with your owner email

    # Get colleague list and credentials
    colleagues = st.text_area("Colleagues' emails (comma-separated)")
    sender_email = st.text_input("Sender Gmail address (same as owner)")
    sender_password = st.text_input("App Password", type="password")

    # Prepare file saving
    os.makedirs("data/forms", exist_ok=True)
    os.makedirs("data/responses", exist_ok=True)

    form_name = uploaded_file.name.split('.')[0]
    form_name = form_name.strip().replace(" ", "_").lower()  # clean filename

    # Save blank form template
    df.head(0).to_csv(f"data/forms/{form_name}.csv", index=False)

    # --- Send Email with Form Link ---
    if st.button("✉️ Send Form Link"):
        subject = f"Please fill out the form '{form_name}'"
        form_link = f"http://localhost:8501/Form?form={form_name}"  # local link

        body = f"""
Hello,

You've been invited to fill out the form: **{form_name}**

👉 Click here to fill the form: {form_link}

Thank you,
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

# --- Owner can always view responses ---
st.subheader("📊 View All Responses")

response_files = [f for f in os.listdir("data/responses") if f.endswith("_responses.csv")]

if response_files:
    selected = st.selectbox("Select a form to view responses:", response_files)
    df = pd.read_csv(f"data/responses/{selected}")
    st.dataframe(df)
    st.download_button("⬇️ Download CSV", df.to_csv(index=False), file_name=selected)
else:
    st.info("No responses yet.")
