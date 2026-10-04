"""
Data Loading Module for Superstore Statistical Analysis
YUVA Internship - Week 3

Handles loading raw Superstore sales data with encoding fallbacks and integrity checks.
"""

import os
import pandas as pd
from typing import Optional


def load_raw_data(filepath: str, encoding_priority: Optional[list] = None) -> pd.DataFrame:
    """
    Loads the Superstore dataset from the specified filepath.
    Attempts multiple encodings (windows-1252, utf-8, latin1) to ensure robust loading.

    Args:
        filepath: Relative or absolute path to the CSV file.
        encoding_priority: Optional list of encodings to try sequentially.

    Returns:
        pd.DataFrame: Loaded dataset.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If loading fails across all attempted encodings.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset file not found at: {filepath}")

    if encoding_priority is None:
        encoding_priority = ['windows-1252', 'utf-8', 'latin1', 'cp1252']

    last_error = None
    for enc in encoding_priority:
        try:
            df = pd.read_csv(filepath, encoding=enc)
            print(f"[INFO] Successfully loaded dataset using '{enc}' encoding.")
            print(f"[INFO] Dimensions: {df.shape[0]} rows, {df.shape[1]} columns.")
            return df
        except UnicodeDecodeError as e:
            last_error = e
            continue
        except Exception as e:
            raise RuntimeError(f"Unexpected error loading dataset: {e}")

    raise ValueError(f"Failed to load dataset with tried encodings {encoding_priority}. Last error: {last_error}")


if __name__ == "__main__":
    test_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "Sample - Superstore.csv")
    df = load_raw_data(test_path)
    print("Columns:", df.columns.tolist()[:5], "...")
