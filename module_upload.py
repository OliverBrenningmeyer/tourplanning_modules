import pandas as pd
from typing import Optional, Union, Dict

def upload_excel(path: str, sheet_name: Optional[str] = None) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    Load an Excel file from a local path into a pandas DataFrame.
    Returns a single DataFrame (if sheet_name provided) or dict of DataFrames when sheet_name is None.

    Usage:
        df = upload_excel('data.xlsx', sheet_name='Sheet1')
    """
    try:
        return pd.read_excel(path, sheet_name=sheet_name)
    except Exception as e:
        raise IOError(f"Could not read Excel file at {path}: {e}")


def upload_excel_via_widget(sheet_name: Optional[str] = None) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    Display an upload button in Colab to select an Excel file interactively.
    Returns a DataFrame or dict of DataFrames based on sheet_name.

    Usage in Colab:
        df = upload_excel_via_widget('Sheet1')
    """
    from google.colab import files
    uploaded = files.upload()  # opens file chooser
    if not uploaded:
        raise FileNotFoundError('No file uploaded')
    # Take first uploaded file
    fname = next(iter(uploaded.keys()))
    return upload_excel(fname, sheet_name=sheet_name)