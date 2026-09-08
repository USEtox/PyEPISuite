"""
DataFrame conversion utilities for PyEPISuite results.

This module provides functions to convert EPI Suite and EcoSAR results
to pandas DataFrames for easier data analysis and manipulation.
"""

import re
import pandas as pd
from typing import List, Dict, Any, Optional, Union
from .models import ResultEPISuite, ResultEcoSAR, ExperimentalValue, Parameter, ModuleError


def episuite_to_dataframe(results: List[ResultEPISuite]) -> pd.DataFrame:
    """
    Convert a list of EPI Suite results to a pandas DataFrame.
    
    This function extracts the main properties and estimated values from
    EPI Suite results and organizes them into a tabular format suitable
    for analysis.
    
    Parameters:
        results (List[ResultEPISuite]): List of EPI Suite result objects
        
    Returns:
        pd.DataFrame: DataFrame with chemicals as rows and properties as columns
        
    Example:
        >>> from pyepisuite.utils import search_episuite_by_cas, submit_to_episuite
        >>> from pyepisuite.dataframe_utils import episuite_to_dataframe
        >>> 
        >>> cas_list = ["50-00-0", "100-00-5"]
        >>> ids = search_episuite_by_cas(cas_list)
        >>> epi_results, _ = submit_to_episuite(ids)
        >>> df = episuite_to_dataframe(epi_results)
        >>> print(df.head())
    """
    data = []
    
    for result in results:
        row = {}
        
        # Chemical identification
        chem_props = getattr(result, 'chemicalProperties', None)
        row['cas'] = getattr(chem_props, 'cas', None)
        row['name'] = getattr(chem_props, 'name', None)
        row['systematic_name'] = getattr(chem_props, 'systematicName', None)
        row['smiles'] = getattr(chem_props, 'smiles', None)
        row['molecular_weight'] = getattr(chem_props, 'molecularWeight', None)
        row['molecular_formula'] = getattr(chem_props, 'molecularFormula', None)
        row['is_organic'] = getattr(chem_props, 'organic', None)
        row['is_organic_acid'] = getattr(chem_props, 'organicAcid', None)
        row['is_amino_acid'] = getattr(chem_props, 'aminoAcid', None)
        row['is_non_standard_metal'] = getattr(chem_props, 'nonStandardMetal', None)

        # Modules the API could not estimate. Without this the failures are
        # invisible: the module's columns are simply absent or empty.
        failed = [e.module for e in (getattr(result, 'errors', None) or [])
                  if getattr(e, 'module', None)]
        row['failed_modules'] = ', '.join(sorted(failed)) if failed else None

        # Physical and chemical properties - estimated values
        row['log_kow_estimated'] = _safe_get_estimated_value(result.logKow)
        row['log_kow_units'] = _safe_get_estimated_units(result.logKow)
        
        row['melting_point_estimated'] = _safe_get_estimated_value(result.meltingPoint)
        row['melting_point_units'] = _safe_get_estimated_units(result.meltingPoint)
        
        row['boiling_point_estimated'] = _safe_get_estimated_value(result.boilingPoint)
        row['boiling_point_units'] = _safe_get_estimated_units(result.boilingPoint)
        
        # Safely extract vapor pressure model data
        if (hasattr(result, 'vaporPressure') and result.vaporPressure and 
            hasattr(result.vaporPressure, 'estimatedValue') and result.vaporPressure.estimatedValue and
            hasattr(result.vaporPressure.estimatedValue, 'model') and result.vaporPressure.estimatedValue.model):
            for vp in result.vaporPressure.estimatedValue.model:
                if hasattr(vp, 'type') and vp.type == 'Selected':
                    continue
                if hasattr(vp, 'type') and hasattr(vp, 'mmHg'):
                    row[f'vapor_pressure_{vp.type}_estimated'] = vp.mmHg
        types = ['Antoine', 'Grain', 'Mackay', 'SubCooled']
        for t in types:
            key = f'vapor_pressure_{t}_estimated'
            if key not in row.keys():
                row[key] = None
        
        row['vapor_pressure_estimated'] = _safe_get_estimated_value(result.vaporPressure)
        row['vapor_pressure_units'] = _safe_get_estimated_units(result.vaporPressure)
        
        row['water_solubility_logkow_estimated'] = _safe_get_estimated_value(result.waterSolubilityFromLogKow)
        row['water_solubility_logkow_units'] = _safe_get_estimated_units(result.waterSolubilityFromLogKow)
        
        row['water_solubility_waternt_estimated'] = _safe_get_estimated_value(result.waterSolubilityFromWaterNt)
        row['water_solubility_waternt_units'] = _safe_get_estimated_units(result.waterSolubilityFromWaterNt)
        
        # Henry's law constant from different models
        if (hasattr(result, 'henrysLawConstant') and result.henrysLawConstant and 
            hasattr(result.henrysLawConstant, 'estimatedValue') and result.henrysLawConstant.estimatedValue and
            hasattr(result.henrysLawConstant.estimatedValue, 'model') and result.henrysLawConstant.estimatedValue.model):
            for hlc in result.henrysLawConstant.estimatedValue.model:
                if getattr(hlc, 'name', None) is not None:
                    row[f'henrys_law_constant_{hlc.name}_estimated'] = hlc.hlcAtmM3PerMol
        types = ['VP/WSOL', 'Bond', 'Group']
        for t in types:
            key = f'henrys_law_constant_{t}_estimated'
            if key not in row.keys():
                row[key] = None

        row['henrys_law_constant_estimated'] = _safe_get_estimated_value(result.henrysLawConstant)
        row['henrys_law_constant_units'] = _safe_get_estimated_units(result.henrysLawConstant)
        
        row['log_koa_estimated'] = _safe_get_estimated_value(result.logKoa)
        row['log_koa_units'] = _safe_get_estimated_units(result.logKoa)
        
        row['log_koc_estimated'] = _safe_get_estimated_value(result.logKoc)
        row['log_koc_units'] = _safe_get_estimated_units(result.logKoc)
        
        # Environmental fate properties
        row['atmospheric_half_life_estimated'] = _safe_get_estimated_value(result.atmosphericHalfLife)
        row['atmospheric_half_life_units'] = _safe_get_estimated_units(result.atmosphericHalfLife)
        
        # Additional atmospheric half-life properties
        if hasattr(result.atmosphericHalfLife, 'estimatedHydroxylRadicalReactionRateConstant'):
            row['hydroxyl_radical_rate_constant'] = _safe_get_value_direct(result.atmosphericHalfLife.estimatedHydroxylRadicalReactionRateConstant)
            row['hydroxyl_radical_rate_constant_units'] = _safe_get_units_direct(result.atmosphericHalfLife.estimatedHydroxylRadicalReactionRateConstant)
        
        if hasattr(result.atmosphericHalfLife, 'estimatedOzoneReactionRateConstant'):
            row['ozone_reaction_rate_constant'] = _safe_get_value_direct(result.atmosphericHalfLife.estimatedOzoneReactionRateConstant)
            row['ozone_reaction_rate_constant_units'] = _safe_get_units_direct(result.atmosphericHalfLife.estimatedOzoneReactionRateConstant)
        
        row['aerosol_adsorption_fraction_estimated'] = _safe_get_estimated_value(result.aerosolAdsorptionFraction)
        row['aerosol_adsorption_fraction_units'] = _safe_get_estimated_units(result.aerosolAdsorptionFraction)
        row['aerosol_adsorption_fraction_selected'] = _safe_get_selected_value(result.aerosolAdsorptionFraction)
        
        row['hydrocarbon_biodegradation_rate_estimated'] = _safe_get_estimated_value(result.hydrocarbonBiodegradationRate)
        row['hydrocarbon_biodegradation_rate_units'] = _safe_get_estimated_units(result.hydrocarbonBiodegradationRate)
        
        # Bioconcentration
        if hasattr(result.bioconcentration, 'bioconcentrationFactor'):
            row['bioconcentration_factor'] = result.bioconcentration.bioconcentrationFactor
            row['log_bioconcentration_factor'] = result.bioconcentration.logBioconcentrationFactor
            row['bioaccumulation_factor'] = result.bioconcentration.bioaccumulationFactor
            row['log_bioaccumulation_factor'] = result.bioconcentration.logBioaccumulationFactor
            row['biotransformation_half_life'] = result.bioconcentration.biotransformationHalfLife
            row['experimental_biotransformation_rate'] = result.bioconcentration.experimentalBioTransformationRate
            
            # Arnot-Gobas estimates are reported as titled rows, one column each
            for estimate in getattr(result.bioconcentration, 'arnotGobasBcfBafEstimates', None) or []:
                title = getattr(estimate, 'title', None)
                if not title:
                    continue
                key = _column_name(title)
                row[f'arnot_gobas_{key}'] = estimate.value
                row[f'arnot_gobas_{key}_log'] = estimate.logValue
                row[f'arnot_gobas_{key}_unit'] = estimate.unit

        # Hydrolysis - the flat rate constants are nested under `rates` in v1.1.0.
        # `disposition` says whether the compound has hydrolyzable functions at
        # all, which distinguishes "no estimate" from "estimated as zero".
        hydrolysis = getattr(result, 'hydrolysis', None)
        row['hydrolysis_disposition'] = getattr(hydrolysis, 'disposition', None)
        hydrolysis_rates = getattr(hydrolysis, 'rates', None)
        if hydrolysis_rates is not None:
            row['acid_catalyzed_rate_constant'] = _safe_get_value_direct(hydrolysis_rates.acidCatalyzedPrimary)
            row['base_catalyzed_rate_constant'] = _safe_get_value_direct(hydrolysis_rates.baseCatalyzed)
            row['neutral_rate_constant'] = _safe_get_value_direct(hydrolysis_rates.neutral)
            row['acid_catalyzed_trans_isomer_rate'] = _safe_get_value_direct(hydrolysis_rates.acidCatalyzedTrans)

        # Half-lives are reported per mechanism and pH
        for half_life in getattr(hydrolysis, 'halfLives', None) or []:
            mechanism = getattr(half_life, 'mechanism', None)
            if mechanism is None:
                continue
            suffix = _column_name(mechanism)
            if getattr(half_life, 'pH', None) is not None:
                suffix = f'{suffix}_ph{half_life.pH}'
            row[f'hydrolysis_half_life_{suffix}'] = half_life.value
            row[f'hydrolysis_half_life_{suffix}_unit'] = half_life.unit

        # Biodegradation models - get summary of main models
        biodeg_models = getattr(getattr(result, 'biodegradationRate', None), 'models', None) or []
        for model in biodeg_models:
            # Prefer the BIOWIN short name ("biowin1"); fall back to the long name.
            label = getattr(model, 'shortName', None) or getattr(model, 'name', None)
            if label is None:
                continue
            row[f'biodeg_{_column_name(label)}'] = model.calculatedValue
        
        # Water volatilization
        if hasattr(result.waterVolatilization, 'riverHalfLifeHours'):
            row['river_half_life_hours'] = result.waterVolatilization.riverHalfLifeHours
            row['lake_half_life_hours'] = result.waterVolatilization.lakeHalfLifeHours
            
            # Water volatilization parameters
            params = getattr(result.waterVolatilization, 'parameters', None)
            if params is not None:
                row['lake_current_velocity_ms'] = _safe_get_parameter_value(params.lakeCurrentVelocityMetersPerSecond)
                row['lake_water_depth_m'] = _safe_get_parameter_value(params.lakeWaterDepthMeters)
                row['lake_wind_velocity_ms'] = _safe_get_parameter_value(params.lakeWindVelocityMetersPerSecond)
                row['river_current_velocity_ms'] = _safe_get_parameter_value(params.riverCurrentVelocityMetersPerSecond)
                row['river_water_depth_m'] = _safe_get_parameter_value(params.riverWaterDepthMeters)
                row['river_wind_velocity_ms'] = _safe_get_parameter_value(params.riverWindVelocityMetersPerSecond)
        
        # Sewage treatment model - get key removal percentages
        stm = getattr(getattr(result, 'sewageTreatmentModel', None), 'model', None)
        stm_estimates = getattr(stm, 'estimates', None)
        if stm_estimates is not None:
            row['sewage_total_removal_percent'] = stm_estimates.totalRemovalPercent
            row['sewage_sludge_percent'] = stm_estimates.totalSludgeAdsorptionPercent
            row['sewage_air_percent'] = stm_estimates.totalAirPercent
            row['sewage_biodeg_percent'] = stm_estimates.totalBiodegradationPercent
            row['sewage_effluent_percent'] = stm_estimates.finalEffluentPercent
        
        # Dermal permeability
        if hasattr(result.dermalPermeability, 'dermalPermeabilityCoefficient'):
            row['dermal_permeability_coefficient'] = result.dermalPermeability.dermalPermeabilityCoefficient
            row['dermal_absorbed_dose'] = result.dermalPermeability.dermalAbsorbedDose
            row['dermal_absorbed_dose_per_event'] = result.dermalPermeability.dermalAbsorbedDosePerEvent
            row['lag_time_hours'] = result.dermalPermeability.lagTimePerEventHours
            row['time_to_steady_state_hours'] = result.dermalPermeability.timeToReachSteadyStateHours
        
        # Fugacity model - half-lives and persistence
        fugacity_model = getattr(getattr(result, 'fugacityModel', None), 'model', None)
        if fugacity_model is not None:
            fugacity_estimates = getattr(fugacity_model, 'estimates', None)
            if fugacity_estimates is not None:
                row['fugacity_persistence'] = fugacity_estimates.persistenceHours
                row['fugacity_air_percent'] = fugacity_estimates.airPercent
                row['fugacity_water_percent'] = fugacity_estimates.waterPercent
                row['fugacity_soil_percent'] = fugacity_estimates.soilPercent
                row['fugacity_sediment_percent'] = fugacity_estimates.sedimentPercent
                row['fugacity_selected_koc'] = fugacity_estimates.selectedKoc

            # Compartments are a named list, no longer fixed-order arrays
            for compartment in getattr(fugacity_model, 'compartments', None) or []:
                name = getattr(compartment, 'name', None)
                if not name:
                    continue
                key = _column_name(name)
                row[f'fugacity_{key}_half_life'] = compartment.halfLifeHours
                row[f'fugacity_{key}_mass_percent'] = compartment.massPercent

        data.append(row)
    
    return pd.DataFrame(data)


