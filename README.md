# Insurance Risk Analytics & Predictive Modeling

[![Continuous Integration](https://github.com/Avicci-b/Insurance-risk-analytics/actions/workflows/ci.yml/badge.svg)](https://github.com/Avicci-b/Insurance-risk-analytics/actions/workflows/ci.yml)

## Business Problem

AlphaCare Insurance Solutions (ACIS) wants to identify low‑risk customer segments to offer competitive premiums and attract new clients, while maintaining overall profitability. Currently, pricing is uniform across regions, leading to missed opportunities (e.g., Gauteng has 122.2% loss ratio, Northern Cape only 28.3%). This project aims to:

- Uncover risk drivers using historical claim data.
- Build predictive models to assess individual policy risk.
- Provide data‑backed recommendations for premium adjustments.

## Solution Overview

We analyzed **1,000,098 policies** from Feb 2014 – Aug 2015 using a four‑phase approach:

1. **EDA** – Corrected a critical data misinterpretation (monthly vs annual premiums) and identified large geographic disparities.
2. **Data Version Control** – Implemented DVC to ensure reproducibility and audit compliance.
3. **Hypothesis Testing** – Statistically validated that risk varies by province and zip code (p < 0.001) but not by gender (p > 0.45).
4. **Predictive Modeling** – Built a two‑stage model (classification + regression) achieving **80.84% recall** for claim detection and created a risk scoring system (0–100) to guide pricing.

## Key Results

| Metric | Value |
|--------|-------|
| **Corrected loss ratio** | 8.7% (was 104.77% before correction) |
| **Geographic profitability gap** | 93.9% between Gauteng and Northern Cape |
| **Claim detection recall** | 80.84% (Logistic Regression) |
| **Risk‑based premium range** | -15% to +25% adjustment |
| **Statistical confidence (geography)** | p < 0.001 (99.9% confidence) |

## Quick Start

bash
git clone https://github.com/Avicci-b/Insurance-risk-analytics
cd insurance-risk-analytics
pip install -r requirements.txt
# Pull data with DVC 
dvc pull
# Run the interactive dashboard
streamlit run app.pydvc pull
# Run the interactive dashboard
streamlit run app.py

## Project strucutre
Insurance-risk-analytics/
├── .github/workflows/        # CI/CD pipeline
├──.dvc
├── data/                     # Data (DVC‑tracked)
├── notebooks/  
├──scripts/              # Original analysis notebooks
├── src/             # Dataclasses, constants
├── tests/                    # Unit tests
├── dashboard/                   # Streamlit dashboard
├── requirements.txt
├── README.
├──params.yaml
├──dvc.yaml
├──dvc.lock
├──reports/
├──models/
├──.dvcignore
└── .gitignore
## Technical Details
# Data
- Source: ACIS historical claims (Feb 2014 – Aug 2015)
- Size: 1,000,098 policies, 49 original columns
- Preprocessing:
     - Corrected premium scaling (×12)
     - Selected 15 features based on EDA and hypothesis tests
     - Ordinal encoding for high‑cardinality categoricals

# Models

- Classification (Logistic Regression) – predicts TotalClaims with 80.84% recall.
- Regression (Linear Regression) – predicts TotalClaims amount (R² = 0.30).
- Risk Score = Probability × Expected Amount, scaled 0‑100.

# Evaluation
- Classification metrics: accuracy, precision, recall, F1, ROC‑AUC.
- Regression metrics: R², RMSE, MAE.
- Cross‑validation on 500K sample due to memory constraints.

# Future Improvements

- Incorporate telematics and credit score data.
- Retrain models quarterly with new data.
- Implement A/B testing for premium adjustments.
- Add SHAP explanations directly in the dashboard.

Author
Biniyam Mitiku 
Data Analytics Engineer

This project was completed as part of the KAIM Academy Insurance Risk Analytics Challenge.

text

### Blog Post / Technical Report Outline

**Title:** *How We Turned Insurance Data into a 125% Pricing Opportunity*

**1. Introduction**
- Briefly introduce ACIS and the business challenge.
- Why insurance analytics matters.

**2. The Data Surprise**
- The premium misinterpretation story.
- Impact of the correction.

**3. Exploratory Analysis**
- Key visualizations (loss ratio by province, claim distribution).
- Discovering the 93.9% profitability gap.

**4. Statistical Rigor**
- Hypothesis testing: rejecting geography null, failing to reject gender.
- P‑values and business implications.

**5. Building Predictive Models**
- Two‑stage approach.
- Model performance (recall, R²).
- Creating the risk score.

**6. From Insights to Action**
- Risk‑based pricing tiers.
- Dashboard demo (screenshots).
- Expected business impact.

**7. Lessons Learned**
- Importance of data quality.
- Balancing complexity with interpretability.
- Next steps.

**8. Conclusion**
- Summary of value delivered.