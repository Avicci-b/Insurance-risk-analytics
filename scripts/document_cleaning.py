#!/usr/bin/env python3
"""Document data cleaning steps discovered in EDA."""
import json
import yaml
from pathlib import Path

def document_cleaning():
    """Document cleaning steps from Task 1 EDA."""
    
    with open("params.yaml", 'r') as f:
        params = yaml.safe_load(f)
    
    print("🧹 Documenting data cleaning process")
    
    # Based on your EDA findings
    doc = {
        "key_discoveries": {
            "premium_data": "TotalPremium represents MONTHLY premium (not annual)",
            "scaling_applied": f"Multiplied by {params['data']['premium_scaling_factor']} for annual equivalent",
            "new_column": "Created AnnualPremium = TotalPremium × 12",
            "business_impact": "Loss ratio changed from 104.77% → 8.7% (profitable)"
        },
        "cleaning_steps": [
            "Unit correction: Monthly → Annual premium",
            "Created derived column: AnnualPremium",
            "Recalculated business metrics with corrected units"
        ],
        "business_insights": {
            "overall_profitability": f"{params['business']['overall_loss_ratio']}% loss ratio (profitable)",
            "claim_frequency": f"{params['business']['claim_frequency']}% of policies",
            "claim_severity": f"R{params['business']['avg_claim_severity']:,.2f} average",
            "risk_segmentation": "93.9% loss ratio gap between Gauteng and Northern Cape"
        }
    }
    
    # Save reports
    report_path = Path("reports/cleaning_documentation.md")
    with open(report_path, 'w') as f:
        f.write("# Data Cleaning Documentation\n\n")
        f.write("## Key Discovery\n")
        f.write(f"- **Issue:** {doc['key_discoveries']['premium_data']}\n")
        f.write(f"- **Fix:** {doc['key_discoveries']['scaling_applied']}\n")
        f.write(f"- **Impact:** {doc['key_discoveries']['business_impact']}\n\n")
        
        f.write("## Business Insights\n")
        for key, value in doc['business_insights'].items():
            f.write(f"- **{key.replace('_', ' ').title()}:** {value}\n")
    
    # Save metrics
    metrics_path = Path("reports/cleaning_metrics.json")
    with open(metrics_path, 'w') as f:
        json.dump(doc, f, indent=2)
    
    # Save business insights separately
    insights_path = Path("reports/business_insights.json")
    with open(insights_path, 'w') as f:
        json.dump(doc['business_insights'], f, indent=2)
    
    print(f"✅ Cleaning documented: {report_path}")
    print(f"   Key fix: Premium × {params['data']['premium_scaling_factor']}")
    return doc

if __name__ == "__main__":
    document_cleaning()