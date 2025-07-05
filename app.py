import streamlit as st
import joblib
import numpy as np

# ---- Load model and feature names ----
@st.cache_resource
def load_model():
    model = joblib.load('wine_model.pkl')
    features = joblib.load('feature_names.pkl')
    return model, features

model, feature_names = load_model()

# ---- UI Header ----
st.set_page_config(page_title="Wine Quality Predictor", page_icon="🍷", layout="centered")
st.title("🍷 Wine Quality Predictor")
st.markdown(
    """
    Input the chemical properties of a red wine sample below to predict if it meets premium quality standards.
    A model trained on real winery data will instantly classify the wine as **Good** (quality ≥ 7) or **Not Good**.
    """
)

# ---- User Input Section ----
st.header("Wine Sample Chemical Attributes")

input_values = []
with st.form("input_form"):
    cols = st.columns(2)
    for idx, feature in enumerate(feature_names):
        with cols[idx % 2]:
            value = st.number_input(
                f"{feature.replace('_', ' ').capitalize()}",
                min_value=0.0,
                max_value=100.0,
                step=0.01,
                format="%.3f",
                key=feature
            )
            input_values.append(value)
    submitted = st.form_submit_button("Predict Quality", type="primary")

# ---- Prediction ----
if submitted:
    # Reshape input for prediction
    sample = np.array(input_values).reshape(1, -1)
    pred = model.predict(sample)[0]
    prob = model.predict_proba(sample)[0][1]  # Probability of 'Good'
    label = "🌟 Good Quality (7+)" if pred == 1 else "❌ Not Good (<7)"
    color = "#e0ffe0" if pred == 1 else "#ffe0e0"
    st.markdown(
        f"""
        <div style="background-color:{color};padding:1.2em 1em;border-radius:10px;text-align:center;">
        <span style="font-size:1.5em;"><b>{label}</b></span><br>
        <span style="font-size:1.1em;">Confidence: {prob:.2%}</span>
        </div>
        """, unsafe_allow_html=True
    )

    st.info("You can adjust the sliders and predict again for different samples.")

st.markdown("---")
st.markdown(
    """
    <div style='text-align:center; font-size:0.9em; color:gray;'>
    Created by Paul Tristan Dujali. Powered by Streamlit.<br>
    <a href="https://github.com/hirocenzo/sms-spam-detector" target="_blank">View on GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)