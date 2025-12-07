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