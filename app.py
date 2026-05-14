# =========================
# IMPORT LIBRARIES
# =========================
import streamlit as st
import pandas as pd
import pickle
import joblib

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Salary Prediction App",
    page_icon="💼",
    layout="centered"
)

# =========================
# LOAD MODEL FILES
# =========================
model = joblib.load(open("knn_model.pkl", "rb"))
scaler = joblib.load(open("scaler.pkl", "rb"))
columns = joblib.load(open("columns.pkl", "rb"))

# =========================
# HELPER FUNCTION
# =========================
def get_options(prefix):

    values = []

    for col in columns:
        if col.startswith(prefix):
            values.append(col.replace(prefix, ""))

    values = sorted(list(set(values)))

    return ["Other"] + values

# =========================
# GET DROPDOWN OPTIONS
# =========================
job_options = get_options("job_title_")

edu_options = get_options("education_level_")

loc_options = get_options("location_")

industry_options = get_options("industry_")

company_options = get_options("company_size_")

remote_options = get_options("remote_work_")

# =========================
# APP TITLE
# =========================
st.title("💼 Salary Prediction App")

st.write("Predict employee salary using KNN Machine Learning Model")

# =========================
# USER INPUTS
# =========================
experience = st.number_input(
    "Experience (Years)",
    min_value=0,
    max_value=40,
    value=1
)

skills = st.number_input(
    "Skills Count",
    min_value=0,
    max_value=50,
    value=5
)

certifications = st.number_input(
    "Certifications",
    min_value=0,
    max_value=20,
    value=1
)

job = st.selectbox(
    "Job Title",
    job_options
)

education = st.selectbox(
    "Education Level",
    edu_options
)

location = st.selectbox(
    "Location",
    loc_options
)

industry = st.selectbox(
    "Industry",
    industry_options
)

company = st.selectbox(
    "Company Size",
    company_options
)

remote = st.selectbox(
    "Remote Work",
    remote_options
)

# =========================
# PREDICT BUTTON
# =========================
if st.button("Predict Salary"):

    # =========================
    # CREATE INPUT DATAFRAME
    # =========================
    input_data = pd.DataFrame({
        "experience_years": [experience],
        "skills_count": [skills],
        "certifications": [certifications],
        "job_title": [job],
        "education_level": [education],
        "location": [location],
        "industry": [industry],
        "company_size": [company],
        "remote_work": [remote]
    })

    # =========================
    # FEATURE ENGINEERING
    # =========================
    input_data["exp_squared"] = (
        input_data["experience_years"] ** 2
    )

    input_data["skill_per_exp"] = (
        input_data["skills_count"] /
        (input_data["experience_years"] + 1)
    )

    input_data["cert_per_skill"] = (
        input_data["certifications"] /
        (input_data["skills_count"] + 1)
    )

    # =========================
    # SENIORITY
    # =========================
    input_data["seniority"] = pd.cut(
        input_data["experience_years"],
        bins=[0, 2, 5, 10, 20, 40],
        labels=[
            "Fresher",
            "Junior",
            "Mid",
            "Senior",
            "Expert"
        ]
    )

    # =========================
    # ONE HOT ENCODING
    # =========================
    input_data = pd.get_dummies(input_data)
    

   # Save with compression
   joblib.dump(model, "salary_prediction_model.pkl", compress=3
    joblib.dump(model, "salary_prediction_model.pkl", compress=9)

    # =========================
    # ALIGN COLUMNS
    # =========================
    input_data = input_data.reindex(
        columns=columns,
        fill_value=0
    )

    # =========================
    # SCALE DATA
    # =========================
    input_scaled = scaler.transform(input_data)

    # =========================
    # PREDICTION
    # =========================
    prediction = model.predict(input_scaled)

    predicted_salary = int(prediction[0])

    # =========================
    # OUTPUT
    # =========================
    st.success(
        f"💰 Predicted Salary: ₹ {predicted_salary:,}"
    )

    st.balloons()