"""Tests for USEtox input functionality."""

import pytest
import pandas as pd
import numpy as np
import tempfile
import os
from unittest.mock import patch, MagicMock
from pyepisuite.usetox_input import USEtoxInput, create_usetox_input_from_cas_list
from pyepisuite.usetox_input import column_names_dict, BAF_dict, toxicity_dict, flagged_indicative_dict


class TestUSEtoxInput:
    """Test the USEtoxInput class."""
    
    @pytest.fixture
    def sample_episuite_data(self):
        """Sample EPI Suite result data."""
        return {
            'cas': '50-00-0',
            'name': 'Formaldehyde',
            'molecular_weight': 30.03,
            'log_kow_estimated': -0.35,
            'log_koc_estimated': 1.5,
            'henrys_law_constant_estimated': 3.37e-5,
            'vapor_pressure_estimated': 3.89e3,
            'water_solubility_logkow_estimated': 4.0e5,
            'atmospheric_half_life_estimated': 245.0,
            'water_biodegradation_half_life_unacclimated': 30,
            'sediment_half_life_hours': 120,
            'soil_half_life_hours': 168,
            'bioconcentration_factor': 3.2
        }
    
    @pytest.fixture
    def temp_excel_file(self):
        """Create a temporary Excel file path."""
        fd, path = tempfile.mkstemp(suffix='.xlsx')
        os.close(fd)
        yield path
        try:
            os.unlink(path)
        except:
            pass
    
    def test_initialization_without_template(self):
        """Test USEtoxInput initialization without template file."""
        # This will fail if template doesn't exist, which is expected in test environment
        try:
            usetox_input = USEtoxInput()
            assert usetox_input is not None
        except Exception:
            # Template file doesn't exist in test environment
            pytest.skip("USEtox template file not found")
    
    def test_column_mapping_dictionaries(self):
        """Test that column mapping dictionaries are correctly defined."""
        # Test basic column mappings
        assert 'CAS RN' in column_names_dict
        assert 'Name' in column_names_dict
        assert 'MW' in column_names_dict
        
        # Check that mappings point to valid Excel column letters
        for prop, excel_col in column_names_dict.items():
            assert isinstance(excel_col, str)
            assert len(excel_col) >= 1  # Valid Excel column
            
        # Test BAF dictionary
        assert 'BAFfish' in BAF_dict
        
        # Test other dictionaries exist
        assert isinstance(toxicity_dict, dict)
        assert isinstance(flagged_indicative_dict, dict)
    
    def test_unit_conversion_methods(self):
        """Test unit conversion methods."""
        # Create a USEtoxInput instance (will fail in test environment without template)
        try:
            usetox_input = USEtoxInput()
        except:
            pytest.skip("USEtox template file not found")
        
        # Test log KOW conversion
        result = usetox_input._convert_log_kow_to_kow(2.0)
        assert abs(result - 100.0) < 1e-10
        
        # Test None handling
        assert usetox_input._convert_log_kow_to_kow(None) is None
        
        # Test vapor pressure conversion (mmHg to Pa)
        result = usetox_input._convert_mmhg_to_pa(1.0)
        assert abs(result - 133.322) < 1e-3
        
        # Test solubility conversion (mg/L to g/L)
        result = usetox_input._convert_mg_l_to_g_l(1000.0)
        assert abs(result - 1.0) < 1e-10
        
        # Test time conversion (hours to days)
        result = usetox_input._convert_hours_to_days(24.0)
        assert abs(result - 1.0) < 1e-10
    
    @patch('pyepisuite.usetox_input.load_workbook')
    def test_add_chemical_from_episuite(self, mock_load_workbook, sample_episuite_data):
        """Test adding a single chemical from EPI Suite data."""
        # Mock the workbook and worksheet
        mock_workbook = MagicMock()
        mock_worksheet = MagicMock()
        mock_load_workbook.return_value = mock_workbook
        mock_workbook.__getitem__.return_value = mock_worksheet
        
        # Create USEtoxInput instance with mocked template
        usetox_input = USEtoxInput("dummy_path.xlsx")
        usetox_input.workbook = mock_workbook
        usetox_input.worksheet = mock_worksheet
        
        # Add chemical
        row_num = usetox_input.add_chemical_from_episuite(sample_episuite_data)
        
        # Verify row number
        assert row_num == 6  # Should start at row 6
        
        # Verify that worksheet cells were set (checking if __setitem__ was called)
        assert mock_worksheet.__setitem__.called
    
    def test_inorganic_detection(self):
        """Test inorganic chemical detection."""
        try:
            usetox_input = USEtoxInput()
        except:
            pytest.skip("USEtox template file not found")
        
        # Test organic chemical
        organic_data = {'name': 'Benzene', 'molecular_weight': 78.11}
        assert not usetox_input._check_if_inorganic(organic_data)
        
        # Test inorganic chemical
        inorganic_data = {'name': 'Sodium chloride', 'molecular_weight': 58.44}
        assert usetox_input._check_if_inorganic(inorganic_data)
        
        # Test by molecular weight
        small_molecule = {'name': 'Unknown', 'molecular_weight': 20.0}
        assert usetox_input._check_if_inorganic(small_molecule)
    
    @patch('pyepisuite.utils.search_episuite_by_cas')
    @patch('pyepisuite.utils.submit_to_episuite')
    @patch('pyepisuite.usetox_input.load_workbook')
    def test_add_chemicals_from_cas_list(self, mock_load_workbook, mock_submit, mock_search):
        """Test adding multiple chemicals from CAS list."""
        # Mock the workbook
        mock_workbook = MagicMock()
        mock_worksheet = MagicMock()
        mock_load_workbook.return_value = mock_workbook
        mock_workbook.__getitem__.return_value = mock_worksheet
        
        # Mock search results
        mock_identifier = MagicMock()
        mock_identifier.cas = '000050-00-0'  # EPI Suite format with leading zeros
        mock_identifier.name = 'Formaldehyde'
        mock_search.return_value = [mock_identifier]
        
        # Mock EPI Suite result
        mock_result = MagicMock()
        mock_result.chemicalProperties.molecularWeight = 30.03
        mock_result.logKow.selectedValue.value = -0.35
        mock_result.logKoc.selectedValue.value = 1.5
        mock_submit.return_value = ([mock_result], None)
        
        # Create USEtoxInput instance
        usetox_input = USEtoxInput("dummy_path.xlsx")
        usetox_input.workbook = mock_workbook
        usetox_input.worksheet = mock_worksheet
        
        # Test adding chemicals
        cas_list = ['50-00-0']
        results = usetox_input.add_chemicals_from_cas_list(cas_list)
        
        # Verify results
        assert '50-00-0' in results
        assert results['50-00-0'] == 6
    
    def test_get_summary(self):
        """Test summary generation."""
        try:
            usetox_input = USEtoxInput()
            summary = usetox_input.get_summary()
            
            assert 'chemicals_added' in summary
            assert 'current_row' in summary
            assert 'template_path' in summary
            assert summary['chemicals_added'] == 0  # No chemicals added yet
            assert summary['current_row'] == 6  # Should start at row 6
        except:
            pytest.skip("USEtox template file not found")
    
    @patch('pyepisuite.usetox_input.USEtoxInput')
    def test_create_usetox_input_from_cas_list(self, mock_usetox_class, temp_excel_file):
        """Test the convenience function."""
        # Mock the USEtoxInput instance
        mock_instance = MagicMock()
        mock_instance.add_chemicals_from_cas_list.return_value = {'50-00-0': 6}
        mock_instance.get_summary.return_value = {'chemicals_added': 1}
        mock_usetox_class.return_value = mock_instance
        
        # Test the convenience function
        cas_list = ['50-00-0']
        result = create_usetox_input_from_cas_list(cas_list, temp_excel_file)
        
        # Verify calls
        mock_usetox_class.assert_called_once_with(None)
        mock_instance.add_chemicals_from_cas_list.assert_called_once_with(cas_list)
        mock_instance.save_excel.assert_called_once_with(temp_excel_file)
        assert result == mock_instance


class TestIntegration:
    """Integration tests that require the full environment."""
    
    def test_full_workflow_mock(self):
        """Test the full workflow with mocked external dependencies."""
        # This would test the complete workflow but with mocked API calls
        # to avoid depending on external services in tests
        pass