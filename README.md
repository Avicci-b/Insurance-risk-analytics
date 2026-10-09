# Insurance Risk Analytics & Predictive Modeling

[![CI](https://github.com/Avicci-b/Insurance-risk-analytics/actions/workflows/ci.yml/badge.svg)](https://github.com/Avicci-b/Insurance-risk-analytics/actions/workflows/ci.yml)

An end-to-end insurance analytics project exploring claims, geographic risk differences, and predictive modeling to support more informed insurance pricing decisions. The project combines exploratory data analysis (EDA), statistical hypothesis testing, machine learning, data version control, and an interactive Streamlit dashboard.

## Business Problem

AlphaCare Insurance Solutions (ACIS) wants to identify differences in insurance risk across customer segments and use evidence from historical policy and claims data to inform pricing decisions.

Uniform pricing across regions may overlook meaningful differences in claims experience. This project investigates those differences and explores how predictive models can help estimate claim risk and expected claim amounts.

**Project objectives**

* Explore claims, premiums, and customer risk patterns.
* Test whether risk differs across geographic and demographic groups.
* Build classification and regression models for claims analysis.
* Develop a risk-scoring approach to support pricing decisions.
* Organize the workflow for reproducibility using DVC and automated testing.

## Key Findings & Results

| Analysis                | Reported result                                                                                                   |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Dataset                 | Approximately 1 million policies                                                                                  |
| Observation period      | February 2014 – August 2015                                                                                       |
| Geographic analysis     | Reported loss ratios of 122.2% for Gauteng and 28.3% for Northern Cape                                            |
| Hypothesis testing      | Geographic differences reported at p < 0.001; no statistically significant gender difference reported at p > 0.45 |
| Claim classification    | 80.84% recall using Logistic Regression                                                                           |
| Claim amount prediction | Linear Regression R² = 0.30                                                                                       |
| Risk scoring            | Probability of a claim combined with predicted claim amount, scaled to 0–100                                      |

*Results are based on the project's analysis and should be interpreted alongside the relevant notebook definitions, evaluation methods, and assumptions. The loss-ratio calculation and premium-scaling correction require validation before the corrected loss-ratio figure is reported as a final result.*

## Methodology

### 1. Exploratory Data Analysis

* Examined the distribution of premiums and claims.
* Investigated differences in loss ratios across provinces and other customer segments.
* Identified data interpretation and preprocessing issues that could affect downstream analysis.

### 2. Statistical Hypothesis Testing

* Tested whether claims experience differed across geographic groups.
* Investigated whether the data provided evidence of differences by gender.
* Used statistical results to inform the interpretation of observed patterns.

### 3. Predictive Modeling

* **Classification — Logistic Regression:** estimates claim occurrence and evaluates claim detection using classification metrics.
* **Regression — Linear Regression:** estimates claim amounts and evaluates prediction errors.
* **Risk scoring:** combines estimated claim probability and expected claim amount into a score intended to support risk segmentation.

### 4. Reproducibility & Engineering

* Used DVC to track data and support reproducible analysis.
* Organized analysis code, source modules, and tests into separate directories.
* Configured continuous integration to run automated checks.

## Technology Stack

* **Programming & analysis:** Python, pandas, NumPy
* **Visualization:** Matplotlib, Seaborn, Streamlit
* **Statistics & machine learning:** SciPy, scikit-learn
* **Data and experiment workflow:** DVC, Git, GitHub Actions
* **Testing:** pytest

## Repository Structure

```text
Insurance-risk-analytics/
├── .github/
│   └── workflows/       # CI configuration
├── data/                # Dataset files or DVC-tracked data
├── notebooks/           # EDA, statistical tests, and modeling
├── scripts/             # Analysis and utility scripts
├── src/                 # Reusable source code
├── tests/               # Automated tests
├── dashboard/           # Streamlit dashboard
├── reports/             # Analysis reports and outputs
├── models/              # Model artifacts, if retained
├── params.yaml          # Pipeline parameters
├── dvc.yaml             # DVC pipeline definition
├── dvc.lock             # Recorded pipeline dependencies
├── requirements.txt     # Python dependencies
├── .gitignore
├── .dvcignore
└── README.md
```

## Getting Started

### Prerequisites

* Python installed
* Git installed
* Access to the DVC remote if the project data is stored remotely

### Installation

Clone the repository and enter the project directory:

```bash
git clone https://github.com/Avicci-b/Insurance-risk-analytics.git
cd Insurance-risk-analytics
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Linux or macOS:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### Retrieve the data

If the dataset is managed through a configured DVC remote and you have access to it, run:

```bash
dvc pull
```

### Launch the dashboard

```bash
streamlit run dashboard/app.py
```

Run notebook analyses separately in Jupyter if you want to explore the data preparation, hypothesis tests, and model evaluation in detail.

## Evaluation

The modeling workflow reports classification metrics such as precision, recall, F1-score, and ROC-AUC, alongside regression metrics such as R², RMSE, and MAE. Cross-validation was performed on a 500,000-row sample to accommodate memory constraints.

Recall measures the proportion of actual claim-positive cases identified by the classifier. It should be interpreted alongside precision and other metrics, particularly when deciding how a model could be used in a pricing workflow.

## Limitations & Future Work

* Validate the premium-scaling and loss-ratio calculations against the source data and business definitions.
* Compare additional models and tune their hyperparameters.
* Improve the interpretation of risk scores and assess their calibration.
* Add model explanations to the dashboard.
* Evaluate model stability on newer data before considering deployment.
* Investigate additional relevant data sources, subject to availability, legality, and appropriate use.

## Author

**Biniyam Mitiku**
Information Science Student | Data Analytics & Machine Learning

This project was completed as part of the KAIM Academy Insurance Risk Analytics Challenge.
