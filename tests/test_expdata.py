# tests/test_expdata.py

import pytest
from pyepisuite.expdata import HenryData, BoilingPointData, MeltingPointData, VaporPressureData, SolubilityData

class TestHenryData:
    def test_HLC_valid_cas(self):
        """Test the HLC method with a valid CAS number."""
        henry = HenryData()
        valid_cas = "71-41-0"  # Example CAS number expected to be in the data
        
        result = henry.HLC(valid_cas)
        
        assert isinstance(result, dict), "Result should be a dictionary."
        assert result['CASRN'] == valid_cas, "CASRN should match the input CAS number."
        assert 'value' in result, "'value' key should be present in the result."
        assert 'unit' in result, "'unit' key should be present in the result."
        assert 'Temp (C)' in result, "'Temp (C)' key should be present in the result."
        assert 'type' in result, "'type' key should be present in the result."

    def test_HLC_invalid_cas(self):
        """Test the HLC method with an invalid CAS number."""
        henry = HenryData()
        invalid_cas = "000000-00-0"  # Example CAS number not present in the data
        
        with pytest.raises(IndexError):
            henry.HLC(invalid_cas)

    def test_HLC_return_structure(self):
        """Ensure that the HLC method returns the correct dictionary structure."""
        henry = HenryData()
        valid_cas = "71-41-0"
        
        result = henry.HLC(valid_cas)
        
        expected_keys = {'CASRN', 'name', 'value', 'unit', 'Temp (C)', 'type'}
        assert set(result.keys()) == expected_keys, f"Result keys {result.keys()} do not match expected {expected_keys}"
        assert isinstance(result['name'], str), "'name' should be a string."
        assert isinstance(result['value'], (float, int)), "'value' should be a float or int."
        assert isinstance(result['unit'], str), "'unit' should be a string."
        assert isinstance(result['Temp (C)'], (float, int)), "'Temp (C)' should be a float or int."
        assert result['type'] in {'EXP', 'EST'}, "'type' should be either 'EXP' or 'EST'."

class TestBoilingPointData:
    def test_boiling_point_valid_cas(self):
        """Test the boiling_point method with a valid CAS number."""
        bp = BoilingPointData()
        valid_cas = "64-17-5"  # Example CAS number for Ethanol
        
        result = bp.boiling_point(valid_cas)
        
        assert isinstance(result, dict), "Result should be a dictionary."
        assert result['CASRN'] == valid_cas, "CASRN should match the input CAS number."
        assert 'name' in result, "'name' key should be present in the result."
        assert 'value' in result, "'value' key should be present in the result."
        assert 'unit' in result, "'unit' key should be present in the result."
        assert result['unit'] == 'C', "Unit should be 'C'."

    def test_boiling_point_invalid_cas(self):
        """Test the boiling_point method with an invalid CAS number."""
        bp = BoilingPointData()
        invalid_cas = "000000-00-0"  # Example CAS number not present in the data
        
        with pytest.raises(IndexError):
            bp.boiling_point(invalid_cas)

    def test_boiling_point_return_structure(self):
        """Ensure that the boiling_point method returns the correct dictionary structure."""
        bp = BoilingPointData()
        valid_cas = "64-17-5"
        
        result = bp.boiling_point(valid_cas)
        
        expected_keys = {'CASRN', 'name', 'value', 'unit'}
        assert set(result.keys()) == expected_keys, f"Result keys {result.keys()} do not match expected {expected_keys}"
        assert isinstance(result['value'], (float, int, str)), "'value' should be a float or int."
        assert isinstance(result['unit'], str), "'unit' should be a string."

class TestMeltingPointData:
    def test_melting_point_valid_cas(self):
        """Test the melting_point method with a valid CAS number."""
        mp = MeltingPointData()
        valid_cas = "64-17-5"  # Example CAS number for Ethanol
        
        result = mp.melting_point(valid_cas)
        
        assert isinstance(result, dict), "Result should be a dictionary."
        assert result['CASRN'] == valid_cas, "CASRN should match the input CAS number."
        assert 'name' in result, "'name' key should be present in the result."
        assert 'value' in result, "'value' key should be present in the result."
        assert 'unit' in result, "'unit' key should be present in the result."
        assert result['unit'] == 'C', "Unit should be 'C'."

    def test_melting_point_invalid_cas(self):
        """Test the melting_point method with an invalid CAS number."""
        mp = MeltingPointData()
        invalid_cas = "000000-00-0"  # Example CAS number not present in the data
        
        with pytest.raises(IndexError):
            mp.melting_point(invalid_cas)

    def test_melting_point_return_structure(self):
        """Ensure that the melting_point method returns the correct dictionary structure."""
        mp = MeltingPointData()
        valid_cas = "64-17-5"
        
        result = mp.melting_point(valid_cas)
        
        expected_keys = {'CASRN', 'name', 'value', 'unit'}
        assert set(result.keys()) == expected_keys, f"Result keys {result.keys()} do not match expected {expected_keys}"
        assert isinstance(result['value'], (float, int, str)), "'value' should be a float or int."
        assert isinstance(result['unit'], str), "'unit' should be a string."

