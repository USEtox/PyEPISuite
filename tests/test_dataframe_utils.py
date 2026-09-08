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
    _safe_get_parameter_value,
    episuite_experimental_to_dataframe,
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
    Parameter,
    ModuleError,
)
from pyepisuite.utils import get_dacite_config
import dacite


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
    
    # Arnot-Gobas estimates are titled rows in v1.1.0
    arnot_mock = Mock()
    arnot_mock.title = "Estimated Log BCF (upper trophic)"
    arnot_mock.value = 10.5
    arnot_mock.logValue = 1.02
    arnot_mock.unit = "L/kg wet-wt"
    result.bioconcentration.arnotGobasBcfBafEstimates = [arnot_mock]
    
    # Special handling for waterVolatilization parameters
    result.waterVolatilization.riverHalfLifeHours = 12.5
    result.waterVolatilization.lakeHalfLifeHours = 48.2
    result.waterVolatilization.parameters = Mock()
    # The API returns these either as a Value object or as a bare scalar,
    # so cover both shapes here.
    result.waterVolatilization.parameters.lakeCurrentVelocityMetersPerSecond = Mock(value=0.1)
    result.waterVolatilization.parameters.lakeWaterDepthMeters = Mock(value=2.0)
    result.waterVolatilization.parameters.lakeWindVelocityMetersPerSecond = Mock(value=3.0)
    result.waterVolatilization.parameters.riverCurrentVelocityMetersPerSecond = 0.5
    result.waterVolatilization.parameters.riverWaterDepthMeters = 1.0
    result.waterVolatilization.parameters.riverWindVelocityMetersPerSecond = 3.0
    
    # Hydrolysis rate constants live under `rates` in v1.1.0
    result.hydrolysis.disposition = "estimated"
    result.hydrolysis.rates = Mock()
    result.hydrolysis.rates.acidCatalyzedPrimary = Mock(value=0.1)
    result.hydrolysis.rates.baseCatalyzed = Mock(value=0.05)
    result.hydrolysis.rates.neutral = Mock(value=0.01)
    result.hydrolysis.rates.acidCatalyzedTrans = Mock(value=0.08)
    half_life_mock = Mock()
    half_life_mock.mechanism = "base-catalyzed"
    half_life_mock.pH = 7
    half_life_mock.value = 663.4
    half_life_mock.unit = "days"
    result.hydrolysis.halfLives = [half_life_mock]

    # BIOWIN reports calculatedValue, keyed by short name
    bio_model = Mock()
    bio_model.name = "Linear Model Prediction"
    bio_model.shortName = "biowin1"
    bio_model.calculatedValue = 0.75
    result.biodegradationRate.models = [bio_model]
    
    # Special handling for dermal permeability
    result.dermalPermeability.dermalPermeabilityCoefficient = 0.001
    result.dermalPermeability.dermalAbsorbedDose = 0.5
    result.dermalPermeability.dermalAbsorbedDosePerEvent = 0.1
    result.dermalPermeability.lagTimePerEventHours = 2.0
    result.dermalPermeability.timeToReachSteadyStateHours = 24.0
    
    # Fugacity: named compartments plus an estimates block
    result.fugacityModel.model = Mock()
    result.fugacityModel.model.estimates = Mock(
        persistenceHours=72.0, airPercent=40.0, waterPercent=35.0,
        soilPercent=20.0, sedimentPercent=5.0, selectedKoc=56.2,
    )
    result.fugacityModel.model.compartments = [
        Mock(name_=n, massPercent=p, halfLifeHours=h)
        for n, p, h in [('air', 40.0, 12.0), ('water', 35.0, 24.0),
                        ('soil', 20.0, 168.0), ('sediment', 5.0, 720.0)]
    ]
    # `name` is reserved by Mock(), so assign it after construction
    for compartment, name in zip(result.fugacityModel.model.compartments,
                                 ['air', 'water', 'soil', 'sediment']):
        compartment.name = name

    # Sewage treatment: a single estimates block of percentages
    result.sewageTreatmentModel.model = Mock()
    result.sewageTreatmentModel.model.estimates = Mock(
        totalRemovalPercent=85.5,
        totalSludgeAdsorptionPercent=10.2,
        totalAirPercent=5.3,
        totalBiodegradationPercent=70.0,
        finalEffluentPercent=14.5,
    )

    # No failed modules in the happy-path fixture
    result.errors = []

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
    
    def test_safe_get_parameter_value(self):
        """Test safe extraction of numeric values from bare scalars and Parameter objects."""
        # Bare scalar shape (the common case returned by the API)
        assert _safe_get_parameter_value(1.0) == 1.0
        assert _safe_get_parameter_value(0) == 0

        # Structured Parameter object shape
        param_obj = Mock()
        param_obj.value = 2.5
        assert _safe_get_parameter_value(param_obj) == 2.5

        # None
        assert _safe_get_parameter_value(None) is None

    def test_episuite_to_dataframe_handles_missing_nested_fields(self):
        """Result objects with null nested sections should not crash the conversion."""
        result = dacite.from_dict(
            ResultEPISuite,
            {
                "chemicalProperties": {"cas": "1"},
                "biodegradationRate": {"unit": "d"},
                "waterVolatilization": {"riverHalfLifeHours": 1.0},
            },
            config=get_dacite_config(),
        )
        df = episuite_to_dataframe([result])
        assert df.loc[0, 'cas'] == "1"

        result_empty = dacite.from_dict(ResultEPISuite, {}, config=get_dacite_config())
        df_empty = episuite_to_dataframe([result_empty])
        assert df_empty.loc[0, 'cas'] is None

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


