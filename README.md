# Insurance Risk Analytics & Predictive Modeling

## Project Overview
This project analyzes historical car insurance claim data for AlphaCare Insurance Solutions (ACIS) to identify low-risk customer segments and optimize premium pricing strategies.

## Business Objective
Discover "low-risk" customer targets for premium reduction to attract new clients while maintaining profitability.

## Project Structure
insurance-risk-analytics/
├── .github/workflows/ # CI/CD pipelines
├── data/ # Data storage
├── notebooks/ # Jupyter notebooks for analysis
├── scripts/ # Utility scripts
├── src/ # Source code modules
├── tests/ # Test files
├── venv/ # Virtual environment (ignored)
├── .gitignore # Git ignore rules
├── README.md # Project documentation
└── requirements.txt # Python dependencies
## Tasks Timeline
Task 1: EDA & Statistical Analysis

Task 2: Data Version Control Setup

Task 3: A/B Hypothesis Testing

Task 4: Predictive Modeling

## Data Source
Historical insurance claim data (February 2014 - August 2015) provided by ACIS.

## Task 2 DVC set-up
Data Tracking
✅ Raw data: MachineLearningRating_v3.txt (pipe-separated)

✅ Converted data: insurance_data.csv (CSV format)

✅ Cleaned data: insurance_data_cleaned.csv (premium corrected)

Reproducible Pipeline
bash
# Run entire data pipeline
dvc repro

# View pipeline
dvc dag

# Output:
# 1. document_raw_data → 2. document_conversion → 
# 3. document_cleaning → 4. generate_eda_summary
Storage Configuration
Remote: localstorage

Location: ../dvc_storage/

Status: All data files version controlled

✅ Task 3: A/B Hypothesis Testing
Objective: Statistically validate key risk drivers

Tests Conducted:

- Provincial Risk: ANOVA (p=0.000044) → REJECT H₀ - Significant differences

- Zip Code Risk: ANOVA (p<0.001) → REJECT H₀ - Hyper-local variation exists

- Zip Code Profit: t-test (p<0.001) → REJECT H₀ - Profitability varies

- Gender Risk: Multiple tests (p=0.45-0.95) → FAIL TO REJECT H₀ - No significant difference

- Business Impact: Statistical evidence supports regional pricing, rejects gender-based pricing

✅ Task 4: Predictive Modeling
Objective: Build risk-based pricing models

Models Built:

- Classification: Predict claim probability (3 models tested)

- Regression: Predict claim amount (3 models tested)

Best Performers:

- Logistic Regression: 80.84% recall for claim detection

- Linear Regression: R²=0.2995 for amount prediction

Key Output: Risk scoring system (0-100 scale) with premium adjustments (-15% to +25%)