import streamlit as st
import os

# --- Streamlit Page Config ---
st.set_page_config(page_title="Smart Form Automation", layout="wide")

# --- Define Owner Email ---
OWNER_EMAIL = "owner@gmail.com"  # 👈 replace this with your real owner email

# --- Sidebar Login ---
st.sidebar.header("🔐 Login")
user_email = st.sidebar.text_input("Enter your email address")
login_btn = st.sidebar.button("Login")

# --- Session Management ---
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# --- Authentication Logic ---
if login_btn:
    if user_email.strip().lower() == OWNER_EMAIL:
        st.session_state.user_role = "owner"
        st.session_state.user_email = user_email.strip().lower()
        st.sidebar.success("✅ Welcome, Owner!")
    else:
        st.session_state.user_role = "colleague"
        st.session_state.user_email = user_email.strip().lower()
        st.sidebar.info("👋 Welcome, Colleague!")

# --- Main Title ---
st.title("📄 Smart Form Automation")

# --- Role Based Content ---
if st.session_state.user_role == "owner":
    st.markdown("### 👤 You are logged in as the **Owner**.")
    st.write("Use the sidebar to open the **Owner Dashboard** to upload files, send form links, and see responses.")
    st.info("📩 When you send a form, your colleagues will only see the form—not this dashboard.")

elif st.session_state.user_role == "colleague":
    st.markdown("### 🧑‍💼 You are logged in as a **Colleague**.")
    st.write("If you received a link from your owner, go directly to that link to fill out the form.")
    st.info("⚙️ You don’t have access to the owner dashboard or responses — only the form link sent to you.")

else:
    st.info("👋 Please log in from the sidebar to continue.")


# --- Safety check: Ensure folders exist ---
os.makedirs("data/forms", exist_ok=True)
os.makedirs("data/responses", exist_ok=True)
