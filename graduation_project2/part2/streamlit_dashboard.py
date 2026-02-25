"""
הקוד יוצר ממשק משתמש עם Streamlit שמתקשר עם שרת FastAPI כדי לנהל משתמשים וטוקנים
 במילים אחרות הקוד מגדיר את מה שהמשתמש רואה ומסוגל לעשות
לפני התחברות, המשתמש רואה מסך שבו אפשר לבחור אם להתחבר או להירשם ומזין שם משתמש וסיסמה
אחרי התחברות המשתמש רואה כמה הטוקנים שברשותו
הוא את רואה כפתורים לפעולות כמו אימון מודל ביצוע חיזוי קניית טוקנים ויציאה מהמערכת
"""


import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="Tokens Dashboard", page_icon="🪙")
st.title("🪙 Tokens Dashboard")

if "token" not in st.session_state:
    st.session_state.token = None


def safe_api_call(method, endpoint, **kwargs):
    try:
        response = method(f"{API}{endpoint}", **kwargs)
        try:
            return response.status_code, response.json()
        except:
            return response.status_code, {"detail": response.text}
    except requests.exceptions.ConnectionError:
        return 0, {"detail": "Connection failed. Is the server running?"}


if not st.session_state.token:
    choice = st.radio("Choose action", ["Login", "Sign Up"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Sign Up":
        if st.button("Sign Up"):
            status, data = safe_api_call(requests.post, "/signup", json={"username": username, "password": password})
            if status == 200:
                st.success("User registered successfully! Now you can login.")
            else:
                st.error(f"Error {status}: {data.get('detail', 'Unknown error')}")

    elif choice == "Login":
        if st.button("Login"):
            status, data = safe_api_call(requests.post, "/login", json={"username": username, "password": password})
            if status == 200:
                st.session_state.token = data.get("access_token")
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error(f"Error {status}: {data.get('detail', 'Invalid credentials')}")

else:
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    st.subheader("Welcome! You are logged in.")

    if st.button("Show tokens"):
        status, data = safe_api_call(requests.get, "/tokens", headers=headers)
        st.write(data)

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Train (1 token)"):
            status, data = safe_api_call(requests.post, "/train", headers=headers)
            if status == 200: st.success("Success!")
            st.write(data)

    with col2:
        if st.button("Predict (5 tokens)"):
            status, data = safe_api_call(requests.post, "/predict", headers=headers)
            if status == 200: st.success("Success!")
            st.write(data)

    with col3:
        if st.button("Buy 5 tokens"):
            status, data = safe_api_call(requests.post, "/add_tokens", headers=headers, json={"amount": 5})
            if status == 200: st.success("Added!")
            st.write(data)

    if st.button("Logout"):
        st.session_state.token = None
        st.rerun()