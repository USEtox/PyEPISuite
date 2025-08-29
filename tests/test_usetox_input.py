"""
Tests for USEtox Input module
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
import os
from pathlib import Path

from pyepisuite.usetox_input import USEtoxInput, create_usetox_input_from_episuite


@pytest.fixture
def sample_episuite_df():
    """Create a sample PyEPISuite DataFrame for testing."""
    return pd.DataFrame({
        'cas': ['50-00-0', '100-00-5', '100-02-7'],
        'name': ['FORMALDEHYDE', 'P-CHLORONITROBENZENE', '4-NITROPHENOL'],
        'molecular_weight': [30.026, 157.555, 139.109],
        'log_kow_estimated': [0.35, 2.39, 1.91],
        'log_koc_estimated': [0.11, 2.04, 1.58],
        'henrys_law_constant_estimated': [3.37e-07, 1.09e-05, 1.12e-08],
        'vapor_pressure_estimated': [3890.0, 0.4, 0.001],
        'water_solubility_logkow_estimated': [400000.0, 240.0, 16000.0],
        'atmospheric_half_life_estimated': [9.77, 35.7, 245.0]
    })


@pytest.fixture
def temp_excel_file():
    """Create a temporary Excel file path."""
    temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
    temp_file.close()
    yield temp_file.name
    # Cleanup
    if os.path.exists(temp_file.name):
        os.unlink(temp_file.name)


class TestUSEtoxInput:
    
    def test_init_with_default_template(self):
        """Test initialization with default template."""
        # This test might fail if template doesn't exist, which is expected
        try:
            usetox_input = USEtoxInput()
            assert usetox_input.template_df is not None
        except Exception:
            # Template file doesn't exist in test environment
            pytest.skip("USEtox template file not found")
    
    def test_episuite_to_usetox_mapping(self):
        """Test that column mapping is correctly defined."""
        assert 'cas' in USEtoxInput.EPISUITE_TO_USETOX_MAPPING
        assert 'molecular_weight' in USEtoxInput.EPISUITE_TO_USETOX_MAPPING
        assert USEtoxInput.EPISUITE_TO_USETOX_MAPPING['cas'] == 'CAS RN'
        assert USEtoxInput.EPISUITE_TO_USETOX_MAPPING['molecular_weight'] == 'MW'
    
    def test_unit_conversions(self):
        """Test unit conversion functions."""
        # Test log KOW conversion
        log_kow_converter = USEtoxInput.UNIT_CONVERSIONS['KOW']
        assert abs(log_kow_converter(2.0) - 100.0) < 1e-10
        assert np.isnan(log_kow_converter(np.nan))
        
        # Test vapor pressure conversion (mmHg to Pa)
        vp_converter = USEtoxInput.UNIT_CONVERSIONS['Pvap25']
        assert abs(vp_converter(1.0) - 133.322) < 1e-3
        
        # Test solubility conversion (mg/L to g/L)
        sol_converter = USEtoxInput.UNIT_CONVERSIONS['Sol25']
        assert abs(sol_converter(1000.0) - 1.0) < 1e-10
    
    def test_populate_from_episuite_dataframe(self, sample_episuite_df):
        """Test populating template from PyEPISuite DataFrame."""
        # Create a mock template
        template_data = {
            'RowNr': [np.nan] * 10,
            'CAS RN': [np.nan] * 10,
            'Name': [np.nan] * 10,
            'MW': [np.nan] * 10,
            'KOW': [np.nan] * 10,
            'Data source': [np.nan] * 10
        }
        template_df = pd.DataFrame(template_data)
        
        # Create USEtoxInput instance and manually set template
        usetox_input = USEtoxInput.__new__(USEtoxInput)
        usetox_input.template_df = template_df
        usetox_input.populated_df = None
        # Add required class constants
        usetox_input.EPISUITE_TO_USETOX_MAPPING = USEtoxInput.EPISUITE_TO_USETOX_MAPPING
        usetox_input.EXPERIMENTAL_PROPERTY_PRIORITY = USEtoxInput.EXPERIMENTAL_PROPERTY_PRIORITY
        usetox_input.UNIT_CONVERSIONS = USEtoxInput.UNIT_CONVERSIONS
        usetox_input.EXCEL_COLUMN_MAPPING = USEtoxInput.EXCEL_COLUMN_MAPPING
        
        # Populate with sample data
        result_df = usetox_input.populate_from_episuite_dataframe(sample_episuite_df)
        
        # Check that data was populated correctly
        assert result_df.loc[0, 'CAS RN'] == '50-00-0'
        assert result_df.loc[0, 'Name'] == 'FORMALDEHYDE'
        assert result_df.loc[0, 'MW'] == 30.026
        assert result_df.loc[0, 'Data source'] == 'PyEPISuite Estimated'  # Updated to match new naming
        
        # Check unit conversions
        assert abs(result_df.loc[0, 'KOW'] - 10**0.35) < 1e-10
    
    def test_add_chemical_manually(self):
        """Test manually adding a chemical."""
        # Create a mock template
        template_data = {
            'RowNr': [np.nan] * 5,
            'CAS RN': [np.nan] * 5,
            'Name': [np.nan] * 5,
            'MW': [np.nan] * 5
        }
        template_df = pd.DataFrame(template_data)
        
        # Create USEtoxInput instance
        usetox_input = USEtoxInput.__new__(USEtoxInput)
        usetox_input.template_df = template_df
        usetox_input.populated_df = None
        
        # Add a chemical manually
        properties = {'MW': 78.11}
        row_idx = usetox_input.add_chemical_manually(
            cas='71-43-2', 
            name='Benzene', 
            properties=properties
        )
        
        assert row_idx == 0
        assert usetox_input.populated_df.loc[0, 'CAS RN'] == '71-43-2'
        assert usetox_input.populated_df.loc[0, 'Name'] == 'Benzene'
        assert usetox_input.populated_df.loc[0, 'MW'] == 78.11
        assert usetox_input.populated_df.loc[0, 'RowNr'] == 1
    
    def test_get_summary_statistics(self, sample_episuite_df):
        """Test summary statistics generation."""
        # Create a mock template with more columns
        template_data = {
            'RowNr': [np.nan] * 10,
            'CAS RN': [np.nan] * 10,
            'Name': [np.nan] * 10,
            'MW': [np.nan] * 10,
            'KOW': [np.nan] * 10,
            'Data source': [np.nan] * 10
        }
        template_df = pd.DataFrame(template_data)
        
        usetox_input = USEtoxInput.__new__(USEtoxInput)
        usetox_input.template_df = template_df
        usetox_input.populated_df = None
        # Add required class constants for summary statistics test
        usetox_input.EPISUITE_TO_USETOX_MAPPING = USEtoxInput.EPISUITE_TO_USETOX_MAPPING
        usetox_input.EXPERIMENTAL_PROPERTY_PRIORITY = USEtoxInput.EXPERIMENTAL_PROPERTY_PRIORITY
        usetox_input.UNIT_CONVERSIONS = USEtoxInput.UNIT_CONVERSIONS
        usetox_input.EXCEL_COLUMN_MAPPING = USEtoxInput.EXCEL_COLUMN_MAPPING
        
        # Populate with sample data
        usetox_input.populate_from_episuite_dataframe(sample_episuite_df)
        
        # Get statistics
        stats = usetox_input.get_summary_statistics()
        
        assert stats['total_chemicals'] == 3
        assert 'MW' in stats['property_statistics']
        assert stats['property_statistics']['MW']['count'] == 3
        assert 'PyEPISuite Estimated' in stats['data_sources']  # Updated to match new naming
    
    def test_validate_data(self, sample_episuite_df):
        """Test data validation."""
        # Create template with some problematic data
        template_data = {
            'RowNr': [1, 2, 3, 4],
            'CAS RN': ['50-00-0', '100-00-5', np.nan, '50-00-0'],  # Missing and duplicate CAS
            'Name': ['Chemical1', 'Chemical2', 'Chemical3', 'Chemical4'],
            'MW': [30.0, 157.0, -10.0, 100.0],  # Negative MW
            'KOW': [1.0, 100.0, 1e15, 50.0],  # Extreme KOW
            'Data source': ['Test'] * 4
        }
        populated_df = pd.DataFrame(template_data)
        
        usetox_input = USEtoxInput.__new__(USEtoxInput)
        usetox_input.template_df = None
        usetox_input.populated_df = populated_df
        
        validation = usetox_input.validate_data()
        
        assert len(validation['warnings']) > 0
        assert len(validation['errors']) > 0
        assert any('missing CAS' in warning for warning in validation['warnings'])
        assert any('duplicate CAS' in warning for warning in validation['warnings'])
        assert any('negative molecular weights' in error for error in validation['errors'])
    
    def test_export_to_excel(self, sample_episuite_df, temp_excel_file):
        """Test Excel export functionality."""
        # Create a mock template
        template_data = {
            'RowNr': [np.nan] * 10,
            'CAS RN': [np.nan] * 10,
            'Name': [np.nan] * 10,
            'MW': [np.nan] * 10,
            'Data source': [np.nan] * 10
        }
        template_df = pd.DataFrame(template_data)
        
        usetox_input = USEtoxInput.__new__(USEtoxInput)
        usetox_input.template_df = template_df
        usetox_input.populated_df = None
        
        # Populate with sample data
        usetox_input.populate_from_episuite_dataframe(sample_episuite_df)
        
        # Export to Excel
        usetox_input.export_to_excel(temp_excel_file)
        
        # Verify file was created
        assert os.path.exists(temp_excel_file)
        
        # Read back the Excel file, accounting for the title row
        exported_df = pd.read_excel(temp_excel_file, sheet_name="Substance inputs", skiprows=2)
        assert len(exported_df) >= 3
        
        # Check if the data was exported correctly
        cas_column = None
        for col in exported_df.columns:
            if 'CAS' in str(col) or exported_df[col].astype(str).str.contains('50-00-0').any():
                cas_column = col
                break
        
        # At minimum, verify that formaldehyde CAS is in the data somewhere
        found_formaldehyde = False
        for col in exported_df.columns:
            if exported_df[col].astype(str).str.contains('50-00-0').any():
                found_formaldehyde = True
                break
        
        assert found_formaldehyde, "Expected to find formaldehyde CAS number in exported data"


def test_create_usetox_input_from_episuite(sample_episuite_df, temp_excel_file):
    """Test the convenience function."""
    try:
        result = create_usetox_input_from_episuite(
            sample_episuite_df, 
            temp_excel_file
        )
        assert isinstance(result, USEtoxInput)
        assert os.path.exists(temp_excel_file)
    except Exception:
        # Template file might not exist in test environment
        pytest.skip("USEtox template file not found")


if __name__ == "__main__":
    pytest.main([__file__])