class TestVaporPressureData:
    def test_vapor_pressure_valid_cas(self):
        """Test the vapor_pressure method with a valid CAS number."""
        vp = VaporPressureData()
        valid_cas = "64-17-5"  # Example CAS number for Ethanol
        
        result = vp.vapor_pressure(valid_cas)
        
        assert isinstance(result, dict), "Result should be a dictionary."
        assert result['CASRN'] == valid_cas, "CASRN should match the input CAS number."
        assert 'name' in result, "'name' key should be present in the result."
        assert 'value' in result, "'value' key should be present in the result."
        assert 'unit' in result, "'unit' key should be present in the result."
        assert result['unit'] == 'mmHg', "Unit should be 'atm-m3/mole'."

    def test_vapor_pressure_invalid_cas(self):
        """Test the vapor_pressure method with an invalid CAS number."""
        vp = VaporPressureData()
        invalid_cas = "000000-00-0"  # Example CAS number not present in the data
        
        with pytest.raises(IndexError):
            vp.vapor_pressure(invalid_cas)

    def test_vapor_pressure_return_structure(self):
        """Ensure that the vapor_pressure method returns the correct dictionary structure.
        {'CASRN': '64-17-5',
        'name': 'Ethanol',
        'value': 59.3,
        'unit': 'mmHg',
        'Temp (C)': 20.0,
        'type': 'EXP' or 'EXT'}
        """
        vp = VaporPressureData()
        valid_cas = "64-17-5"
        
        result = vp.vapor_pressure(valid_cas)
        
        expected_keys = {'CASRN', 'name', 'value', 'unit', 'Temp (C)', 'type'}
        assert set(result.keys()) == expected_keys, f"Result keys {result.keys()} do not match expected {expected_keys}"
        assert isinstance(result['value'], (float, int, str)), "'value' should be a float or int."
        assert isinstance(result['unit'], str), "'unit' should be a string."

class TestSolubilityData:
    def test_solubility_valid_cas(self):
        """Test the solubility method with a valid CAS number."""
        sd = SolubilityData()
        valid_cas = "64-17-5"  # CAS number for Ethanol
        
        result = sd.solubility(valid_cas)
        
        assert isinstance(result, dict), "Result should be a dictionary."
        assert result['CASRN'] == valid_cas, "CASRN should match the input CAS number."
        assert 'name' in result, "'name' key should be present."
        assert 'class' in result, "'class' key should be present."
        assert 'logKow' in result, "'logKow' key should be present."
        assert 'water_solubility_mg_per_L' in result, "'water_solubility_mg_per_L' key should be present."
        assert 'log_mol_per_L' in result, "'log_mol_per_L' key should be present."
        assert isinstance(result['logKow'], (float, int)), "'logKow' should be a number."
        assert isinstance(result['water_solubility_mg_per_L'], (float, int)), "'water_solubility_mg_per_L' should be a number."
        assert isinstance(result['log_mol_per_L'], (float, int)), "'log_mol_per_L' should be a number."
        assert isinstance(result['name'], str), "'name' should be a string."
        assert isinstance(result['class'], str), "'class' should be a string."
    
    def test_solubility_invalid_cas(self):
        """Test the solubility method with an invalid CAS number."""
        sd = SolubilityData()
        invalid_cas = "000000-00-0"  # Invalid CAS number
        
        with pytest.raises(IndexError):
            sd.solubility(invalid_cas)
    
    def test_solubility_return_structure(self):
        """Ensure the solubility method returns the correct structure."""
        sd = SolubilityData()
        valid_cas = "64-17-5"
        
        result = sd.solubility(valid_cas)
        
        expected_keys = {
            'CASRN', 'name', 'class', 'logKow',
            'water_solubility_mg_per_L', 'log_mol_per_L'
        }
        assert set(result.keys()) == expected_keys, "Result keys do not match expected keys."
        for key in expected_keys:
            assert result[key] is not None, f"Value for '{key}' should not be None."