def episuite_experimental_to_dataframe(results: List[ResultEPISuite]) -> pd.DataFrame:
    """
    Convert experimental values from EPI Suite results to a pandas DataFrame.
    
    This function extracts all experimental values for various properties
    and creates a long-format DataFrame suitable for analysis.
    
    Parameters:
        results (List[ResultEPISuite]): List of EPI Suite result objects
        
    Returns:
        pd.DataFrame: DataFrame with experimental values in long format
    """
    data = []
    
    _PROPERTIES = (
        'logKow', 'meltingPoint', 'boilingPoint', 'vaporPressure',
        'waterSolubilityFromLogKow', 'waterSolubilityFromWaterNt',
        'henrysLawConstant', 'logKoa', 'logKoc',
    )
    _COLUMN_NAMES = {
        'logKow': 'log_kow',
        'meltingPoint': 'melting_point',
        'boilingPoint': 'boiling_point',
        'vaporPressure': 'vapor_pressure',
        'waterSolubilityFromLogKow': 'water_solubility_logkow',
        'waterSolubilityFromWaterNt': 'water_solubility_waternt',
        'henrysLawConstant': 'henrys_law_constant',
        'logKoa': 'log_koa',
        'logKoc': 'log_koc',
    }

    for result in results:
        chem_props = getattr(result, 'chemicalProperties', None)
        cas = getattr(chem_props, 'cas', None)
        name = getattr(chem_props, 'name', None)

        for attr in _PROPERTIES:
            module = getattr(result, attr, None)
            # `module` is None when absent and a ModuleError when the module
            # failed; neither carries experimental values.
            for exp_val in getattr(module, 'experimentalValues', None) or []:
                data.append({
                    'cas': cas,
                    'name': name,
                    'property': _COLUMN_NAMES[attr],
                    'value': getattr(exp_val, 'value', None),
                    'units': getattr(exp_val, 'units', None),
                    'author': getattr(exp_val, 'author', None),
                    'year': getattr(exp_val, 'year', None),
                    'order': getattr(exp_val, 'order', None),
                    'value_type': getattr(exp_val, 'valueType', None),
                    'source': getattr(exp_val, 'source', None),
                    'source_database': getattr(exp_val, 'sourceDatabase', None),
                    'temperature_c': getattr(exp_val, 'temperatureC', None),
                })

    return pd.DataFrame(data)


