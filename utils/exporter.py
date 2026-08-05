"""
Export Utilities for HealthGuardian AI
Provides CSV and Excel file exports for patient prediction records and health metrics.
"""

import io
import pandas as pd
from typing import List, Dict, Any


def export_to_csv(data: List[Dict[str, Any]]) -> bytes:
    """Export list of dictionary records to CSV byte buffer."""
    if not data:
        return b""
    df = pd.DataFrame(data)
    # Remove complex nested json columns for clean tabular export
    if "details_json" in df.columns:
        df = df.drop(columns=["details_json"])
    if "details" in df.columns:
        df = df.drop(columns=["details"])
        
    return df.to_csv(index=False).encode('utf-8')


def export_to_excel(data: List[Dict[str, Any]]) -> bytes:
    """Export list of dictionary records to Excel (.xlsx) byte buffer."""
    if not data:
        return b""
    df = pd.DataFrame(data)
    if "details_json" in df.columns:
        df = df.drop(columns=["details_json"])
    if "details" in df.columns:
        df = df.drop(columns=["details"])

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Prediction_History')
    return output.getvalue()
