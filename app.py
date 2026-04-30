import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import joblib
import shap
import os
from sklearn.ensemble import RandomForestClassifier

# ---------------- DATABASE ----------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT
)
""")
conn.commit()

def add_user(username, password):
    c.execute("INSERT INTO users VALUES (?,?)", (username, password))
    conn.commit()

def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone()

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- AUTH ----------------
if not st.session_state.logged_in:
    st.title("🔐 Student Login System")

    choice = st.sidebar.selectbox("Menu", ["Login", "Register"])

    if choice == "Register":
        st.subheader("Create Account")
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")

        if st.button("Register"):
            try:
                add_user(new_user, new_pass)
                st.success("Account created!")
            except:
                st.error("User already exists")

    elif choice == "Login":
        st.subheader("Login")
        user = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_user(user, password):
                st.session_state.logged_in = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

    st.stop()

# ---------------- LOAD DATA ----------------
DATA_PATH = "data/students.csv.zip"

if not os.path.exists(DATA_PATH):
    st.error("Dataset not found! Please add Kaggle dataset to data/students.csv")
    st.stop()

df = pd.read_csv(DATA_PATH)

# Clean column names
df.columns = df.columns.str.replace(" ", "_")

# Feature engineering
df["total_score"] = df["math_score"] + df["reading_score"] + df["writing_score"]
df["pass"] = df["total_score"].apply(lambda x: 1 if x >= 150 else 0)

# ---------------- MODEL ----------------
model_path = "model.pkl"

if not os.path.exists(model_path):
    X = df.drop(["pass", "total_score"], axis=1)
    X = pd.get_dummies(X)
    y = df["pass"]

    model = RandomForestClassifier()
    model.fit(X, y)

    joblib.dump((model, X.columns), model_path)

model, columns = joblib.load(model_path)

# ---------------- UI ----------------
st.title("🎓 Student Performance Predictor (Kaggle Data)")

menu = st.sidebar.selectbox("Navigation", ["Home", "Charts", "Predict", "Batch Upload"])

# ---------------- HOME ----------------
if menu == "Home":
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

# ---------------- CHARTS ----------------
elif menu == "Charts":
    st.subheader("📊 Visualizations")

    st.bar_chart(df.groupby("gender")["total_score"].mean())
    st.bar_chart(df.groupby("parental_level_of_education")["total_score"].mean())
    st.line_chart(df["math_score"])

# ---------------- PREDICT ----------------
elif menu == "Predict":
    st.subheader("🎯 Predict Student Performance")

    gender = st.selectbox("Gender", ["male", "female"])
    race = st.selectbox("Race", ["group A","group B","group C","group D","group E"])
    education = st.selectbox("Parental Education", [
        "some high school","high school","some college",
        "associate's degree","bachelor's degree","master's degree"
    ])
    lunch = st.selectbox("Lunch", ["standard","free/reduced"])
    prep = st.selectbox("Test Preparation Course", ["none","completed"])

    math = st.slider("Math Score", 0, 100)
    reading = st.slider("Reading Score", 0, 100)
    writing = st.slider("Writing Score", 0, 100)

    if st.button("Predict"):
        input_df = pd.DataFrame([{
            "gender": gender,
            "race/ethnicity": race,
            "parental_level_of_education": education,
            "lunch": lunch,
            "test_preparation_course": prep,
            "math_score": math,
            "reading_score": reading,
            "writing_score": writing
        }])

        input_df.columns = input_df.columns.str.replace(" ", "_")

        input_df = pd.get_dummies(input_df)
        input_df = input_df.reindex(columns=columns, fill_value=0)

        prediction = model.predict(input_df)[0]
        prob = model.predict_proba(input_df)[0][1]

        st.write(f"Prediction: {'PASS' if prediction else 'FAIL'}")
        st.write(f"Confidence: {prob:.2f}")

        # SHAP
        st.subheader("🔍 SHAP Explanation")
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(input_df)

        shap_df = pd.DataFrame({
            "Feature": input_df.columns,
            "Impact": shap_values[1][0]
        }).sort_values(by="Impact", key=abs, ascending=False)

        st.bar_chart(shap_df.set_index("Feature"))

# ---------------- BATCH UPLOAD ----------------
elif menu == "Batch Upload":
    st.subheader("📂 Upload CSV")

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        data = pd.read_csv(file)
        data.columns = data.columns.str.replace(" ", "_")

        data_processed = pd.get_dummies(data)
        data_processed = data_processed.reindex(columns=columns, fill_value=0)

        preds = model.predict(data_processed)
        probs = model.predict_proba(data_processed)[:, 1]

        data["Prediction"] = preds
        data["Confidence"] = probs

        st.write(data)

        csv = data.to_csv(index=False).encode("utf-8")
        st.download_button("Download Results", csv, "results.csv")

# ---------------- LOGOUT ----------------
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()