"""
app_final.py
קובץ זה מהווה את הדשבורד (ממשק המשתמש) עבור graduation_project2.
הוא מאפשר למשתמשים להירשם, להתחבר, לאמן מודלים (חלק 1) ולהריץ את חלק 2.
"""
# app_final.py
import streamlit as st
import pandas as pd
import requests
from part1.train_model import train_model_from_csv


API_URL = "http://127.0.0.1:8000"

st.title("🎓 Graduation Project Dashboard")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.token = None

if "users" not in st.session_state:
    st.session_state.users = {}

if not st.session_state.logged_in:
    """
    פה מתבצע התחברות או הרשמה למערכת.
    """
    mode = st.radio("Choose action", ["Login", "Register"])

    if mode == "Register":
        st.subheader("Register new user")
        new_user = st.text_input("Username", key="reg_user")
        new_pass = st.text_input("Password", type="password", key="reg_pass")
        if st.button("Register"):
            if new_user in st.session_state.users:
                st.error("Username already exists")
            else:
                st.session_state.users[new_user] = new_pass
                st.success(f"User {new_user} registered successfully")

    elif mode == "Login":
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.logged_in = True
                st.session_state.token = username
                st.success(f"Logged in as {username}")
            else:
                st.error("Invalid username or password")

else:
    """
    חלק 1: אימון מודל.
    המשתמש מעלה קובץ CSV, בוחר את עמודת היעד, ומאמן מודל ML.
    """
    st.subheader("Part 1: Model Training")
    uploaded_file = st.file_uploader("Upload CSV for training", type="csv")
    target_col = st.text_input("Target column", value="price")
    model_name = st.text_input("Model name", value="linear_model")
    model_type = st.selectbox("Model type", ["linear", "random_forest", "gradient_boost"])

    if st.button("Train Model") and uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Columns in CSV:", df.columns.tolist())

        target_col_name = target_col

        feature_cols = [col for col in df.columns if col != target_col_name]

        if not feature_cols:
            st.error("No feature columns found. CSV must contain columns other than the target.")
        else:
            column_types = {}
            metadata, model_path, metadata_path = train_model_from_csv(
                df, feature_cols, target_col_name, model_type, model_name, {}, column_types
            )
            st.success(f"Model trained successfully: {metadata['model_name']}")
            st.json(metadata)




    if st.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()
