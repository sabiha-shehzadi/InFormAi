import streamlit as st

st.set_page_config(page_title="Smart Form Automation", layout="wide")

# Simple login simulation (no backend yet)
st.sidebar.header("🔐 Login")
user_email = st.sidebar.text_input("Enter your email address")
login_btn = st.sidebar.button("Login")

if "user_role" not in st.session_state:
    st.session_state.user_role = None

if login_btn:
    if user_email.strip().lower() == "owner@gmail.com":  # replace with your real owner email
        st.session_state.user_role = "owner"
        st.sidebar.success("Welcome, Owner!")
    else:
        st.session_state.user_role = "colleague"
        st.sidebar.info("Welcome, Colleague!")

st.title("📄 Smart Form Automation")

# Role-based display
if st.session_state.user_role == "owner":
    st.markdown("### 👤 You are logged in as the **Owner**.")
    st.write("Use the sidebar to select **Owner Dashboard** to create forms and view responses.")

elif st.session_state.user_role == "colleague":
    st.markdown("### 🧑‍💼 You are logged in as a **Colleague**.")
    st.write("Use the sidebar to open the **Form** page and submit your responses.")

else:
    st.info("👋 Please log in from the sidebar to continue.")
