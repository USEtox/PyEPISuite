"""
Tests for DataFrame utilities in PyEPISuite.
"""

import pytest
import pandas as pd
from unittest.mock import Mock, patch
from pyepisuite.dataframe_utils import (
    episuite_to_dataframe,
    ecosar_to_dataframe,
    combine_episuite_ecosar_dataframes,
    create_summary_statistics,
    _safe_get_estimated_value,
    _safe_get_estimated_units,
)
from pyepisuite.models import (
    ResultEPISuite, 
    ResultEcoSAR, 
    ChemicalProperties,
    Parameters,
    LogKowResponse,
    logKowEstimatedValue,
    KowModel,
    SelectedValue,
    EcosarParameters,
    ModelResult,
    Parameter
)


def create_mock_episuite_result():
    """Create a mock EPI Suite result for testing."""
    # Create mock chemical properties
    chem_props = Mock(spec=ChemicalProperties)
    chem_props.cas = "50-00-0"
    chem_props.name = "Formaldehyde"
    chem_props.systematicName = "Formaldehyde"
    chem_props.smiles = "C=O"
    chem_props.molecularWeight = 30.026
    chem_props.molecularFormula = "CH2O"
    chem_props.organic = True
    chem_props.organicAcid = False
    chem_props.aminoAcid = False
    chem_props.nonStandardMetal = False
    
    # Create mock parameters
    params = Mock(spec=Parameters)
    params.cas = "50-00-0"
    
    # Create mock LogKow response
    estimated_value = Mock(spec=logKowEstimatedValue)
    estimated_value.value = 0.35
    estimated_value.units = "dimensionless"
    
    selected_value = Mock(spec=SelectedValue)
    selected_value.value = 0.35
    selected_value.units = "dimensionless"
    
    log_kow = Mock(spec=LogKowResponse)
    log_kow.estimatedValue = estimated_value
    log_kow.experimentalValues = []
    log_kow.selectedValue = selected_value
    
    # Create main result object
    result = Mock(spec=ResultEPISuite)
    result.parameters = params
    result.chemicalProperties = chem_props
    result.logKow = log_kow
    
    # Mock other required attributes
    for attr in ['meltingPoint', 'boilingPoint', 'vaporPressure', 'waterSolubilityFromLogKow',
                 'waterSolubilityFromWaterNt', 'henrysLawConstant', 'logKoa', 'logKoc',
                 'atmosphericHalfLife', 'aerosolAdsorptionFraction', 'hydrocarbonBiodegradationRate',
                 'waterVolatilization', 'dermalPermeability', 'fugacityModel', 'hydrolysis', 'biodegradationRate',
                 'sewageTreatmentModel']:
        mock_attr = Mock()
        mock_attr.estimatedValue.value = 1.0
        mock_attr.estimatedValue.units = "test_unit"
        mock_attr.estimatedValue.model = []
        mock_attr.selectedValue.value = 1.0
        mock_attr.selectedValue.units = "test_unit"
        setattr(result, attr, mock_attr)
    
    # Special handling for atmosphericHalfLife with additional attributes
    result.atmosphericHalfLife.estimatedHydroxylRadicalReactionRateConstant = Mock()
    result.atmosphericHalfLife.estimatedHydroxylRadicalReactionRateConstant.value = 1.5e-12
    result.atmosphericHalfLife.estimatedHydroxylRadicalReactionRateConstant.units = "cm3/molecule-sec"
    result.atmosphericHalfLife.estimatedOzoneReactionRateConstant = Mock()
    result.atmosphericHalfLife.estimatedOzoneReactionRateConstant.value = 2.0e-18
    result.atmosphericHalfLife.estimatedOzoneReactionRateConstant.units = "cm3/molecule-sec"
    
    # Special handling for bioconcentration
    result.bioconcentration = Mock()
    result.bioconcentration.bioconcentrationFactor = 10.5
    result.bioconcentration.logBioconcentrationFactor = 1.02
    result.bioconcentration.bioaccumulationFactor = 15.2
    result.bioconcentration.logBioaccumulationFactor = 1.18
    result.bioconcentration.biotransformationHalfLife = 24.0
    result.bioconcentration.experimentalBioTransformationRate = 0.029
    
    # Mock trophic level data
    trophic_mock = Mock()
    trophic_mock.trophicLevel = 2
    trophic_mock.bioaccumulationFactor = 15.2
    trophic_mock.bioconcentrationFactor = 10.5
    trophic_mock.unit = "L/kg"
    result.bioconcentration.arnotGobasBcfBafEstimates = [trophic_mock]
    
    # Special handling for waterVolatilization parameters
    result.waterVolatilization.riverHalfLifeHours = 12.5
    result.waterVolatilization.lakeHalfLifeHours = 48.2
    result.waterVolatilization.parameters = Mock()
    result.waterVolatilization.parameters.lakeCurrentVelocityMetersPerSecond = Mock(value=0.1)
    result.waterVolatilization.parameters.lakeWaterDepthMeters = Mock(value=2.0)
    result.waterVolatilization.parameters.lakeWindVelocityMetersPerSecond = Mock(value=3.0)
    result.waterVolatilization.parameters.riverCurrentVelocityMetersPerSecond = Mock(value=0.5)
    result.waterVolatilization.parameters.riverWaterDepthMeters = Mock(value=1.0)
    result.waterVolatilization.parameters.riverWindVelocityMetersPerSecond = Mock(value=3.0)
    
    # Special handling for hydrolysis
    result.hydrolysis.acidCatalyzedRateConstant = 0.1
    result.hydrolysis.baseCatalyzedRateConstant = 0.05
    result.hydrolysis.neutralRateConstant = 0.01
    result.hydrolysis.acidCatalyzedRateConstantForTransIsomer = 0.08
    
    # Special handling for biodegradation models
    bio_model = Mock()
    bio_model.name = "Linear Model Prediction"
    bio_model.value = 0.75
    result.biodegradationRate.models = [bio_model]
    
    # Special handling for dermal permeability
    result.dermalPermeability.dermalPermeabilityCoefficient = 0.001
    result.dermalPermeability.dermalAbsorbedDose = 0.5
    result.dermalPermeability.dermalAbsorbedDosePerEvent = 0.1
    result.dermalPermeability.lagTimePerEventHours = 2.0
    result.dermalPermeability.timeToReachSteadyStateHours = 24.0
    
    # Special handling for fugacity model
    result.fugacityModel.model = Mock()
    result.fugacityModel.model.Persistence = 72.0
    result.fugacityModel.model.HalfLifeArray = [12.0, 24.0, 168.0, 720.0]  # air, water, soil, sediment
    
    # Special handling for sewage treatment model
    result.sewageTreatmentModel.model = Mock()
    result.sewageTreatmentModel.model.TotalRemoval = Mock()
    result.sewageTreatmentModel.model.TotalRemoval.Percent = 85.5
    result.sewageTreatmentModel.model.TotalSludge = Mock()
    result.sewageTreatmentModel.model.TotalSludge.Percent = 10.2
    result.sewageTreatmentModel.model.TotalAir = Mock()
    result.sewageTreatmentModel.model.TotalAir.Percent = 5.3
    result.sewageTreatmentModel.model.TotalBiodeg = Mock()
    result.sewageTreatmentModel.model.TotalBiodeg.Percent = 70.0
    result.sewageTreatmentModel.model.FinalEffluent = Mock()
    result.sewageTreatmentModel.model.FinalEffluent.Percent = 14.5
    
    return result


