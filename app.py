import streamlit as st
from datetime import datetime
from auth import authenticate, register_user, reset_password
from data_store import load_records, save_record
from model import predict_stress

st.set_page_config("Student Stress System", layout="centered")

# SESSION
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.email = ""
    st.session_state.name = ""

st.title("🧠 Student Mental Stress Assessment System")

# ---------------- LOGIN / REGISTER / FORGOT ----------------
if not st.session_state.logged_in:

    tab1, tab2, tab3 = st.tabs(["Login", "Register", "Forgot Password"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            role, name = authenticate(email, password)
            if role:
                st.session_state.logged_in = True
                st.session_state.role = role
                st.session_state.email = email
                st.session_state.name = name
            else:
                st.error("Invalid credentials")

    with tab2:
        name = st.text_input("Full Name")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_pass")

        if st.button("Register"):
            if register_user(name, email, password):
                st.success("Registered successfully. Login now.")
            else:
                st.error("Email already exists")

    with tab3:
        email = st.text_input("Registered Email")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Reset Password"):
            if reset_password(email, new_pass):
                st.success("Password updated. Login now.")
            else:
                st.error("Email not found")

    st.stop()

# ---------------- LOGOUT ----------------
if st.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.stop()

# ================= STUDENT =================
if st.session_state.role == "student":

    st.subheader(f"👤 Welcome {st.session_state.name}")

    age = st.number_input("Age", 15, 30)
    study = st.slider("Study Hours", 0, 12, 6)
    sleep = st.slider("Sleep Hours", 0, 12, 7)
    screen = st.slider("Screen Time", 0, 12, 6)
    activity = st.selectbox("Physical Activity", ["Yes", "No"])
    pressure = st.slider("Academic Pressure", 1, 5, 3)
    quality = st.slider("Sleep Quality", 1, 5, 3)

    if st.button("Assess Stress"):
        pred = predict_stress([
            study, sleep, screen,
            1 if activity == "Yes" else 0,
            pressure, quality
        ])

        levels = {0: "Low", 1: "Moderate", 2: "High"}
        scores = {"Low": 1, "Moderate": 2, "High": 3}
        stress = levels[pred]

        st.success(f"Stress Level: {stress}")

        save_record({
            "Timestamp": datetime.now(),
            "Name": st.session_state.name,
            "Email": st.session_state.email,
            "Age": age,
            "Study_Hours": study,
            "Sleep_Hours": sleep,
            "Screen_Time": screen,
            "Physical_Activity": activity,
            "Academic_Pressure": pressure,
            "Sleep_Quality": quality,
            "Stress_Level": stress,
            "Stress_Score": scores[stress]
        })

    df = load_records()
    df = df[df["Email"] == st.session_state.email]

    if not df.empty:
        st.subheader("📈 Your Stress Trend")
        st.line_chart(df.sort_values("Timestamp").set_index("Timestamp")["Stress_Score"])

# ================= ADMIN =================
if st.session_state.role == "admin":

    st.subheader("👑 Admin Dashboard")

    df = load_records()
    st.dataframe(df, use_container_width=True)

    if not df.empty:
        st.subheader("📊 Overall Stress Analysis")
        st.bar_chart(df["Stress_Score"].value_counts())
        st.line_chart(df.groupby("Timestamp")["Stress_Score"].mean())

        st.download_button(
            "⬇️ Download All Data",
            df.to_csv(index=False).encode("utf-8"),
            "student_records.csv",
            "text/csv"
        )