def ecosar_to_dataframe(results: List[ResultEcoSAR]) -> pd.DataFrame:
    """
    Convert a list of EcoSAR results to a pandas DataFrame.
    
    This function extracts ecotoxicity predictions from EcoSAR results
    and organizes them into a tabular format.
    
    Parameters:
        results (List[ResultEcoSAR]): List of EcoSAR result objects
        
    Returns:
        pd.DataFrame: DataFrame with ecotoxicity predictions
        
    Example:
        >>> from pyepisuite.utils import search_episuite_by_cas, submit_to_episuite
        >>> from pyepisuite.dataframe_utils import ecosar_to_dataframe
        >>> 
        >>> cas_list = ["50-00-0", "100-00-5"]
        >>> ids = search_episuite_by_cas(cas_list)
        >>> _, ecosar_results = submit_to_episuite(ids)
        >>> df = ecosar_to_dataframe(ecosar_results)
        >>> print(df.head())
    """
    data = []
    
    for result in results:
        cas = result.parameters.cas
        smiles = result.parameters.smiles
        
        # Get input parameters
        log_kow = result.parameters.logKow.value if result.parameters.logKow else None
        water_solubility = result.parameters.waterSolubility.value if result.parameters.waterSolubility else None
        melting_point = result.parameters.meltingPoint.value if result.parameters.meltingPoint else None
        
        # Extract model results
        for model_result in result.modelResults:
            row = {
                'cas': cas,
                'smiles': smiles,
                'log_kow_input': log_kow,
                'water_solubility_input': water_solubility,
                'melting_point_input': melting_point,
                'qsar_class': model_result.qsarClass,
                'organism': model_result.organism,
                'duration': model_result.duration,
                'endpoint': model_result.endpoint,
                'concentration': model_result.concentration,
                'max_log_kow': model_result.maxLogKow,
                'flags': ', '.join(model_result.flags) if model_result.flags else None
            }
            data.append(row)
    
    return pd.DataFrame(data)


