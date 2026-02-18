import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib
import os
from datetime import datetime

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="AlphaCare Insurance Risk Analytics",
    layout="wide"
)

st.title("🚗 AlphaCare Insurance Risk Analytics Dashboard")
st.markdown(
    "End-to-end risk-based pricing using **Machine Learning** "
    "(Classification + Regression)."
)

# -------------------------------
# PATH HANDLING
# -------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_DIR = os.path.join(PROJECT_ROOT, "models")
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "insurance_data_cleaned.parquet")

# -------------------------------
# LOAD MODELS
# -------------------------------
@st.cache_resource
def load_models():
    try:
        clf = joblib.load(os.path.join(MODEL_DIR, "final_claim_classifier_model.joblib"))
        reg = joblib.load(os.path.join(MODEL_DIR, "final_claim_regressor_model.joblib"))
        return clf, reg
    except FileNotFoundError as e:
        st.error(f"❌ Model file not found: {e}")
        return None, None

clf_model, reg_model = load_models()

# -------------------------------
# LOAD DATA (Parquet)
# -------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_parquet(DATA_PATH)
        # Optional: sample if still too large
        if len(df) > 20000:
            df = df.sample(20000, random_state=42)
        return df
    except FileNotFoundError:
        st.error("❌ Parquet file not found. Please convert your CSV first.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Failed to load data: {e}")
        return pd.DataFrame()

df = load_data()
# -------------------------------
# SIDEBAR
# -------------------------------
page = st.sidebar.radio(
    "📌 Navigation",
    ["📊 Data Explorer", "🧪 Hypothesis Testing", "🔮 Predict Risk"]
)
# ======================================================
# DATA EXPLORER
# ======================================================
if page == "📊 Data Explorer" and not df.empty:

    st.header("📊 Portfolio Risk Overview")
    st.write("Data preview:", df.head())
    st.write("Unique provinces:", df["Province"].unique())
    st.write("TotalClaims summary:", df["TotalClaims"].describe())


    # Show quick diagnostics
    st.write("Non‑zero claims count:", (df["TotalClaims"] > 0).sum())
    st.write("Non‑zero premiums count:", (df["AnnualPremium"] > 0).sum())

    col1, col2 = st.columns(2)

    with col1:
        # Only include provinces with non‑zero premiums
        loss_ratio = (
            df[df["AnnualPremium"] > 0]
            .groupby("Province")
            .apply(lambda x: x["TotalClaims"].sum() / (x["AnnualPremium"].sum() + 1e-9))
            .reset_index(name="Loss Ratio")
        )
        fig = px.bar(loss_ratio, x="Province", y="Loss Ratio",
                     title="Loss Ratio by Province")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Focus only on non‑zero claims
        df_nonzero_claims = df[df["TotalClaims"] > 0]
        fig2 = px.histogram(
            df_nonzero_claims,
            x="TotalClaims",
            nbins=40,
            histnorm="percent",   # show % instead of raw counts
            title="Claim Amount Distribution (%)"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 🎯 Key Insight")
    st.info(
        "Large provincial differences justify **risk-based pricing** "
        "instead of flat premiums."
    )

# ======================================================
# HYPOTHESIS TESTING
# ======================================================
elif page == "🧪 Hypothesis Testing":

    st.header("🧪 Statistical Validation")

    st.markdown("""
    | Hypothesis | Result |
    |------------|--------|
    | Province risk differences | **Significant** |
    | Postal code risk differences | **Significant** |
    | Gender risk differences | **Not significant** |
    """)

    st.success(
        "✔ Statistical evidence supports **geographic risk pricing** "
        "and rejects unfair discrimination."
    )

# ======================================================
# PREDICT RISK
# ======================================================
elif page == "🔮 Predict Risk" and not df.empty and clf_model and reg_model:

    st.header("🔮 Predict Policy Risk")

    with st.form("prediction_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            sum_insured = st.number_input("Sum Insured", 0, 1_000_000, 50_000)
            reg_year = st.number_input("Registration Year", 1980, datetime.now().year, 2015)
            excess = st.number_input("Excess Selected", 0, 50_000, 1_000)

        with col2:
            postal_code = st.selectbox("Postal Code", sorted(df["PostalCode"].unique()))
            vehicle_type = st.selectbox("Vehicle Type", df["VehicleType"].unique())
            cover_type = st.selectbox("Cover Type", df["CoverType"].unique())

        with col3:
            gender = st.selectbox("Gender", df["Gender"].unique())

        submitted = st.form_submit_button("🚀 Calculate Risk")

    if submitted:
        input_df = pd.DataFrame([{
            "SumInsured": sum_insured,
            "PostalCode": postal_code,
            "VehicleType": vehicle_type,
            "RegistrationYear": reg_year,
            "ExcessSelected": excess,
            "CoverType": cover_type,
            "Gender": gender
        }])

        try:
            claim_prob = clf_model.predict_proba(input_df)[:, 1][0]
            expected_claim = max(reg_model.predict(input_df)[0], 0)

            raw_risk = claim_prob * expected_claim
            risk_score = np.clip((raw_risk / 10_000) * 100, 0, 100)

            col1, col2, col3 = st.columns(3)
            col1.metric("📉 Claim Probability", f"{claim_prob*100:.2f}%")
            col2.metric("💰 Expected Claim (R)", f"{expected_claim:,.0f}")
            col3.metric("⚠️ Risk Score (0–100)", f"{risk_score:.1f}")

            if risk_score < 20:
                adj, level = "-15%", "🟢 Very Low Risk"
            elif risk_score < 40:
                adj, level = "-5%", "🟢 Low Risk"
            elif risk_score < 60:
                adj, level = "0%", "🟡 Medium Risk"
            elif risk_score < 80:
                adj, level = "+10%", "🟠 High Risk"
            else:
                adj, level = "+25%", "🔴 Very High Risk"

            st.success(f"**Risk Level:** {level}")
            st.info(f"**Suggested Premium Adjustment:** {adj}")
            st.caption("Risk Score = Probability of Claim × Expected Claim Amount")
        except Exception as e:
            st.error(f"Prediction failed: {e}")