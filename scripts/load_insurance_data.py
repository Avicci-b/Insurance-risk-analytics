#!/usr/bin/env python3
"""
Load pipe-separated insurance data and convert to CSV.
"""
import pandas as pd
import os
from pathlib import Path
import numpy as np


def load_and_convert():
    """Load the pipe-separated TXT file and convert to CSV."""

    # Define paths
    data_dir = Path("data/raw")
    txt_file = data_dir / "MachineLearningRating_v3.txt"
    csv_file = data_dir / "insurance_data.csv"

    print("📁 Loading insurance data...")
    print(f"Input file: {txt_file}")

    # Check if file exists
    if not txt_file.exists():
        print(f"❌ Error: File not found at {txt_file}")
        print("Please ensure MachineLearningRating_v3.txt is in data/raw/ directory")
        return None

    # Load with pipe delimiter
    try:
        df = pd.read_csv(txt_file, delimiter="|", low_memory=False)
        print(f"✅ Successfully loaded {len(df):,} rows and {len(df.columns)} columns")
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return None

    # Basic information
    print("\n" + "=" * 60)
    print("📊 DATA BASIC INFORMATION")
    print("=" * 60)
    print(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

    # Show columns by category
    print("\n📋 COLUMNS BY CATEGORY:")

    # Policy columns
    policy_cols = [col for col in df.columns if "Cover" in col or "Policy" in col or "ID" in col]
    print(f"  • Policy/ID columns: {len(policy_cols)}")

    # Client columns
    client_cols = [
        col
        for col in df.columns
        if col
        in [
            "IsVATRegistered",
            "Citizenship",
            "LegalType",
            "Title",
            "Language",
            "Bank",
            "AccountType",
            "MaritalStatus",
            "Gender",
        ]
    ]
    print(f"  • Client columns: {len(client_cols)}")

    # Location columns
    location_cols = [
        col for col in df.columns if col in ["Country", "Province", "PostalCode", "MainCrestaZone", "SubCrestaZone"]
    ]
    print(f"  • Location columns: {len(location_cols)}")

    # Vehicle columns
    vehicle_cols = [
        col
        for col in df.columns
        if col
        in [
            "ItemType",
            "mmcode",
            "VehicleType",
            "RegistrationYear",
            "make",
            "Model",
            "Cylinders",
            "cubiccapacity",
            "kilowatts",
            "bodytype",
            "NumberOfDoors",
            "VehicleIntroDate",
            "CustomValueEstimate",
            "AlarmImmobiliser",
            "TrackingDevice",
            "CapitalOutstanding",
            "NewVehicle",
            "WrittenOff",
            "Rebuilt",
            "Converted",
            "CrossBorder",
            "NumberOfVehiclesInFleet",
        ]
    ]
    print(f"  • Vehicle columns: {len(vehicle_cols)}")

    # Plan columns
    plan_cols = [
        col
        for col in df.columns
        if col
        in [
            "SumInsured",
            "TermFrequency",
            "CalculatedPremiumPerTerm",
            "ExcessSelected",
            "CoverCategory",
            "CoverType",
            "CoverGroup",
            "Section",
            "Product",
            "StatutoryClass",
            "StatutoryRiskType",
        ]
    ]
    print(f"  • Plan columns: {len(plan_cols)}")

    # Payment/Claim columns
    payment_cols = [col for col in df.columns if col in ["TotalPremium", "TotalClaims"]]
    print(f"  • Payment/Claim columns: {len(payment_cols)}")

    # Date columns
    date_cols = [col for col in df.columns if "Date" in col or "Month" in col]
    print(f"  • Date columns: {len(date_cols)}")

    # Calculate basic financial metrics
    print("\n💰 FINANCIAL METRICS:")
    total_premium = df["TotalPremium"].sum()
    total_claims = df["TotalClaims"].sum()

    print(f"  • Total Premium: R {total_premium:,.2f}")
    print(f"  • Total Claims: R {total_claims:,.2f}")

    # Loss Ratio
    loss_ratio = (total_claims / total_premium * 100) if total_premium > 0 else 0
    print(f"  • Loss Ratio: {loss_ratio:.2f}%")

    # Margin
    margin = total_premium - total_claims
    print(f"  • Total Margin: R {margin:,.2f}")

    # Claim statistics
    policies_with_claims = (df["TotalClaims"] > 0).sum()
    claim_frequency = (policies_with_claims / len(df)) * 100
    print(f"  • Policies with claims: {policies_with_claims:,} ({claim_frequency:.1f}%)")

    # Save as CSV
    print("\n💾 SAVING DATA...")
    df.to_csv(csv_file, index=False)
    print(f"✅ Saved as CSV: {csv_file}")
    print(f"   File size: {os.path.getsize(csv_file) / (1024*1024):.2f} MB")

    # Save a sample for quick analysis
    sample_size = min(5000, len(df))
    sample_file = data_dir / "insurance_sample.csv"
    df.sample(sample_size, random_state=42).to_csv(sample_file, index=False)
    print(f"📝 Saved {sample_size:,}-row sample: {sample_file}")

    # Save column description
    with open(data_dir / "column_description.txt", "w") as f:
        f.write("COLUMN DESCRIPTION FOR INSURANCE DATA\n")
        f.write("=" * 50 + "\n\n")
        for i, col in enumerate(df.columns, 1):
            f.write(f"{i:3}. {col}\n")
            # Add non-null count and type
            non_null = df[col].notna().sum()
            dtype = str(df[col].dtype)
            f.write(f"     Type: {dtype}, Non-null: {non_null:,}\n")

            # For categorical, show unique values
            if df[col].dtype == "object":
                unique_count = df[col].nunique()
                f.write(f"     Unique values: {unique_count:,}\n")
                if unique_count <= 10:
                    unique_vals = df[col].dropna().unique()[:10]
                    f.write(f"     Values: {', '.join(map(str, unique_vals))}\n")

            f.write("\n")

    print(f"📄 Column description saved: {data_dir / 'column_description.txt'}")

    return df


if __name__ == "__main__":
    df = load_and_convert()

    if df is not None:
        print("\n" + "=" * 60)
        print("✅ DATA LOADING COMPLETE!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Check column_description.txt for data understanding")
        print("2. Use insurance_sample.csv for quick EDA")
        print("3. Begin Task 1.2 EDA analysis")
