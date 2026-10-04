"""
Data Preprocessing and Feature Engineering Module
YUVA Internship - Week 3

Cleans and prepares Superstore transaction records for hypothesis testing and statistical modeling.
"""

import os
import pandas as pd
import numpy as np
from typing import Tuple


def clean_and_prepare_data(df: pd.DataFrame, output_path: str = None) -> pd.DataFrame:
    """
    Cleans raw Superstore data and engineers statistical features:
    - Parses date columns
    - Validates null counts and data types
    - Constructs Discount_Status (Discounted vs No Discount)
    - Constructs Profitability_Status (Profitable vs Loss-making)
    - Constructs Profit_Margin and Discount_Band

    Args:
        df: Raw DataFrame.
        output_path: Optional path to save processed CSV.

    Returns:
        pd.DataFrame: Cleaned and feature-engineered DataFrame.
    """
    cleaned = df.copy()

    # 1. Column standardization (strip whitespace)
    cleaned.columns = [col.strip() for col in cleaned.columns]

    # 2. Date parsing
    if 'Order Date' in cleaned.columns:
        cleaned['Order Date'] = pd.to_datetime(cleaned['Order Date'])
    if 'Ship Date' in cleaned.columns:
        cleaned['Ship Date'] = pd.to_datetime(cleaned['Ship Date'])
    if 'Order Date' in cleaned.columns and 'Ship Date' in cleaned.columns:
        cleaned['Shipping Days'] = (cleaned['Ship Date'] - cleaned['Order Date']).dt.days

    # 3. Numeric validation
    numeric_cols = ['Sales', 'Quantity', 'Discount', 'Profit']
    for col in numeric_cols:
        if col in cleaned.columns:
            cleaned[col] = pd.to_numeric(cleaned[col], errors='coerce')

    # Verify missing values
    null_counts = cleaned[numeric_cols].isnull().sum()
    if null_counts.sum() > 0:
        print(f"[WARNING] Missing numeric values detected:\n{null_counts}")
        cleaned = cleaned.dropna(subset=numeric_cols)
    else:
        print("[INFO] Zero missing values detected across numeric target columns.")

    # 4. Feature Engineering for Statistical Testing
    # Discount Status: Discount > 0 vs Discount == 0
    cleaned['Discount_Status'] = np.where(cleaned['Discount'] > 0, 'Discounted', 'No Discount')

    # Profitability Status: Profit > 0 vs Profit <= 0
    cleaned['Profitability_Status'] = np.where(cleaned['Profit'] > 0, 'Profitable', 'Loss-making')

    # Profit Margin
    cleaned['Profit_Margin'] = np.where(cleaned['Sales'] > 0, cleaned['Profit'] / cleaned['Sales'], 0.0)

    # Discount Percentage
    cleaned['Discount_Pct'] = cleaned['Discount'] * 100.0

    # Discount Bins / Bands for granular exploratory analysis
    bins = [-0.001, 0.000, 0.100, 0.200, 0.500, 1.000]
    labels = ['None (0%)', 'Low (1-10%)', 'Moderate (11-20%)', 'High (21-50%)', 'Deep (>50%)']
    cleaned['Discount_Band'] = pd.cut(cleaned['Discount'], bins=bins, labels=labels)

    # 5. Output summary
    print("[INFO] Preprocessing complete:")
    print(f"  - Total records: {len(cleaned)}")
    print(f"  - Discounted orders: {(cleaned['Discount_Status'] == 'Discounted').sum()} ({(cleaned['Discount_Status'] == 'Discounted').mean()*100:.2f}%)")
    print(f"  - No-discount orders: {(cleaned['Discount_Status'] == 'No Discount').sum()} ({(cleaned['Discount_Status'] == 'No Discount').mean()*100:.2f}%)")
    print(f"  - Profitable orders: {(cleaned['Profitability_Status'] == 'Profitable').sum()} ({(cleaned['Profitability_Status'] == 'Profitable').mean()*100:.2f}%)")
    print(f"  - Loss-making orders: {(cleaned['Profitability_Status'] == 'Loss-making').sum()} ({(cleaned['Profitability_Status'] == 'Loss-making').mean()*100:.2f}%)")

    # Save to disk if path specified
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cleaned.to_csv(output_path, index=False)
        print(f"[INFO] Processed dataset saved to: {output_path}")

    return cleaned


if __name__ == "__main__":
    from data_loading import load_raw_data
    raw_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "Sample - Superstore.csv")
    out_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "superstore_cleaned.csv")
    df_raw = load_raw_data(raw_path)
    df_clean = clean_and_prepare_data(df_raw, out_path)