def create_mock_ecosar_result():
    """Create a mock EcoSAR result for testing."""
    # Create mock parameters
    params = Mock(spec=EcosarParameters)
    params.cas = "50-00-0"
    params.smiles = "C=O"
    params.logKow = Mock(spec=Parameter)
    params.logKow.value = 0.35
    params.waterSolubility = Mock(spec=Parameter)
    params.waterSolubility.value = 400000.0
    params.meltingPoint = Mock(spec=Parameter)
    params.meltingPoint.value = -92.0
    
    # Create mock model result
    model_result = Mock(spec=ModelResult)
    model_result.qsarClass = "Neutral Organics"
    model_result.organism = "fish"
    model_result.duration = "acute"
    model_result.endpoint = "LC50"
    model_result.concentration = 100.0
    model_result.maxLogKow = 8.0
    model_result.flags = []
    
    # Create main result object
    result = Mock(spec=ResultEcoSAR)
    result.parameters = params
    result.modelResults = [model_result]
    result.output = "Test output"
    result.alerts = None
    
    return result


class TestDataFrameUtils:
    """Test class for DataFrame utility functions."""
    
    def test_episuite_to_dataframe_single_result(self):
        """Test converting a single EPI Suite result to DataFrame."""
        mock_result = create_mock_episuite_result()
        
        df = episuite_to_dataframe([mock_result])
        
        assert len(df) == 1
        assert df.iloc[0]['cas'] == "50-00-0"
        assert df.iloc[0]['name'] == "Formaldehyde"
        assert df.iloc[0]['log_kow_estimated'] == 0.35
        assert 'cas' in df.columns
        assert 'name' in df.columns
        assert 'log_kow_estimated' in df.columns
    
    def test_episuite_to_dataframe_empty_list(self):
        """Test converting empty list returns empty DataFrame."""
        df = episuite_to_dataframe([])
        
        assert len(df) == 0
        assert isinstance(df, pd.DataFrame)
    
    def test_ecosar_to_dataframe_single_result(self):
        """Test converting a single EcoSAR result to DataFrame."""
        mock_result = create_mock_ecosar_result()
        
        df = ecosar_to_dataframe([mock_result])
        
        assert len(df) == 1
        assert df.iloc[0]['cas'] == "50-00-0"
        assert df.iloc[0]['organism'] == "fish"
        assert df.iloc[0]['concentration'] == 100.0
        assert 'cas' in df.columns
        assert 'qsar_class' in df.columns
        assert 'concentration' in df.columns
    
    def test_ecosar_to_dataframe_empty_list(self):
        """Test converting empty EcoSAR list returns empty DataFrame."""
        df = ecosar_to_dataframe([])
        
        assert len(df) == 0
        assert isinstance(df, pd.DataFrame)
    
    def test_combine_dataframes(self):
        """Test combining EPI Suite and EcoSAR DataFrames."""
        epi_mock = create_mock_episuite_result()
        ecosar_mock = create_mock_ecosar_result()
        
        epi_df = episuite_to_dataframe([epi_mock])
        ecosar_df = ecosar_to_dataframe([ecosar_mock])
        
        combined = combine_episuite_ecosar_dataframes(epi_df, ecosar_df)
        
        assert len(combined) == 1
        assert 'cas' in combined.columns
        assert 'log_kow_estimated' in combined.columns
        # Check that EcoSAR summary columns are added
        ecosar_cols = [col for col in combined.columns if 'organism' in col or 'concentration' in col]
        assert len(ecosar_cols) > 0
    
    def test_create_summary_statistics(self):
        """Test creating summary statistics."""
        # Create a test DataFrame with numeric columns
        test_data = {
            'numeric1': [1.0, 2.0, 3.0, 4.0, 5.0],
            'numeric2': [10.0, 20.0, 30.0, 40.0, 50.0],
            'text': ['a', 'b', 'c', 'd', 'e']
        }
        df = pd.DataFrame(test_data)
        
        stats = create_summary_statistics(df)
        
        assert isinstance(stats, pd.DataFrame)
        assert 'numeric1' in stats.columns
        assert 'numeric2' in stats.columns
        assert 'text' not in stats.columns  # Should exclude non-numeric columns
        assert stats.loc['mean', 'numeric1'] == 3.0
        assert stats.loc['mean', 'numeric2'] == 30.0
    
    def test_create_summary_statistics_with_specified_columns(self):
        """Test creating summary statistics with specified columns."""
        test_data = {
            'col1': [1.0, 2.0, 3.0],
            'col2': [10.0, 20.0, 30.0],
            'col3': [100.0, 200.0, 300.0]
        }
        df = pd.DataFrame(test_data)
        
        stats = create_summary_statistics(df, ['col1', 'col2'])
        
        assert 'col1' in stats.columns
        assert 'col2' in stats.columns
        assert 'col3' not in stats.columns
    
    def test_safe_get_estimated_value(self):
        """Test safe extraction of estimated values."""
        # Test with valid object
        mock_obj = Mock()
        mock_obj.estimatedValue.value = 42.0
        assert _safe_get_estimated_value(mock_obj) == 42.0
        
        # Test with None
        assert _safe_get_estimated_value(None) is None
        
        # Test with missing attribute
        mock_obj_invalid = Mock()
        del mock_obj_invalid.estimatedValue
        assert _safe_get_estimated_value(mock_obj_invalid) is None
    
    def test_safe_get_estimated_units(self):
        """Test safe extraction of units."""
        # Test with valid object
        mock_obj = Mock()
        mock_obj.estimatedValue.units = "mg/L"
        assert _safe_get_estimated_units(mock_obj) == "mg/L"
        
        # Test with None
        assert _safe_get_estimated_units(None) is None
        
        # Test with missing attribute
        mock_obj_invalid = Mock()
        del mock_obj_invalid.estimatedValue
        assert _safe_get_estimated_units(mock_obj_invalid) is None
    
    def test_export_to_excel(self):
        """Test Excel export functionality."""
        from pyepisuite.dataframe_utils import export_to_excel
        import tempfile
        import os
        
        # Create test data
        test_data = {
            'Sheet1': pd.DataFrame({'col1': [1, 2, 3]}),
            'Sheet2': pd.DataFrame({'col2': [4, 5, 6]})
        }
        
        # Use a temporary file
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            temp_filename = tmp.name
        
        try:
            # Call the function
            export_to_excel(test_data, temp_filename)
            
            # Verify file was created
            assert os.path.exists(temp_filename)
            
            # Verify content by reading back
            with pd.ExcelFile(temp_filename) as xls:
                assert 'Sheet1' in xls.sheet_names
                assert 'Sheet2' in xls.sheet_names
                
                sheet1 = pd.read_excel(xls, 'Sheet1')
                sheet2 = pd.read_excel(xls, 'Sheet2')
                
                assert len(sheet1) == 3
                assert len(sheet2) == 3
                assert 'col1' in sheet1.columns
                assert 'col2' in sheet2.columns
        
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)


if __name__ == "__main__":
    pytest.main([__file__])
