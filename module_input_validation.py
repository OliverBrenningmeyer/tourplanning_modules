"""
Input validation module for tour planning.
Validates input files and data quality before processing.
"""

import pandas as pd
import os
from typing import Dict, List, Tuple, Optional
from module_column_mapping import get_column_mapping, EXPECTED_COLUMNS
from module_client_configuration import CONFIG


class InputValidator:
    """
    Validates input files and data quality for tour planning.
    """
    
    def __init__(self, client_name: str):
        self.client_name = client_name
        self.column_mapping = get_column_mapping(client_name)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def validate_file_upload(self, df: pd.DataFrame, sheet_name: Optional[str] = None) -> Tuple[bool, List[str], List[str]]:
        """
        Validate the uploaded Excel file.
        
        Args:
            df: The uploaded DataFrame
            sheet_name: Optional sheet name that was used
            
        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        if df is None:
            self.errors.append("❌ No file was uploaded or file could not be read.")
            return False, self.errors, self.warnings
        
        if df.empty:
            self.errors.append("❌ The uploaded file is empty (no rows).")
            self.errors.append("   → Check that you selected the correct file and sheet.")
            return False, self.errors, self.warnings
        
        # Check for minimum required columns
        required_columns = self._get_required_columns()
        missing_columns = []
        for col in required_columns:
            if col not in df.columns:
                missing_columns.append(col)
        
        if missing_columns:
            self.errors.append(f"❌ Missing required columns in input file:")
            for col in missing_columns:
                self.errors.append(f"   - '{col}'")
            self.errors.append("")
            self.errors.append("   Common causes:")
            self.errors.append("   → Wrong file uploaded (check file name and content)")
            self.errors.append("   → Wrong sheet selected (check sheet name)")
            self.errors.append("   → File format changed (check column names match expected format)")
            self.errors.append("")
            self.errors.append(f"   Expected columns for client '{self.client_name}':")
            for col in required_columns:
                mapped_col = self._find_mapped_column(col)
                if mapped_col:
                    self.errors.append(f"   - '{mapped_col}' (mapped to '{col}')")
                else:
                    self.errors.append(f"   - '{col}'")
            return False, self.errors, self.warnings
        
        # Check data quality
        self._validate_data_quality(df)
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def _get_required_columns(self) -> List[str]:
        """Get the list of required columns for the client."""
        # Critical columns that must exist after mapping
        critical_columns = [
            "customer_branch_cluster",
            "Entl. bis (Auftr.)",
            "Auftr.-Nr.",
            "customer_shipment_weight_kg",
            "customer_shipment_volume_units"
        ]
        
        # Add address columns based on geocoding config
        geocoding_config = CONFIG.get(self.client_name, {}).get("geocoding", {"pickup": True, "dropoff": True})
        
        if geocoding_config.get("pickup", True):
            critical_columns.extend(["Vers.-Str.", "Vers.-PLZ", "Vers.-Ort"])
        
        if geocoding_config.get("dropoff", True):
            critical_columns.extend(["Empf.-Str.", "Empf.-PLZ", "Empf.-Ort"])
        
        return critical_columns
    
    def _find_mapped_column(self, standard_column: str) -> Optional[str]:
        """Find the original column name that maps to the standard column."""
        for original, mapped in self.column_mapping.items():
            if mapped == standard_column:
                return original
        return None
    
    def _validate_data_quality(self, df: pd.DataFrame):
        """Validate data quality issues."""
        # Check for empty critical columns
        critical_checks = {
            "customer_branch_cluster": "Branch cluster",
            "Entl. bis (Auftr.)": "Delivery date",
            "Auftr.-Nr.": "Order number"
        }
        
        for col, description in critical_checks.items():
            if col in df.columns:
                null_count = df[col].isnull().sum()
                empty_count = (df[col].astype(str).str.strip() == "").sum() if df[col].dtype == 'object' else 0
                total_issues = null_count + empty_count
                
                if total_issues > 0:
                    if total_issues == len(df):
                        self.errors.append(f"❌ All rows have missing {description} ('{col}')")
                        self.errors.append("   → Check your input file - this column is required for all orders")
                    else:
                        self.warnings.append(f"⚠️  {total_issues} rows have missing {description} ('{col}')")
                        self.warnings.append("   → These rows will be filtered out during processing")
        
        # Check date format
        if "Entl. bis (Auftr.)" in df.columns:
            try:
                # Try to parse dates
                pd.to_datetime(df["Entl. bis (Auftr.)"], errors='coerce', format='%d.%m.%y %H:%M')
                invalid_dates = df["Entl. bis (Auftr.)"].isnull().sum()
                if invalid_dates > 0:
                    self.warnings.append(f"⚠️  {invalid_dates} rows have invalid date format in 'Entl. bis (Auftr.)'")
                    self.warnings.append("   → Expected format: 'dd.mm.yy HH:MM' (e.g., '15.12.25 14:30')")
            except:
                self.warnings.append("⚠️  Could not validate date format in 'Entl. bis (Auftr.)'")
                self.warnings.append("   → Expected format: 'dd.mm.yy HH:MM' (e.g., '15.12.25 14:30')")
        
        # Check numeric columns
        if "customer_shipment_weight_kg" in df.columns:
            try:
                numeric_weight = pd.to_numeric(df["customer_shipment_weight_kg"], errors='coerce')
                invalid_weight = numeric_weight.isnull().sum()
                if invalid_weight > 0:
                    self.warnings.append(f"⚠️  {invalid_weight} rows have invalid weight values")
                    self.warnings.append("   → Weight will be set to 1 kg for these rows")
            except:
                pass
        
        if "customer_shipment_volume_units" in df.columns:
            try:
                numeric_volume = pd.to_numeric(df["customer_shipment_volume_units"], errors='coerce')
                invalid_volume = numeric_volume.isnull().sum()
                if invalid_volume > 0:
                    self.warnings.append(f"⚠️  {invalid_volume} rows have invalid volume values")
                    self.warnings.append("   → Volume will be set to 0 for these rows")
            except:
                pass
    
    def validate_depots_file(self, depots_path: str) -> Tuple[bool, List[str], List[str]]:
        """
        Validate the depots Excel file.
        
        Args:
            depots_path: Path to the depots file
            
        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        if not os.path.exists(depots_path):
            self.errors.append(f"❌ Depots file not found: {depots_path}")
            self.errors.append("   → Check that the file exists at the specified path")
            self.errors.append("   → Verify the client name is correct")
            return False, self.errors, self.warnings
        
        try:
            df_depots = pd.read_excel(depots_path, engine='openpyxl')
        except Exception as e:
            self.errors.append(f"❌ Could not read depots file: {str(e)}")
            self.errors.append("   → Check that the file is a valid Excel file (.xlsx)")
            return False, self.errors, self.warnings
        
        if df_depots.empty:
            self.errors.append("❌ Depots file is empty")
            return False, self.errors, self.warnings
        
        # Check required columns
        required_depot_columns = [
            "Dispobereich",
            "active_Dispobereich",
            "here_lat",
            "here_lng"
        ]
        
        missing_columns = [col for col in required_depot_columns if col not in df_depots.columns]
        if missing_columns:
            self.errors.append(f"❌ Missing required columns in depots file:")
            for col in missing_columns:
                self.errors.append(f"   - '{col}'")
            return False, self.errors, self.warnings
        
        # Check for active depots
        active_depots = df_depots[df_depots['active_Dispobereich'].notna()]
        if active_depots.empty:
            self.warnings.append("⚠️  No active depots found in depots file")
            self.warnings.append("   → Check 'active_Dispobereich' column has values")
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def validate_after_cleaning(self, df_clean: pd.DataFrame, df_raw: pd.DataFrame) -> Tuple[bool, List[str], List[str]]:
        """
        Validate data after cleaning step.
        
        Args:
            df_clean: Cleaned DataFrame
            df_raw: Original raw DataFrame
            
        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        if df_clean.empty:
            self.errors.append("❌ No data remaining after cleaning and filtering")
            self.errors.append("")
            self.errors.append("   Common causes:")
            self.errors.append("   → No orders match the selected planning date")
            self.errors.append("   → All orders were filtered out due to missing branch clusters")
            self.errors.append("   → Date format in input file doesn't match expected format")
            self.errors.append("")
            self.errors.append(f"   Original data had {len(df_raw)} rows")
            self.errors.append("   → Check your input file date column format")
            self.errors.append("   → Verify the planning date matches dates in your file")
            return False, self.errors, self.warnings
        
        rows_lost = len(df_raw) - len(df_clean)
        if rows_lost > 0:
            self.warnings.append(f"⚠️  {rows_lost} rows were filtered out during cleaning")
            self.warnings.append(f"   → {len(df_clean)} rows remain for processing")
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def validate_geocoding(self, df_geocoded: pd.DataFrame) -> Tuple[bool, List[str], List[str]]:
        """
        Validate geocoding results.
        
        Args:
            df_geocoded: Geocoded DataFrame
            
        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        geocoding_config = CONFIG.get(self.client_name, {}).get("geocoding", {"pickup": True, "dropoff": True})
        
        # Check dropoff geocoding
        if geocoding_config.get("dropoff", True):
            if "dropoff_lat" in df_geocoded.columns:
                failed_geocoding = df_geocoded["dropoff_lat"].isnull().sum()
                if failed_geocoding > 0:
                    if failed_geocoding == len(df_geocoded):
                        self.errors.append("❌ All dropoff addresses failed geocoding")
                        self.errors.append("   → Check address columns: 'Empf.-Str.', 'Empf.-PLZ', 'Empf.-Ort'")
                        self.errors.append("   → Verify addresses are complete and valid")
                    else:
                        self.warnings.append(f"⚠️  {failed_geocoding} dropoff addresses failed geocoding")
                        self.warnings.append("   → These orders may not be assigned to tours")
        
        # Check pickup geocoding
        if geocoding_config.get("pickup", True):
            if "pickup_lat" in df_geocoded.columns:
                failed_geocoding = df_geocoded["pickup_lat"].isnull().sum()
                if failed_geocoding > 0:
                    self.warnings.append(f"⚠️  {failed_geocoding} pickup addresses failed geocoding")
        
        return len(self.errors) == 0, self.errors, self.warnings


def validate_input_file(df: pd.DataFrame, client_name: str, sheet_name: Optional[str] = None) -> Tuple[bool, List[str], List[str]]:
    """
    Convenience function to validate input file.
    
    Args:
        df: The uploaded DataFrame
        client_name: Name of the client
        sheet_name: Optional sheet name
        
    Returns:
        Tuple of (is_valid, errors, warnings)
    """
    validator = InputValidator(client_name)
    return validator.validate_file_upload(df, sheet_name)