def _join_unique(values) -> str:
    """Join a group's distinct non-missing values into one comma-separated string.

    Columns such as `flags` are None for most rows, which pandas stores as NaN;
    a plain `is not None` check lets those floats through and breaks the join.
    """
    seen = pd.unique(values.dropna())
    return ', '.join(str(v) for v in seen)


def combine_episuite_ecosar_dataframes(epi_df: pd.DataFrame, ecosar_df: pd.DataFrame) -> pd.DataFrame:
    """
    Combine EPI Suite and EcoSAR DataFrames on CAS number.
    
    Parameters:
        epi_df (pd.DataFrame): DataFrame from episuite_to_dataframe()
        ecosar_df (pd.DataFrame): DataFrame from ecosar_to_dataframe()
        
    Returns:
        pd.DataFrame: Combined DataFrame with both EPI Suite and EcoSAR data
    """
    # Group EcoSAR results by CAS to handle multiple model results
    ecosar_summary = ecosar_df.groupby('cas').agg({
        'qsar_class': _join_unique,
        'organism': _join_unique,
        'endpoint': _join_unique,
        'concentration': ['min', 'max', 'mean'],
        'flags': _join_unique
    }).round(3)
    
    # Flatten column names
    ecosar_summary.columns = ['_'.join(col) if col[1] else col[0] for col in ecosar_summary.columns]
    ecosar_summary = ecosar_summary.reset_index()
    
    # Merge with EPI Suite data
    combined_df = pd.merge(epi_df, ecosar_summary, on='cas', how='left')
    
    return combined_df