class TestVersion110Schema:
    """Parse a real captured v1.1.0 response and check the migrated shapes.

    `data/sample/result.json` is an unmodified `/api/submit` response, so these
    tests fail if the models drift from what the API actually returns.
    """

    @staticmethod
    def _load():
        import json
        from pathlib import Path
        import dacite
        from pyepisuite.utils import get_dacite_config, normalize_response_keys

        path = Path(__file__).resolve().parents[1] / 'data' / 'sample' / 'result.json'
        with path.open() as fh:
            raw = json.load(fh)
        raw = raw[0] if isinstance(raw, list) else raw
        return raw, dacite.from_dict(
            data_class=ResultEPISuite,
            data=normalize_response_keys(raw),
            config=get_dacite_config(),
        )

    def test_parses_without_loss(self):
        """Every key in the response must map onto a declared field."""
        import dataclasses

        raw, result = self._load()
        from pyepisuite.utils import normalize_response_keys

        declared = {f.name for f in dataclasses.fields(ResultEPISuite)}
        unmapped = set(normalize_response_keys(raw)) - declared
        assert not unmapped, f"unmapped response keys: {sorted(unmapped)}"
        assert result.chemicalProperties.cas is not None
        assert result.chemicalProperties.name == "FORMALDEHYDE"

    def test_dotted_ecosar_keys_are_normalized(self):
        from pyepisuite.utils import normalize_response_keys

        raw, result = self._load()
        assert "ecosar.nonionic-surfactant" in raw
        assert "ecosar_nonionic_surfactant" in normalize_response_keys(raw)
        # Typed submodels do not run for a plain organic, so they are errors
        assert isinstance(result.ecosar_nonionic_surfactant, ModuleError)
        assert result.ecosar_nonionic_surfactant.code == "estimation_failed"

    def test_module_errors_are_discriminated_from_results(self):
        _, result = self._load()
        # A module that ran is its result type, never a ModuleError
        assert not isinstance(result.logKow, ModuleError)
        assert result.logKow.estimatedValue.value is not None
        # and the top-level list mirrors the per-module errors
        assert result.errors
        assert all(isinstance(e, ModuleError) for e in result.errors)

    def test_sewage_and_fugacity_estimates(self):
        _, result = self._load()
        sewage = result.sewageTreatmentModel.model.estimates
        assert sewage.totalRemovalPercent is not None
        assert sewage.finalEffluentPercent is not None

        fugacity = result.fugacityModel.model
        assert fugacity.estimates.persistenceHours is not None
        names = {c.name for c in fugacity.compartments}
        assert {'air', 'water', 'soil', 'sediment'} <= names

    def test_biowin_models_expose_calculated_value(self):
        _, result = self._load()
        models = result.biodegradationRate.models
        assert models
        assert all(m.calculatedValue is not None for m in models)
        assert any(m.shortName == 'biowin1' for m in models)

    def test_dataframe_columns_are_populated(self):
        _, result = self._load()
        df = episuite_to_dataframe([result])

        assert df.loc[0, 'sewage_total_removal_percent'] is not None
        assert df.loc[0, 'fugacity_persistence'] is not None
        assert df.loc[0, 'fugacity_air_half_life'] is not None
        assert df.loc[0, 'biodeg_biowin1'] is not None
        # Scalar-valued parameters must survive (see _safe_get_parameter_value)
        assert df.loc[0, 'lake_water_depth_m'] is not None
        # Failed modules are reported rather than silently dropped
        assert 'ecosar.nonionic-surfactant' in df.loc[0, 'failed_modules']

    def test_experimental_values_carry_provenance(self):
        _, result = self._load()
        df = episuite_experimental_to_dataframe([result])
        assert not df.empty
        assert {'source', 'source_database', 'temperature_c'} <= set(df.columns)
