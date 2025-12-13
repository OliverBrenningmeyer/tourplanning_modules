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
        return pd.read_excel(path, sheet_name=sheet_name, engine='openpyxl')
    except FileNotFoundError:
        raise FileNotFoundError(
            f"❌ File not found: {path}\n"
            "   → Check that the file exists at the specified path\n"
            "   → Verify the file name is correct"
        )
    except ValueError as e:
        if "Worksheet named" in str(e) or "sheet_name" in str(e).lower():
            raise ValueError(
                f"❌ Sheet '{sheet_name}' not found in Excel file\n"
                f"   → Check that the sheet name is correct\n"
                f"   → Available sheets can be checked by opening the file\n"
                f"   → Original error: {e}"
            )
        raise
    except Exception as e:
        raise IOError(
            f"❌ Could not read Excel file at {path}\n"
            f"   → Make sure the file is a valid Excel file (.xlsx format)\n"
            f"   → Check that the file is not corrupted\n"
            f"   → Original error: {e}"
        )


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
        raise FileNotFoundError(
            "❌ No file uploaded\n"
            "   → Please select a file using the file upload widget\n"
            "   → Make sure you click 'Choose Files' and select your Excel file"
        )
    # Take first uploaded file
    fname = next(iter(uploaded.keys()))
    print(f"📁 Uploaded file: {fname}")
    if sheet_name:
        print(f"📄 Loading sheet: '{sheet_name}'")
    return upload_excel(fname, sheet_name=sheet_name)