def _safe_get_estimated_value(response_obj) -> Optional[float]:
    """Safely extract estimated value from a response object."""
    try:
        if hasattr(response_obj, 'estimatedValue') and hasattr(response_obj.estimatedValue, 'value'):
            return response_obj.estimatedValue.value
        return None
    except (AttributeError, TypeError):
        return None


def _safe_get_estimated_units(response_obj) -> Optional[str]:
    """Safely extract units from a response object."""
    try:
        if hasattr(response_obj, 'estimatedValue') and hasattr(response_obj.estimatedValue, 'units'):
            return response_obj.estimatedValue.units
        return None
    except (AttributeError, TypeError):
        return None


def _safe_get_selected_value(response_obj) -> Optional[float]:
    """Safely extract selected value from a response object."""
    try:
        if hasattr(response_obj, 'selectedValue') and hasattr(response_obj.selectedValue, 'value'):
            return response_obj.selectedValue.value
        return None
    except (AttributeError, TypeError):
        return None


def _column_name(label: str) -> str:
    """Turn an API label ("Estimated Log BCF (upper trophic)") into a column suffix."""
    slug = re.sub(r'[^0-9a-z]+', '_', str(label).lower())
    return slug.strip('_')


def _safe_get_parameter_value(param_obj) -> Optional[float]:
    """Extract the numeric value from a bare scalar or a Parameter-like object."""
    if param_obj is None:
        return None
    if isinstance(param_obj, (int, float)):
        return param_obj
    return getattr(param_obj, 'value', None)


