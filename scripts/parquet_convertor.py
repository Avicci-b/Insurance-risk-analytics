import pandas as pd

essential_columns = [
    'Province', 'PostalCode', 'MainCrestaZone',
    'VehicleType', 'make', 'bodytype', 'RegistrationYear', 'cubiccapacity',
    'Gender', 'MaritalStatus', 'Bank', 'AccountType',
    'CoverType', 'SumInsured', 'ExcessSelected',
    'TotalClaims', 'AnnualPremium', 'TotalPremium',
    'AnnualLossRatio', 'ProfitLoss'
]

csv_path = "./data/processed/insurance_data_cleaned.csv"
parquet_path = "./data/processed/insurance_data_cleaned.parquet"

# Read in chunks to avoid memory blow‑up
chunksize = 50_000
first = True

for chunk in pd.read_csv(csv_path, usecols=essential_columns, chunksize=chunksize, low_memory=False):
    if first:
        # write first chunk, create new file
        chunk.to_parquet(parquet_path, index=False)
        first = False
    else:
        # append subsequent chunks
        chunk.to_parquet(parquet_path, index=False)#append#=#T#rue)

print("✅ Conversion complete:", parquet_path)