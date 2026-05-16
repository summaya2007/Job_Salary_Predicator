import streamlit as st
import pandas as pd
import os
import hashlib
import joblib

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Salary Prediction App",
    page_icon="💼",
    layout="centered"
)

# =====================================
# CUSTOM CSS
# =====================================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #141e30, #243b55);
}

.main-box {
    background-color: white;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0px 0px 20px rgba(0,0,0,0.3);
}

.title {
    text-align: center;
    color: #243b55;
    font-size: 40px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 20px;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    background-color: #243b55;
    color: white;
    font-size: 18px;
    border: none;
}

.stButton>button:hover {
    background-color: #141e30;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# USER FILE
# =====================================
USER_FILE = "users.csv"

if not os.path.exists(USER_FILE):
    df = pd.DataFrame(columns=["username", "password"])
    df.to_csv(USER_FILE, index=False)

# =====================================
# HASH PASSWORD
# =====================================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =====================================
# LOAD USERS
# =====================================
def load_users():
    return pd.read_csv(USER_FILE)

# =====================================
# SAVE USERS
# =====================================
def save_user(username, password):

    users = load_users()

    new_user = pd.DataFrame({
        "username": [username],
        "password": [hash_password(password)]
    })

    users = pd.concat([users, new_user], ignore_index=True)

    users.to_csv(USER_FILE, index=False)

# =====================================
# LOGIN CHECK
# =====================================
def login_user(username, password):

    users = load_users()

    hashed = hash_password(password)

    result = users[
        (users["username"] == username) &
        (users["password"] == hashed)
    ]

    return not result.empty

# =====================================
# SESSION STATE
# =====================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =====================================
# SIDEBAR
# =====================================
menu = ["Login", "Signup"]

choice = st.sidebar.selectbox("Select Option", menu)

# =====================================
# LOGIN PAGE
# =====================================
if choice == "Login" and not st.session_state.logged_in:

    st.markdown('<div class="main-box">', unsafe_allow_html=True)

    st.markdown(
        '<div class="title">💼 Salary Predictor</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Login to continue</div>',
        unsafe_allow_html=True
    )

    username = st.text_input("👤 Username")

    password = st.text_input(
        "🔒 Password",
        type="password"
    )

    if st.button("Login"):

        if login_user(username, password):

            st.session_state.logged_in = True
            st.success("Login Successful")
            st.rerun()

        else:
            st.error("Invalid Username or Password")

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================
# SIGNUP PAGE
# =====================================
elif choice == "Signup" and not st.session_state.logged_in:

    st.markdown('<div class="main-box">', unsafe_allow_html=True)

    st.markdown(
        '<div class="title">📝 Create Account</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Signup to use the app</div>',
        unsafe_allow_html=True
    )

    new_user = st.text_input("👤 Create Username")

    new_password = st.text_input(
        "🔒 Create Password",
        type="password"
    )

    if st.button("Signup"):

        users = load_users()

        if new_user in users["username"].values:
            st.error("Username already exists")

        elif new_user == "" or new_password == "":
            st.warning("Please fill all fields")

        else:
            save_user(new_user, new_password)
            st.success("Account Created Successfully")

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================
# MAIN APP
# =====================================
if st.session_state.logged_in:

    st.title("💼 Salary Prediction App")

    st.write("Predict employee salary using ML model")

    # LOAD FILES
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
        ["Data Scientist", "Software Engineer", "Manager", "Other"]
    )

    education = st.selectbox(
        "Education Level",
        ["Bachelor", "Master", "PhD", "Other"]
    )

    location = st.selectbox(
        "Location",
        ["Bangalore", "Delhi", "Mumbai", "Other"]
    )

    # PREDICT
    if st.button("Predict Salary"):

        input_data = pd.DataFrame({
            "Experience": [experience],
            "Skills": [skills],
            "Certifications": [certifications],
            "Job_Title": [job_title],
            "Education_Level": [education],
            "Location": [location]
        })

        # ENCODING
        input_data = pd.get_dummies(input_data)

        # ALIGN COLUMNS
        input_data = input_data.reindex(
            columns=columns,
            fill_value=0
        )

        # SCALE
        input_scaled = scaler.transform(input_data)

        # PREDICT
        prediction = model.predict(input_scaled)

        st.success(
            f"💰 Predicted Salary: ₹ {round(prediction[0], 2)}"
        )

    # LOGOUT
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