def _safe_get_value_direct(obj) -> Optional[float]:
    """Safely extract value directly from an object."""
    try:
        if hasattr(obj, 'value'):
            return obj.value
        return None
    except (AttributeError, TypeError):
        return None


def _safe_get_units_direct(obj) -> Optional[str]:
    """Safely extract units directly from an object."""
    try:
        if hasattr(obj, 'units'):
            return obj.units
        return None
    except (AttributeError, TypeError):
        return None


def export_to_excel(dataframes: Dict[str, pd.DataFrame], filename: str) -> None:
    """
    Export multiple DataFrames to an Excel file with multiple sheets.
    
    Parameters:
        dataframes (Dict[str, pd.DataFrame]): Dictionary mapping sheet names to DataFrames
        filename (str): Output Excel filename
        
    Example:
        >>> epi_df = episuite_to_dataframe(epi_results)
        >>> ecosar_df = ecosar_to_dataframe(ecosar_results)
        >>> export_to_excel({
        ...     'EPI_Suite': epi_df,
        ...     'EcoSAR': ecosar_df
        ... }, 'results.xlsx')
    """
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        for sheet_name, df in dataframes.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"Data exported to {filename}")


def create_summary_statistics(df: pd.DataFrame, numeric_columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Create summary statistics for numeric columns in the DataFrame.
    
    Parameters:
        df (pd.DataFrame): Input DataFrame
        numeric_columns (List[str], optional): List of numeric columns to summarize.
            If None, all numeric columns are used.
            
    Returns:
        pd.DataFrame: Summary statistics DataFrame
    """
    if numeric_columns is None:
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    
    return df[numeric_columns].describe()
