"""
DataFrame conversion utilities for PyEPISuite results.

This module provides functions to convert EPI Suite and EcoSAR results
to pandas DataFrames for easier data analysis and manipulation.
"""

import pandas as pd
from typing import List, Dict, Any, Optional, Union
from .models import ResultEPISuite, ResultEcoSAR, ExperimentalValue, Parameter


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
        row['cas'] = result.chemicalProperties.cas
        row['name'] = result.chemicalProperties.name
        row['systematic_name'] = result.chemicalProperties.systematicName
        row['smiles'] = result.chemicalProperties.smiles
        row['molecular_weight'] = result.chemicalProperties.molecularWeight
        row['molecular_formula'] = result.chemicalProperties.molecularFormula
        row['is_organic'] = result.chemicalProperties.organic
        row['is_organic_acid'] = result.chemicalProperties.organicAcid
        row['is_amino_acid'] = result.chemicalProperties.aminoAcid
        row['is_non_standard_metal'] = result.chemicalProperties.nonStandardMetal

        # Physical and chemical properties - estimated values
        row['log_kow_estimated'] = _safe_get_estimated_value(result.logKow)
        row['log_kow_units'] = _safe_get_estimated_units(result.logKow)
        
        row['melting_point_estimated'] = _safe_get_estimated_value(result.meltingPoint)
        row['melting_point_units'] = _safe_get_estimated_units(result.meltingPoint)
        
        row['boiling_point_estimated'] = _safe_get_estimated_value(result.boilingPoint)
        row['boiling_point_units'] = _safe_get_estimated_units(result.boilingPoint)
        
        row['vapor_pressure_estimated'] = _safe_get_estimated_value(result.vaporPressure)
        row['vapor_pressure_units'] = _safe_get_estimated_units(result.vaporPressure)
        
        row['water_solubility_logkow_estimated'] = _safe_get_estimated_value(result.waterSolubilityFromLogKow)
        row['water_solubility_logkow_units'] = _safe_get_estimated_units(result.waterSolubilityFromLogKow)
        
        row['water_solubility_waternt_estimated'] = _safe_get_estimated_value(result.waterSolubilityFromWaterNt)
        row['water_solubility_waternt_units'] = _safe_get_estimated_units(result.waterSolubilityFromWaterNt)
        
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
            
            # Get first trophic level data if available
            if hasattr(result.bioconcentration, 'arnotGobasBcfBafEstimates') and result.bioconcentration.arnotGobasBcfBafEstimates:
                first_trophic = result.bioconcentration.arnotGobasBcfBafEstimates[0]
                row['trophic_level'] = first_trophic.trophicLevel
                row['trophic_bioaccumulation_factor'] = first_trophic.bioaccumulationFactor
                row['trophic_bioconcentration_factor'] = first_trophic.bioconcentrationFactor
                row['trophic_unit'] = first_trophic.unit
        
        # Hydrolysis
        if hasattr(result, 'hydrolysis'):
            row['acid_catalyzed_rate_constant'] = result.hydrolysis.acidCatalyzedRateConstant
            row['base_catalyzed_rate_constant'] = result.hydrolysis.baseCatalyzedRateConstant
            row['neutral_rate_constant'] = result.hydrolysis.neutralRateConstant
            row['acid_catalyzed_trans_isomer_rate'] = result.hydrolysis.acidCatalyzedRateConstantForTransIsomer
        
        # Biodegradation models - get summary of main models
        if hasattr(result, 'biodegradationRate') and hasattr(result.biodegradationRate, 'models'):
            for model in result.biodegradationRate.models:
                if hasattr(model, 'name') and hasattr(model, 'value'):
                    model_name = model.name.lower().replace(' ', '_').replace('-', '_')
                    row[f'biodeg_{model_name}'] = model.value
        
        # Water volatilization
        if hasattr(result.waterVolatilization, 'riverHalfLifeHours'):
            row['river_half_life_hours'] = result.waterVolatilization.riverHalfLifeHours
            row['lake_half_life_hours'] = result.waterVolatilization.lakeHalfLifeHours
            
            # Water volatilization parameters
            if hasattr(result.waterVolatilization, 'parameters'):
                params = result.waterVolatilization.parameters
                row['lake_current_velocity_ms'] = params.lakeCurrentVelocityMetersPerSecond
                row['lake_water_depth_m'] = params.lakeWaterDepthMeters
                row['lake_wind_velocity_ms'] = params.lakeWindVelocityMetersPerSecond
                row['river_current_velocity_ms'] = params.riverCurrentVelocityMetersPerSecond
                row['river_water_depth_m'] = params.riverWaterDepthMeters
                row['river_wind_velocity_ms'] = params.riverWindVelocityMetersPerSecond
        
        # Sewage treatment model - get key removal percentages
        if hasattr(result, 'sewageTreatmentModel') and hasattr(result.sewageTreatmentModel, 'model'):
            stm = result.sewageTreatmentModel.model
            if hasattr(stm, 'TotalRemoval'):
                row['sewage_total_removal_percent'] = stm.TotalRemoval.Percent
            if hasattr(stm, 'TotalSludge'):
                row['sewage_sludge_percent'] = stm.TotalSludge.Percent
            if hasattr(stm, 'TotalAir'):
                row['sewage_air_percent'] = stm.TotalAir.Percent
            if hasattr(stm, 'TotalBiodeg'):
                row['sewage_biodeg_percent'] = stm.TotalBiodeg.Percent
            if hasattr(stm, 'FinalEffluent'):
                row['sewage_effluent_percent'] = stm.FinalEffluent.Percent
        
        # Dermal permeability
        if hasattr(result.dermalPermeability, 'dermalPermeabilityCoefficient'):
            row['dermal_permeability_coefficient'] = result.dermalPermeability.dermalPermeabilityCoefficient
            row['dermal_absorbed_dose'] = result.dermalPermeability.dermalAbsorbedDose
            row['dermal_absorbed_dose_per_event'] = result.dermalPermeability.dermalAbsorbedDosePerEvent
            row['lag_time_hours'] = result.dermalPermeability.lagTimePerEventHours
            row['time_to_steady_state_hours'] = result.dermalPermeability.timeToReachSteadyStateHours
        
        # Fugacity model - half-lives and persistence
        if hasattr(result.fugacityModel, 'model'):
            if hasattr(result.fugacityModel.model, 'Persistence'):
                row['fugacity_persistence'] = result.fugacityModel.model.Persistence
            
            # Get individual compartment half-lives
            if hasattr(result.fugacityModel.model, 'HalfLifeArray'):
                half_lives = result.fugacityModel.model.HalfLifeArray
                if len(half_lives) >= 4:
                    row['fugacity_air_half_life'] = half_lives[0]
                    row['fugacity_water_half_life'] = half_lives[1]
                    row['fugacity_soil_half_life'] = half_lives[2]
                    row['fugacity_sediment_half_life'] = half_lives[3]
            
            # Alternative method to get compartment half-lives (dynamic attributes)
            # Note: These attributes are accessed dynamically and may not be type-checked properly
            try:
                if hasattr(result.fugacityModel.model, 'Sediment') and result.fugacityModel.model.Sediment and len(result.fugacityModel.model.Sediment) > 0:
                    sediment_obj = result.fugacityModel.model.Sediment[0]
                    if hasattr(sediment_obj, 'HalfLife'):
                        row['fugacity_sediment_half_life_alt'] = getattr(sediment_obj, 'HalfLife', None)
                if hasattr(result.fugacityModel.model, 'Soil') and result.fugacityModel.model.Soil and len(result.fugacityModel.model.Soil) > 0:
                    soil_obj = result.fugacityModel.model.Soil[0]
                    if hasattr(soil_obj, 'HalfLife'):
                        row['fugacity_soil_half_life_alt'] = getattr(soil_obj, 'HalfLife', None)
                if hasattr(result.fugacityModel.model, 'Water') and result.fugacityModel.model.Water and len(result.fugacityModel.model.Water) > 0:
                    water_obj = result.fugacityModel.model.Water[0]
                    if hasattr(water_obj, 'HalfLife'):
                        row['fugacity_water_half_life_alt'] = getattr(water_obj, 'HalfLife', None)
            except (AttributeError, IndexError, TypeError):
                pass
        
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
    
    for result in results:
        cas = result.chemicalProperties.cas
        name = result.chemicalProperties.name
        
        # Extract experimental values for each property
        properties = [
            ('log_kow', result.logKow.experimentalValues if hasattr(result.logKow, 'experimentalValues') else []),
            ('melting_point', result.meltingPoint.experimentalValues if hasattr(result.meltingPoint, 'experimentalValues') else []),
            ('boiling_point', result.boilingPoint.experimentalValues if hasattr(result.boilingPoint, 'experimentalValues') else []),
            ('vapor_pressure', result.vaporPressure.experimentalValues if hasattr(result.vaporPressure, 'experimentalValues') else []),
            ('water_solubility_logkow', result.waterSolubilityFromLogKow.experimentalValues if hasattr(result.waterSolubilityFromLogKow, 'experimentalValues') else []),
            ('water_solubility_waternt', result.waterSolubilityFromWaterNt.experimentalValues if hasattr(result.waterSolubilityFromWaterNt, 'experimentalValues') else []),
            ('henrys_law_constant', result.henrysLawConstant.experimentalValues if hasattr(result.henrysLawConstant, 'experimentalValues') else []),
            ('log_koa', result.logKoa.experimentalValues if hasattr(result.logKoa, 'experimentalValues') else []),
            ('log_koc', result.logKoc.experimentalValues if hasattr(result.logKoc, 'experimentalValues') else []),
        ]
        
        for prop_name, exp_values in properties:
            for exp_val in exp_values:
                if hasattr(exp_val, 'value'):
                    row = {
                        'cas': cas,
                        'name': name,
                        'property': prop_name,
                        'value': exp_val.value,
                        'units': exp_val.units if hasattr(exp_val, 'units') else None,
                        'author': exp_val.author if hasattr(exp_val, 'author') else None,
                        'year': exp_val.year if hasattr(exp_val, 'year') else None,
                        'order': exp_val.order if hasattr(exp_val, 'order') else None,
                        'value_type': exp_val.valueType if hasattr(exp_val, 'valueType') else None
                    }
                    data.append(row)
    
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
        'qsar_class': lambda x: ', '.join(x.unique()),
        'organism': lambda x: ', '.join(x.unique()),
        'endpoint': lambda x: ', '.join(x.unique()),
        'concentration': ['min', 'max', 'mean'],
        'flags': lambda x: ', '.join([f for f in x.unique() if f is not None])
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
