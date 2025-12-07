#!/usr/bin/env python3
"""Document the structure of original data file."""
import pandas as pd
import json
import yaml
from pathlib import Path
import sys

def document_raw_data():
    """Create documentation for raw data structure."""
    
    # Load parameters
    with open("params.yaml", 'r') as f:
        params = yaml.safe_load(f)
    
    original_file = Path("data/raw") / params['data']['original_file']
    
    print(f"📄 Documenting: {original_file}")
    
    # Read first few rows to understand structure
    try:
        # Read with pipe delimiter (discovered in EDA)
        df_sample = pd.read_csv(
            original_file, 
            delimiter=params['data']['delimiter'],
            nrows=5,
            low_memory=False
        )
        
        # Create documentation
        doc = {
            "documentation_date": pd.Timestamp.now().isoformat(),
            "file_info": {
                "filename": str(original_file),
                "size_mb": original_file.stat().st_size / (1024*1024),
                "delimiter": params['data']['delimiter'],
                "note": "Discovered in EDA: File uses pipe (|) delimiter"
            },
            "data_structure": {
                "rows_total": "1,000,098 (from EDA)",
                "columns_total": len(df_sample.columns),
                "columns_sample": df_sample.columns.tolist()[:10],
                "data_types_sample": {
                    col: str(dtype) for col, dtype in df_sample.dtypes.head(10).items()
                }
            },
            "eda_findings_applied": [
                "Delimiter: | (pipe), not comma",
                "All columns match project description (55 columns)",
                "Data appears complete for key columns"
            ]
        }
        
        # Save documentation
        report_path = Path("reports/raw_data_documentation.md")
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write("# Raw Data Documentation\n\n")
            f.write(f"**File:** {doc['file_info']['filename']}\n")
            f.write(f"**Size:** {doc['file_info']['size_mb']:.1f} MB\n")
            f.write(f"**Delimiter:** `{doc['file_info']['delimiter']}`\n\n")
            f.write("## Data Structure\n")
            f.write(f"- **Total columns:** {doc['data_structure']['columns_total']}\n")
            f.write("- **First 10 columns:**\n")
            for col in doc['data_structure']['columns_sample']:
                f.write(f"  - `{col}`\n")
        
        # Save metrics
        metrics_path = Path("reports/raw_data_metrics.json")
        with open(metrics_path, 'w') as f:
            json.dump(doc, f, indent=2)
        
        print(f"✅ Documentation saved: {report_path}")
        return doc
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    document_raw_data()