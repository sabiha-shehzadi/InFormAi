import streamlit as st

st.set_page_config(page_title="Smart Form Automation", layout="wide")

# --- Sidebar Login ---
st.sidebar.header("🔐 Login")
user_email = st.sidebar.text_input("Enter your email address")
login_btn = st.sidebar.button("Login")

# --- Session management ---
if "user_role" not in st.session_state:
    st.session_state.user_role = None

# --- Authentication Logic ---
if login_btn:
    if user_email.strip().lower() == "owner@gmail.com":  # 👈 replace this with your real owner email
        st.session_state.user_role = "owner"
        st.sidebar.success("Welcome, Owner!")
    else:
        st.session_state.user_role = "colleague"
        st.sidebar.info("Welcome, Colleague!")

# --- App Title ---
st.title("📄 Smart Form Automation")

# --- Role-based Pages ---
if st.session_state.user_role == "owner":
    st.markdown("### 👤 You are logged in as the **Owner**.")
    st.write("Go to the **Owner Dashboard** in the sidebar to create and send forms.")

elif st.session_state.user_role == "colleague":
    st.markdown("### 🧑‍💼 You are logged in as a **Colleague**.")
    st.write("Go to the **Form** page to fill out your assigned forms.")

else:
    st.info("👋 Please log in from the sidebar to continue.")
