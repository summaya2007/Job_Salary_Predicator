import streamlit as st
import pandas as pd
import joblib

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Salary Predictor",
    page_icon="💼",
    layout="wide"
)

# ==================================================
# SESSION STATE
# ==================================================
if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ==================================================
# LOGIN DETAILS
# ==================================================
USERNAME = "admin"
PASSWORD = "1234"

# ==================================================
# CSS
# ==================================================
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background-color: #cfefff;
}

/* HIDE STREAMLIT */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* REMOVE TOP SPACE */
.block-container {
    padding-top: 1rem;
}

/* CARD */
.card {
    background: #f8f8f8;
    border-radius: 35px;
    padding: 45px;
    min-height: 720px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.08);
}

/* TITLE */
.title {
    text-align: center;
    font-size: 52px;
    font-weight: bold;
    color: black;
    margin-top: 10px;
}

/* SUBTITLE */
.subtitle {
    text-align: center;
    color: gray;
    font-size: 20px;
    margin-bottom: 25px;
}

/* IMAGE */
.center-img {
    display: flex;
    justify-content: center;
    margin-top: 20px;
    margin-bottom: 30px;
}

/* INPUT */
.stTextInput input,
.stNumberInput input {
    background: transparent;
    border: none;
    border-bottom: 2px solid #cfcfcf;
    border-radius: 0px;
    font-size: 18px;
    padding: 12px;
}

/* SELECTBOX */
.stSelectbox div[data-baseweb="select"] {
    border-radius: 15px;
}

/* BUTTON */
.stButton > button {
    width: 100%;
    height: 58px;
    border-radius: 40px;
    border: 2px solid #555;
    background: white;
    color: black;
    font-size: 22px;
    font-weight: bold;
    transition: 0.3s;
}

/* BUTTON HOVER */
.stButton > button:hover {
    background: #bdeaff;
    color: black;
    border: 2px solid #7bd3ff;
}

/* RESULT */
.result-box {
    background: #bdeaff;
    padding: 25px;
    border-radius: 25px;
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    margin-top: 30px;
}

/* SMALL TEXT */
.small-text {
    text-align: center;
    margin-top: 20px;
    font-size: 18px;
}

/* LOGIN BOX */
.login-info {
    background: #dff5ff;
    padding: 20px;
    border-radius: 20px;
    margin-top: 30px;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# LOGIN PAGE
# ==================================================
if not st.session_state.logged_in:

    col1, col2 = st.columns(2)

    # ==============================================
    # LEFT CARD
    # ==============================================
    with col1:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown("""
        <div class="title">Welcome</div>
        <div class="subtitle">Here you log in securely</div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="center-img">
        <img src="https://cdn-icons-png.flaticon.com/512/4140/4140048.png"
        width="250">
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Log In"):

            if username == USERNAME and password == PASSWORD:

                st.session_state.logged_in = True
                st.rerun()

            else:
                st.error("Invalid Username or Password")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Sign Up"):

            st.session_state.page = "signup"

        st.markdown('</div>', unsafe_allow_html=True)

    # ==============================================
    # RIGHT CARD
    # ==============================================
    with col2:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown("""
        <div class="center-img">
        <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
        width="180">
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="title">Salary Predictor</div>
        <div class="subtitle">
        Predict employee salary using Machine Learning
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="login-info">
        <b>Demo Login Credentials</b><br><br>

        Username: <b>admin</b><br>
        Password: <b>1234</b>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ==================================================
# SIGNUP PAGE
# ==================================================
if st.session_state.page == "signup" and not st.session_state.logged_in:

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,1.2,1])

    with c2:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown("""
        <div class="center-img">
        <img src="https://cdn-icons-png.flaticon.com/512/747/747376.png"
        width="160">
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="title">Sign Up</div>
        <div class="subtitle">
        Create an account, It's free
        </div>
        """, unsafe_allow_html=True)

        st.text_input("Email")

        st.text_input(
            "Password",
            type="password"
        )

        st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button("Create Account"):

            st.success("Account Created Successfully")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Back to Login"):

            st.session_state.page = "login"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# ==================================================
# MAIN APP
# ==================================================
if st.session_state.logged_in:

    st.title("💼 Salary Prediction App")

    st.write("Predict employee salary using Machine Learning")

    # LOAD MODEL
    model = joblib.load("salary_prediction_model.pkl")
    scaler = joblib.load("scaler.pkl")
    columns = joblib.load("model_features.pkl")

    # INPUTS
    experience = st.number_input(
        "Experience (Years)",
        0, 50, 1
    )

    skills = st.number_input(
        "Skills Count",
        0, 50, 5
    )

    certifications = st.number_input(
        "Certifications",
        0, 20, 1
    )

    job_title = st.selectbox(
        "Job Title",
        [
            "Data Scientist",
            "Software Engineer",
            "Manager",
            "Other"
        ]
    )

    education = st.selectbox(
        "Education Level",
        [
            "Bachelor",
            "Master",
            "PhD",
            "Other"
        ]
    )

    location = st.selectbox(
        "Location",
        [
            "Bangalore",
            "Delhi",
            "Mumbai",
            "Other"
        ]
    )

    # PREDICT BUTTON
    if st.button("Predict Salary"):

        input_data = pd.DataFrame({
            "Experience": [experience],
            "Skills": [skills],
            "Certifications": [certifications],
            "Job_Title": [job_title],
            "Education_Level": [education],
            "Location": [location]
        })

        input_data = pd.get_dummies(input_data)

        input_data = input_data.reindex(
            columns=columns,
            fill_value=0
        )

        input_scaled = scaler.transform(input_data)

        prediction = model.predict(input_scaled)

        st.markdown(
            f'''
            <div class="result-box">
            💰 Predicted Salary <br><br>
            ₹ {round(prediction[0],2)}
            </div>
            ''',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()
