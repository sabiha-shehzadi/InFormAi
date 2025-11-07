import streamlit as st
import pandas as pd
import os

st.title("📝 Fill Out the Form")

# --- Read form name from URL query ---
query_params = st.query_params
form_name = query_params.get("form", [None])[0]

if not form_name:
    st.error("Form not found or expired. Contact the owner.")
    st.stop()

form_name = form_name.strip().replace(" ", "_").lower()
template_path = f"data/forms/{form_name}.csv"

# --- Check if the form exists ---
if not os.path.exists(template_path):
    st.error("Form not found or expired. Contact the owner.")
    st.stop()

# --- Load blank template ---
df = pd.read_csv(template_path)
responses = {}

# --- Dynamically generate form inputs ---
st.subheader(f"📋 Form: {form_name}")
for col in df.columns:
    responses[col] = st.text_input(f"{col}")

# --- On Submit, save to responses ---
if st.button("✅ Submit"):
    os.makedirs("data/responses", exist_ok=True)
    response_file = f"data/responses/{form_name}_responses.csv"

    new_data = pd.DataFrame([responses])

    if os.path.exists(response_file):
        existing = pd.read_csv(response_file)
        final_df = pd.concat([existing, new_data], ignore_index=True)
    else:
        final_df = new_data

    final_df.to_csv(response_file, index=False)
    st.success("🎉 Your response has been submitted!")
