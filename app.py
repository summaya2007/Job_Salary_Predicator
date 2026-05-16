import streamlit as st

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Login UI",
    layout="wide"
)

# =====================================
# SESSION
# =====================================
if "page" not in st.session_state:
    st.session_state.page = "login"

# =====================================
# CSS
# =====================================
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background-color: #c9efff;
}

/* HIDE STREAMLIT */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* MAIN CONTAINER */
.main {
    padding-top: 40px;
}

/* CARD */
.card {
    background: #f8f8f8;
    border-radius: 30px;
    padding: 40px;
    height: 720px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.08);
}

/* TITLE */
.title {
    text-align:center;
    font-size:52px;
    font-weight:bold;
    color:black;
    margin-top:20px;
}

/* SUBTITLE */
.subtitle {
    text-align:center;
    color:gray;
    font-size:20px;
    margin-bottom:30px;
}

/* INPUTS */
.stTextInput input {
    background:transparent;
    border:none;
    border-bottom:2px solid #d1d5db;
    border-radius:0px;
    font-size:18px;
    padding:12px;
}

/* BUTTON */
.stButton>button {
    width:100%;
    height:60px;
    border-radius:40px;
    border:2px solid #555;
    background:white;
    color:black;
    font-size:24px;
    font-weight:bold;
}

.stButton>button:hover {
    background:#b8ebff;
    color:black;
}

/* IMAGE */
.center-img {
    display:flex;
    justify-content:center;
    margin-top:30px;
    margin-bottom:30px;
}

.small-text {
    text-align:center;
    font-size:18px;
    margin-top:20px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# LOGIN PAGE
# =====================================
if st.session_state.page == "login":

    st.markdown('<div class="main">', unsafe_allow_html=True)

    left, right = st.columns(2)

    # LEFT CARD
    with left:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown("""
        <div class="title">Welcome</div>
        <div class="subtitle">Here you log in securely</div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="center-img">
        <img src="https://cdn-icons-png.flaticon.com/512/4140/4140047.png" width="260">
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("")

        password = st.text_input(
            "",
            type="password"
        )

        if st.button("Log In"):

            if username == "admin" and password == "1234":

                st.success("Login Successful")

            else:
                st.error("Invalid Username or Password")

        if st.button("Sign Up"):

            st.session_state.page = "signup"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # RIGHT CARD
    with right:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown("""
        <div class="center-img">
        <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="180">
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="title">Salary Predictor</div>
        <div class="subtitle">
        Predict employee salary using Machine Learning
        </div>
        """, unsafe_allow_html=True)

        st.info("""
Demo Login

Username: admin

Password: 1234
""")

        st.markdown('</div>', unsafe_allow_html=True)

# =====================================
# SIGNUP PAGE
# =====================================
if st.session_state.page == "signup":

    st.markdown('<div class="main">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1.2,1])

    with col2:

        st.markdown('<div class="card">', unsafe_allow_html=True)

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

        if st.button("Sign Up"):

            st.success("Account Created Successfully")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Back to Login"):

            st.session_state.page = "login"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
