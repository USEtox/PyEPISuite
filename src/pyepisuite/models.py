# models.py
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union

def ensure_flags(value: Any) -> Optional[Dict[str, bool]]:
    """Normalize flags input to Optional[Dict[str,bool]].

    Accepts dict, iterable of (key, val) pairs, iterable of keys, generator, and some string forms.
    Returns None when no usable value.
    """
    if value is None:
        return None

    # Already a dict -> coerce values to bool
    if isinstance(value, dict):
        return {str(k): bool(v) for k, v in value.items()}

    # Strings handled below
    if isinstance(value, str):
        s = value.strip()
        # reject python repr of generator like "<generator object ...>"
        if s.startswith("<") and "generator" in s:
            return None
        # parse "a:True,b:False"
        if ":" in s and "," in s:
            out = {}
            for part in s.split(","):
                if ":" in part:
                    k, v = part.split(":", 1)
                    out[k.strip()] = v.strip().lower() in ("1", "true", "yes")
            return out or None
        # comma-separated keys -> True
        if "," in s:
            return {p.strip(): True for p in s.split(",") if p.strip()} or None
        # single token -> treat as key True
        return {s: True}

    # Iterable (list/tuple/generator) of pairs or keys
    try:
        it = iter(value)
    except TypeError:
        return None

    out: Dict[str, bool] = {}
    for item in it:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            k, v = item[0], item[1]
            out[str(k)] = bool(v)
        else:
            # single item -> key True
            out[str(item)] = True

    return out or None


# Base Classes
@dataclass
class Identifiers:
    name: Optional[str] = None
    smiles: Optional[str] = None
    cas: Optional[str] = None

@dataclass
class Parameter:
    value: Optional[float] = None
    units: Optional[str] = None
    valueType: Optional[str] = None
    source: Optional[str] = None

# Many "parameters" fields that echo request inputs are returned by the API
# either as a bare scalar (when supplied directly) or as a full Parameter
# object carrying provenance (e.g. {"value": ..., "units": ..., "source": ...,
# "valueType": ...}) when resolved from a default or another module's output.
# Fields subject to this ambiguity are typed with these aliases instead of a
# single fixed type.
NumericParameter = Union[float, Parameter]
BoolParameter = Union[bool, Parameter]

@dataclass
class Coefficient:
    type: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None

@dataclass
class Parameters:
    cas: Optional[str] = None
    smiles: Optional[str] = None
    caseNumber: Optional[str] = None
    userLogKow: Optional[NumericParameter] = None
    userMeltingPoint: Optional[NumericParameter] = None
    userBoilingPoint: Optional[NumericParameter] = None
    userWaterSolubility: Optional[NumericParameter] = None
    userVaporPressure: Optional[NumericParameter] = None
    userHenrysLawConstant: Optional[NumericParameter] = None
    userLogKoa: Optional[NumericParameter] = None
    userLogKoc: Optional[NumericParameter] = None
    userHydroxylReactionRateConstant: Optional[NumericParameter] = None
    userDermalPermeabilityCoefficient: Optional[NumericParameter] = None
    userBiodegradationRateRemoveMetals: Optional[Union[NumericParameter, BoolParameter]] = None
    userAtmosphericHydroxylRadicalConcentration: Optional[NumericParameter] = None
    userAtmosphericOzoneConcentration: Optional[NumericParameter] = None
    userAtmosphericDaylightHours: Optional[NumericParameter] = None
    userStpHalfLifePrimaryClarifier: Optional[NumericParameter] = None
    userStpHalfLifeAerationVessel: Optional[NumericParameter] = None
    userStpHalfLifeSettlingTank: Optional[NumericParameter] = None
    userFugacityHalfLifeAir: Optional[NumericParameter] = None
    userFugacityHalfLifeWater: Optional[NumericParameter] = None
    userFugacityHalfLifeSoil: Optional[NumericParameter] = None
    userFugacityHalfLifeSediment: Optional[NumericParameter] = None
    userFugacityEmissionRateAir: Optional[NumericParameter] = None
    userFugacityEmissionRateWater: Optional[NumericParameter] = None
    userFugacityEmissionRateSoil: Optional[NumericParameter] = None
    userFugacityEmissionRateSediment: Optional[NumericParameter] = None
    userFugacityAdvectionTimeAir: Optional[NumericParameter] = None
    userFugacityAdvectionTimeWater: Optional[NumericParameter] = None
    userFugacityAdvectionTimeSoil: Optional[NumericParameter] = None
    userFugacityAdvectionTimeSediment: Optional[NumericParameter] = None
    modules: Optional[List[str]] = None

@dataclass
class ChemicalProperties:
    name: Optional[str] = None
    systematicName: Optional[str] = None
    cas: Optional[str] = None
    smiles: Optional[str] = None
    molecularWeight: Optional[float] = None
    molecularFormula: Optional[str] = None
    molecularFormulaHtml: Optional[str] = None
    organic: Optional[bool] = None
    organicAcid: Optional[bool] = None
    aminoAcid: Optional[bool] = None
    nonStandardMetal: Optional[bool] = None
    flags: Optional[Dict[str, bool]] = None

# Common Response Classes
@dataclass
class Flag:
    isOrganicAcid: Optional[bool] = None
    isAminoAcid: Optional[bool] = None

@dataclass
class KowFactor:
    type: Optional[str] = None
    description: Optional[str] = None
    fragmentCount: Optional[int] = None
    coefficient: Optional[float] = None
    contribution: Optional[float] = None
    trainingCount: Optional[int] = None
    validationCount: Optional[int] = None

@dataclass
class KowModel:
    logKow: Optional[float] = None
    factors: Optional[List[KowFactor]] = None
    output: Optional[str] = None
    notes: Optional[str] = None
    flags: Optional[Flag] = None

@dataclass
class logKowEstimatedValue:
    # The API does not guarantee a fixed shape for this internal model
    # breakdown (it is not part of the documented Value contract). Try the
    # typical KowModel shape first, and fall back to the raw data untouched
    # when it doesn't match instead of raising.
    model: Optional[Union[KowModel, Any]] = None
    value: Optional[float] = None
    units: Optional[str] = None
    valueType: Optional[str] = None

@dataclass
class ExperimentalValue:
    author: Optional[str] = None
    year: Optional[int] = None
    order: Optional[int] = None
    value: Optional[float] = None
    units: Optional[str] = None
    valueType: Optional[str] = None

@dataclass
class SelectedValue:
    value: Optional[float] = None
    units: Optional[str] = None
    valueType: Optional[str] = None

# Specific Response Classes
@dataclass
class LogKowResponse:
    estimatedValue: Optional[logKowEstimatedValue] = None
    experimentalValues: Optional[List[ExperimentalValue]] = None
    selectedValue: Optional[SelectedValue] = None

# MeltingPointFactor dataclass
@dataclass
class MeltingPointFactor:
    type: Optional[str] = None
    description: Optional[str] = None
    fragmentCount: Optional[int] = None
    coefficient: Optional[float] = None
    totalCoefficient: Optional[float] = None

# MeltingPointModel dataclass
@dataclass
class MeltingPointModel:
    factors: Optional[List[MeltingPointFactor]] = None
    meltingPointKelvins: Optional[float] = None
    meltingPointLimitKelvins: Optional[float] = None
    meltingPointCelsius: Optional[float] = None
    meltingPointAdaptedJoback: Optional[float] = None
    meltingPointGoldOgle: Optional[float] = None
    meltingPointMean: Optional[float] = None
    meltingPointSelected: Optional[float] = None

# MeltingPointEstimatedValue dataclass
@dataclass
class MeltingPointEstimatedValue:
    model: Optional[Union[MeltingPointModel, Any]] = None
    value: Optional[float] = None
    units: Optional[str] = None
    valueType: Optional[str] = None

# MeltingPointResponse dataclass
@dataclass
class MeltingPointResponse:
    estimatedValue: Optional[MeltingPointEstimatedValue] = None
    experimentalValues: Optional[List[ExperimentalValue]] = None
    selectedValue: Optional[SelectedValue] = None

# BoilingPointFactor dataclass
@dataclass
class BoilingPointFactor:
    type: Optional[str] = None
    description: Optional[str] = None
    fragmentCount: Optional[int] = None
    coefficient: Optional[float] = None
    totalCoefficient: Optional[float] = None

# BoilingPointModel dataclass
@dataclass
class BoilingPointModel:
    factors: Optional[List[BoilingPointFactor]] = None
    boilingPointKelvinsUncorrected: Optional[float] = None
    boilingPointKelvinsCorrected: Optional[float] = None
    boilingPointCelsius: Optional[float] = None

# BoilingPointEstimatedValue dataclass
@dataclass
class BoilingPointEstimatedValue:
    model: Optional[Union[BoilingPointModel, Any]] = None
    value: Optional[float] = None
    units: Optional[str] = None
    valueType: Optional[str] = None

# BoilingPointResponse dataclass
@dataclass
class BoilingPointResponse:
    estimatedValue: Optional[BoilingPointEstimatedValue] = None
    experimentalValues: Optional[List[ExperimentalValue]] = None
    selectedValue: Optional[SelectedValue] = None

# VaporPressureModelItem dataclass
@dataclass
class VaporPressureModelItem:
    type: Optional[str] = None
    mmHg: Optional[float] = None
    pa: Optional[float] = None

# VaporPressureEstimatedValue dataclass
@dataclass
class VaporPressureEstimatedValue:
    model: Optional[Union[List[VaporPressureModelItem], Any]] = None
    value: Optional[float] = None
    units: Optional[str] = None
    valueType: Optional[str] = None

# VaporPressureResponse dataclass
@dataclass
class VaporPressureResponse:
    estimatedValue: Optional[VaporPressureEstimatedValue] = None
    experimentalValues: Optional[List[ExperimentalValue]] = None
    selectedValue: Optional[SelectedValue] = None

@dataclass
class WaterSolubilityFromLogKowFactor:
    type: Optional[str] = None
    description: Optional[str] = None
    fragmentCount: Optional[int] = None
    coefficient: Optional[float] = None
    totalCoefficient: Optional[float] = None
    trainingCount: Optional[int] = None
    maxFragmentCount: Optional[int] = None

# WaterSolubilityModel dataclass
@dataclass
class WaterSolubilityModel:
    waterSolubility: Optional[float] = None
    factors: Optional[List[WaterSolubilityFromLogKowFactor]] = None
    equation: Optional[str] = None
    notes: Optional[str] = None
    output: Optional[str] = None

# WaterSolubilityEstimatedValue dataclass
@dataclass
class WaterSolubilityEstimatedValue:
    model: Optional[Union[WaterSolubilityModel, Any]] = None
    value: Optional[float] = None
    units: Optional[str] = None
    valueType: Optional[str] = None

# WaterSolubilityFromLogKowParameters dataclass
@dataclass
class WaterSolubilityFromLogKowParameters:
    smiles: Optional[str] = None
    cas: Optional[str] = None
    logKow: Optional[NumericParameter] = None
    meltingPoint: Optional[NumericParameter] = None

# WaterSolubilityFromLogKowResponse dataclass
@dataclass
class WaterSolubilityFromLogKowResponse:
    parameters: Optional[WaterSolubilityFromLogKowParameters] = None
    estimatedValue: Optional[WaterSolubilityEstimatedValue] = None
    experimentalValues: Optional[List[ExperimentalValue]] = None
    selectedValue: Optional[SelectedValue] = None

# WaterSolubilityFromWaterNtFactor dataclass
@dataclass
class WaterSolubilityFromWaterNtFactor:
    type: Optional[str] = None
    description: Optional[str] = None
    fragmentCount: Optional[int] = None
    coefficient: Optional[float] = None
    totalCoefficient: Optional[float] = None
    trainingCount: Optional[int] = None
    maxFragmentCount: Optional[int] = None

# WaterSolubilityFromWaterNtModel dataclass
@dataclass
class WaterSolubilityFromWaterNtModel:
    waterSolubility: Optional[float] = None
    factors: Optional[List[WaterSolubilityFromWaterNtFactor]] = None
    equation: Optional[str] = None
    notes: Optional[str] = None
    output: Optional[str] = None

# WaterSolubilityFromWaterNtEstimatedValue dataclass
@dataclass
class WaterSolubilityFromWaterNtEstimatedValue:
    model: Optional[Union[WaterSolubilityFromWaterNtModel, Any]] = None
    value: Optional[float] = None
    units: Optional[str] = None
    valueType: Optional[str] = None

# WaterSolubilityFromWaterNtParameters dataclass
@dataclass
class WaterSolubilityFromWaterNtParameters:
    smiles: Optional[str] = None
    cas: Optional[str] = None

# WaterSolubilityFromWaterNtResponse dataclass
@dataclass
class WaterSolubilityFromWaterNtResponse:
    parameters: Optional[WaterSolubilityFromWaterNtParameters] = None
    estimatedValue: Optional[WaterSolubilityFromWaterNtEstimatedValue] = None
    experimentalValues: Optional[List[ExperimentalValue]] = None
    selectedValue: Optional[SelectedValue] = None

# HenrysLawConstantFactor dataclass
@dataclass
class HenrysLawConstantFactor:
    type: Optional[str] = None
    description: Optional[str] = None
    fragmentCount: Optional[int] = None
    totalCoefficient: Optional[float] = None
    trainingCount: Optional[int] = None
    maxFragmentCount: Optional[int] = None

# HenrysLawConstantModelItem dataclass
@dataclass
class HenrysLawConstantModelItem:
    name: Optional[str] = None
    value: Optional[float] = None
    factors: Optional[List[HenrysLawConstantFactor]] = None
    hlcAtm: Optional[float] = None
    hlcUnitless: Optional[float] = None
    hlcPaMol: Optional[float] = None
    notes: Optional[str] = None

# HenrysLawConstantEstimatedValue dataclass
@dataclass
class HenrysLawConstantEstimatedValue:
    model: Optional[List[HenrysLawConstantModelItem]] = None
    value: Optional[float] = None
    units: Optional[str] = None
    valueType: Optional[str] = None

# HenrysLawConstantParameters dataclass
@dataclass
class HenrysLawConstantParameters:
    smiles: Optional[str] = None
    cas: Optional[str] = None
    waterSolubility: Optional[NumericParameter] = None
    vaporPressure: Optional[NumericParameter] = None
    molecularWeight: Optional[NumericParameter] = None

# HenrysLawConstantResponse dataclass
@dataclass
class HenrysLawConstantResponse:
    parameters: Optional[HenrysLawConstantParameters] = None
    estimatedValue: Optional[HenrysLawConstantEstimatedValue] = None
    experimentalValues: Optional[List[ExperimentalValue]] = None
    selectedValue: Optional[SelectedValue] = None

# LogKoaModel dataclass
@dataclass
class LogKoaModel:
    kow: Optional[float] = None
    kaw: Optional[float] = None
    koa: Optional[float] = None
    logKoa: Optional[float] = None

# LogKoaEstimatedValue dataclass
@dataclass
class LogKoaEstimatedValue:
    model: Optional[Union[LogKoaModel, Any]] = None
    value: Optional[float] = None
    units: Optional[str] = None
    valueType: Optional[str] = None

# LogKoaParameters dataclass
@dataclass
class LogKoaParameters:
    smiles: Optional[str] = None
    cas: Optional[str] = None
    logKow: Optional[NumericParameter] = None
    henrysLawConstant: Optional[NumericParameter] = None

# LogKoaResponse dataclass
@dataclass
class LogKoaResponse:
    parameters: Optional[LogKoaParameters] = None
    estimatedValue: Optional[LogKoaEstimatedValue] = None
    experimentalValues: Optional[List[ExperimentalValue]] = None
    selectedValue: Optional[SelectedValue] = None

# BiodegradationRateFactor dataclass
@dataclass
class BiodegradationRateFactor:
    type: Optional[str] = None
    description: Optional[str] = None
    fragmentCount: Optional[int] = None
    coefficient: Optional[float] = None
    totalCoefficient: Optional[float] = None
    trainingCount: Optional[int] = None
    maxFragmentCount: Optional[int] = None

# BiodegradationRateModel dataclass
@dataclass
class BiodegradationRateModel:
    name: Optional[str] = None
    value: Optional[float] = None
    factors: Optional[List[BiodegradationRateFactor]] = None

# BiodegradationRateParameters dataclass
@dataclass
class BiodegradationRateParameters:
    smiles: Optional[str] = None
    cas: Optional[str] = None
    removeMetals: Optional[BoolParameter] = None

# BiodegradationRateResponse dataclass
@dataclass
class BiodegradationRateResponse:
    parameters: Optional[BiodegradationRateParameters] = None
    models: Optional[List[BiodegradationRateModel]] = None
    notes: Optional[str] = None
    output: Optional[str] = None

# HydrocarbonBiodegradationRateModelFactor dataclass
@dataclass
class HydrocarbonBiodegradationRateModelFactor:
    type: Optional[str] = None
    description: Optional[str] = None
    fragmentCount: Optional[int] = None
    coefficient: Optional[float] = None
    totalCoefficient: Optional[float] = None
    trainingCount: Optional[int] = None
    maxFragmentCount: Optional[int] = None

# HydrocarbonBiodegradationRateModel dataclass
@dataclass
class HydrocarbonBiodegradationRateModel:
    halfLifeDays: Optional[float] = None
    logHalfLifeDays: Optional[float] = None
    factors: Optional[List[HydrocarbonBiodegradationRateModelFactor]] = None
    notes: Optional[str] = None
    output: Optional[str] = None

# HydrocarbonBiodegradationRateEstimatedValue dataclass
@dataclass
class HydrocarbonBiodegradationRateEstimatedValue:
    model: Optional[Union[HydrocarbonBiodegradationRateModel, Any]] = None
    value: Optional[float] = None
    units: Optional[str] = None
    valueType: Optional[str] = None

# HydrocarbonBiodegradationRateParameters dataclass
@dataclass
class HydrocarbonBiodegradationRateParameters:
    smiles: Optional[str] = None
    cas: Optional[str] = None

# HydrocarbonBiodegradationRateResponse dataclass
@dataclass
class HydrocarbonBiodegradationRateResponse:
    parameters: Optional[HydrocarbonBiodegradationRateParameters] = None
    estimatedValue: Optional[HydrocarbonBiodegradationRateEstimatedValue] = None
    selectedValue: Optional[SelectedValue] = None

# AerosolAdsorptionFractionModel dataclass
@dataclass
class AerosolAdsorptionFractionModel:
    mackayParticleGasPartitionCoefficient: Optional[float] = None
    koaParticleGasPartitionCoefficient: Optional[float] = None
    mackayAdsorptionFraction: Optional[float] = None
    koaAdsorptionFraction: Optional[float] = None
    jungePankowAdsorptionFraction: Optional[float] = None

# AerosolAdsorptionFractionEstimatedValue dataclass
@dataclass
class AerosolAdsorptionFractionEstimatedValue:
    model: Optional[Union[AerosolAdsorptionFractionModel, Any]] = None
    value: Optional[float] = None
    units: Optional[str] = None
    valueType: Optional[str] = None

# AerosolAdsorptionFractionParameters dataclass
@dataclass
class AerosolAdsorptionFractionParameters:
    logKoa: Optional[NumericParameter] = None
    subcooledVaporPressure: Optional[NumericParameter] = None

# AerosolAdsorptionFractionResponse dataclass
@dataclass
class AerosolAdsorptionFractionResponse:
    parameters: Optional[AerosolAdsorptionFractionParameters] = None
    estimatedValue: Optional[AerosolAdsorptionFractionEstimatedValue] = None
    selectedValue: Optional[SelectedValue] = None

# ReactionFactor dataclass
@dataclass
class ReactionFactor:
    type: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None

# ReactionModel dataclass
@dataclass
class ReactionModel:
    type: Optional[str] = None
    rateConstant: Optional[float] = None
    halfLifeHours: Optional[float] = None
    factors: Optional[List[ReactionFactor]] = None

# EstimatedValueModel dataclass
@dataclass
class EstimatedValueModel:
    models: Optional[List[ReactionModel]] = None
    notes: Optional[str] = None
    output: Optional[str] = None

# EstimatedValue dataclass
@dataclass
class EstimatedValue:
    model: Optional[Union[EstimatedValueModel, Any]] = None
    value: Optional[float] = None
    units: Optional[str] = None
    valueType: Optional[str] = None

# EstimatedHydroxylRadicalReactionRateConstantModel dataclass
@dataclass
class EstimatedHydroxylRadicalReactionRateConstantModel:
    type: Optional[str] = None
    rateConstant: Optional[float] = None
    halfLifeHours: Optional[float] = None
    factors: Optional[List[ReactionFactor]] = None

# EstimatedHydroxylRadicalReactionRateConstant dataclass
@dataclass
class EstimatedHydroxylRadicalReactionRateConstant:
    model: Optional[Union[EstimatedHydroxylRadicalReactionRateConstantModel, Any]] = None
    value: Optional[float] = None
    units: Optional[str] = None
    valueType: Optional[str] = None

# EstimatedOzoneReactionRateConstantModel dataclass
@dataclass
class EstimatedOzoneReactionRateConstantModel:
    type: Optional[str] = None
    rateConstant: Optional[float] = None
    halfLifeHours: Optional[float] = None
    factors: Optional[List[ReactionFactor]] = None

# EstimatedOzoneReactionRateConstant dataclass
@dataclass
class EstimatedOzoneReactionRateConstant:
    model: Optional[Union[EstimatedOzoneReactionRateConstantModel, Any]] = None
    value: Optional[float] = None
    units: Optional[str] = None
    valueType: Optional[str] = None

# ExperimentalReactionRateConstant dataclass
@dataclass
class ExperimentalReactionRateConstant:
    author: Optional[str] = None
    year: Optional[int] = None
    order: Optional[int] = None
    value: Optional[float] = None
    units: Optional[str] = None
    valueType: Optional[str] = None

# AtmosphericHalfLifeParameters dataclass
@dataclass
class AtmosphericHalfLifeParameters:
    smiles: Optional[str] = None
    cas: Optional[str] = None
    hydroxylRadicalConcentration: Optional[NumericParameter] = None
    ozoneConcentration: Optional[NumericParameter] = None
    twelveHourDay: Optional[BoolParameter] = None

# AtmosphericHalfLifeResponse dataclass
@dataclass
class AtmosphericHalfLifeResponse:
    parameters: Optional[AtmosphericHalfLifeParameters] = None
    estimatedValue: Optional[EstimatedValue] = None
    estimatedHydroxylRadicalReactionRateConstant: Optional[EstimatedHydroxylRadicalReactionRateConstant] = None
    estimatedOzoneReactionRateConstant: Optional[EstimatedOzoneReactionRateConstant] = None
    experimentalHydroxylRadicalReactionRateConstantValues: Optional[List[ExperimentalReactionRateConstant]] = None
    experimentalOzoneReactionRateConstantValues: Optional[List[ExperimentalReactionRateConstant]] = None
    experimentalNitrateReactionRateConstantValues: Optional[List[ExperimentalReactionRateConstant]] = None
    selectedHydroxylRadicalReactionRateConstant: Optional[SelectedValue] = None
    selectedOzoneReactionRateConstantValues: Optional[SelectedValue] = None

# LogKocFactor dataclass
@dataclass
class LogKocFactor:
    fragmentCount: Optional[int] = None
    trainingCount: Optional[int] = None
    maxFragmentCount: Optional[int] = None
    description: Optional[str] = None
    coefficient: Optional[float] = None
    totalCoefficient: Optional[float] = None

# LogKocModelItem dataclass
@dataclass
class LogKocModelItem:
    firstOrderMCI: Optional[float] = None
    name: Optional[str] = None
    factors: Optional[List[LogKocFactor]] = None
    nonCorrectedLogKoc: Optional[float] = None
    correctedLogKoc: Optional[float] = None
    koc: Optional[float] = None
    logKow: Optional[float] = None

# LogKocModel dataclass
@dataclass
class LogKocModel:
    logKoc: Optional[float] = None
    models: Optional[List[LogKocModelItem]] = None
    notes: Optional[str] = None
    output: Optional[str] = None

# LogKocEstimatedValue dataclass
@dataclass
class LogKocEstimatedValue:
    model: Optional[Union[LogKocModel, List[LogKocModelItem], Any]] = None
    value: Optional[float] = None
    units: Optional[str] = None
    valueType: Optional[str] = None

# LogKocParameters dataclass
@dataclass
class LogKocParameters:
    smiles: Optional[str] = None
    cas: Optional[str] = None
    logKow: Optional[NumericParameter] = None

# LogKocResponse dataclass
@dataclass
class LogKocResponse:
    parameters: Optional[LogKocParameters] = None
    experimentalValues: Optional[List[ExperimentalValue]] = None
    estimatedValue: Optional[LogKocEstimatedValue] = None
    selectedValue: Optional[SelectedValue] = None

# HydrolysisHalfLife dataclass
@dataclass
class HydrolysisHalfLife:
    ph: Optional[float] = None
    value: Optional[float] = None
    unit: Optional[str] = None
    baseCatalyzed: Optional[bool] = None
    acidCatalyzed: Optional[bool] = None
    phosphorusEster: Optional[bool] = None
    isomer: Optional[str] = None

# HydrolysisFragment dataclass
@dataclass
class HydrolysisFragment:
    # Define fields if available
    pass

# HydrolysisResponse dataclass
@dataclass
class HydrolysisResponse:
    halfLives: Optional[List[HydrolysisHalfLife]] = None
    phosphorusEsterHalfLives: Optional[List[HydrolysisHalfLife]] = None
    fragments: Optional[List[HydrolysisFragment]] = None
    baseCatalyzedRateConstant: Optional[float] = None
    acidCatalyzedRateConstant: Optional[float] = None
    acidCatalyzedRateConstantForTransIsomer: Optional[float] = None
    neutralRateConstant: Optional[float] = None
    output: Optional[str] = None

# BioconcentrationParameters dataclass
@dataclass
class BioconcentrationParameters:
    smiles: Optional[str] = None
    cas: Optional[str] = None
    logKow: Optional[NumericParameter] = None

# BiotransformationFactor dataclass
@dataclass
class BiotransformationFactor:
    type: Optional[str] = None
    description: Optional[str] = None
    fragmentCount: Optional[int] = None
    coefficient: Optional[float] = None
    totalCoefficient: Optional[float] = None
    trainingCount: Optional[int] = None
    maxFragmentCount: Optional[int] = None

# BiotransformationRateConstant dataclass
@dataclass
class BiotransformationRateConstant:
    type: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None

# BioconcentrationFactor dataclass
@dataclass
class BioconcentrationFactor:
    type: Optional[str] = None
    description: Optional[str] = None
    fragmentCount: Optional[int] = None
    coefficient: Optional[float] = None
    totalCoefficient: Optional[float] = None
    trainingCount: Optional[int] = None
    maxFragmentCount: Optional[int] = None

# ArnotGobasBcfBafEstimate dataclass
@dataclass
class ArnotGobasBcfBafEstimate:
    trophicLevel: Optional[str] = None
    trophicLevelNote: Optional[str] = None
    bioconcentrationFactor: Optional[float] = None
    logBioconcentrationFactor: Optional[float] = None
    bioaccumulationFactor: Optional[float] = None
    logBioaccumulationFactor: Optional[float] = None
    unit: Optional[str] = None

# BioconcentrationResponse dataclass
@dataclass
class BioconcentrationResponse:
    parameters: Optional[BioconcentrationParameters] = None
    bioconcentrationFactor: Optional[float] = None
    experimentalBioconcentrationFactor: Optional[float] = None
    experimentalBioTransformationRate: Optional[float] = None
    logBioconcentrationFactor: Optional[float] = None
    biotransformationHalfLife: Optional[float] = None
    bioaccumulationFactor: Optional[float] = None
    logBioaccumulationFactor: Optional[float] = None
    biotransformationFactors: Optional[List[BiotransformationFactor]] = None
    biotransformationRateConstants: Optional[List[BiotransformationRateConstant]] = None
    bioconcentrationFactors: Optional[List[BioconcentrationFactor]] = None
    biocontrationFactorEquation: Optional[str] = None
    biocontrationFactorEquationSum: Optional[float] = None
    arnotGobasBcfBafEstimates: Optional[List[ArnotGobasBcfBafEstimate]] = None
    notes: Optional[str] = None
    output: Optional[str] = None

@dataclass
class WaterVolatilizationParameters:
    molecularWeight: Optional[NumericParameter] = None
    henrysLawConstant: Optional[NumericParameter] = None
    riverWaterDepthMeters: Optional[NumericParameter] = None
    riverWindVelocityMetersPerSecond: Optional[NumericParameter] = None
    riverCurrentVelocityMetersPerSecond: Optional[NumericParameter] = None
    lakeWindVelocityMetersPerSecond: Optional[NumericParameter] = None
    lakeCurrentVelocityMetersPerSecond: Optional[NumericParameter] = None
    lakeWaterDepthMeters: Optional[NumericParameter] = None

@dataclass
class WaterVolatilizationResponse:
    parameters: Optional[WaterVolatilizationParameters] = None
    riverHalfLifeHours: Optional[float] = None
    lakeHalfLifeHours: Optional[float] = None

# SewageTreatmentModelParameters dataclass
@dataclass
class SewageTreatmentModelParameters:
    molecularWeight: Optional[NumericParameter] = None
    henrysLawConstant: Optional[NumericParameter] = None
    waterSolubility: Optional[NumericParameter] = None
    vaporPressure: Optional[NumericParameter] = None
    logKow: Optional[NumericParameter] = None
    biowin3: Optional[NumericParameter] = None
    biowin5: Optional[NumericParameter] = None
    halfLifeHoursPrimaryClarifier: Optional[NumericParameter] = None
    halfLifeHoursAerationVessel: Optional[NumericParameter] = None
    halfLifeHoursSettlingTank: Optional[NumericParameter] = None

# Base ModelComponent dataclass
@dataclass
class SewageModelComponent:
    MassPerHour: Optional[float] = None
    MolPerHour: Optional[float] = None
    Percent: Optional[float] = None

@dataclass
class SewageModelComponents:
    Influent: Optional[SewageModelComponent] = None
    PrimarySludge: Optional[SewageModelComponent] = None
    WasteSludge: Optional[SewageModelComponent] = None
    TotalSludge: Optional[SewageModelComponent] = None
    PrimVloitilization: Optional[SewageModelComponent] = None
    SettlingVloitilization: Optional[SewageModelComponent] = None
    AerationOffGas: Optional[SewageModelComponent] = None
    TotalAir: Optional[SewageModelComponent] = None
    PrimBiodeg: Optional[SewageModelComponent] = None
    SettlingBiodeg: Optional[SewageModelComponent] = None
    AerationBiodeg: Optional[SewageModelComponent] = None
    TotalBiodeg: Optional[SewageModelComponent] = None
    FinalEffluent: Optional[SewageModelComponent] = None
    TotalRemoval: Optional[SewageModelComponent] = None
    PrimaryRateConstant: Optional[SewageModelComponent] = None
    AerationRateConstant: Optional[SewageModelComponent] = None
    SettlingRateConstant: Optional[SewageModelComponent] = None
    CalculationVariables: Optional[List[Optional[float]]] = None

@dataclass
class SewageTreatmentModelResponse:
    parameters: Optional[SewageTreatmentModelParameters] = None
    model: Optional[SewageModelComponents] = None

@dataclass
class FugacityModelParameters:
    henrysLawConstant: Optional[NumericParameter] = None
    logKow: Optional[NumericParameter] = None
    logKoc: Optional[NumericParameter] = None
    molecularWeight: Optional[NumericParameter] = None
    meltingPoint: Optional[NumericParameter] = None
    vaporPressure: Optional[NumericParameter] = None
    waterSolubility: Optional[NumericParameter] = None
    atmosphericHydroxylRateConstant: Optional[NumericParameter] = None
    ultimateBiodegradation: Optional[NumericParameter] = None
    halfLifeAir: Optional[NumericParameter] = None
    halfLifeWater: Optional[NumericParameter] = None
    halfLifeSoil: Optional[NumericParameter] = None
    halfLifeSediment: Optional[NumericParameter] = None
    emissionRateAir: Optional[NumericParameter] = None
    emissionRateWater: Optional[NumericParameter] = None
    emissionRateSoil: Optional[NumericParameter] = None
    emissionRateSediment: Optional[NumericParameter] = None
    advectionTimeAir: Optional[NumericParameter] = None
    advectionTimeWater: Optional[NumericParameter] = None
    advectionTimeSoil: Optional[NumericParameter] = None
    advectionTimeSediment: Optional[NumericParameter] = None

# ModelComponent dataclass
@dataclass
class FugacityModelComponent:
    MassAmount: Optional[float] = None
    HalfLife: Optional[float] = None
    Emissions: Optional[float] = None

# ModelComponents dataclass containing all model components
@dataclass
class FugacityModelComponents:
    Air: Optional[List[Optional[FugacityModelComponent]]] = None
    Water: Optional[List[Optional[FugacityModelComponent]]] = None
    Soil: Optional[List[Optional[FugacityModelComponent]]] = None
    Sediment: Optional[List[Optional[FugacityModelComponent]]] = None
    Persistence: Optional[float] = None
    aEmissionArray: Optional[List[Optional[float]]] = None
    aAdvectionTimeArray: Optional[List[Optional[float]]] = None
    aFugacities: Optional[List[Optional[float]]] = None
    aReaction: Optional[List[Optional[float]]] = None
    aAdvection: Optional[List[Optional[float]]] = None
    aReactionPercent: Optional[List[Optional[float]]] = None
    aAdvectionPercent: Optional[List[Optional[float]]] = None
    aSums: Optional[List[Optional[float]]] = None
    aTimes: Optional[List[Optional[float]]] = None
    HalfLifeArray: Optional[List[Optional[float]]] = None
    HalfLifeFactorArray: Optional[List[Optional[float]]] = None
    Emission: Optional[List[Optional[float]]] = None
    AdvectionTimesArray: Optional[List[Optional[float]]] = None
    aNotes: Optional[List[str]] = None

# FugacityModelResponse dataclass
@dataclass
class FugacityModelResponse:
    parameters: Optional[FugacityModelParameters] = None
    model: Optional[FugacityModelComponents] = None

# DermalPermeabilityParameters dataclass
@dataclass
class DermalPermeabilityParameters:
    smiles: Optional[str] = None
    logKow: Optional[NumericParameter] = None
    molecularWeight: Optional[NumericParameter] = None
    dermalPermeabilityCoefficient: Optional[NumericParameter] = None
    waterConcentrationMgPerLiter: Optional[NumericParameter] = None
    eventDurationHours: Optional[NumericParameter] = None
    fractionAbsorbedWater: Optional[NumericParameter] = None
    skinSurfaceAreaCm2: Optional[NumericParameter] = None
    exposureEventsPerDay: Optional[NumericParameter] = None
    exposureDurationYears: Optional[NumericParameter] = None
    exposureDaysPerYear: Optional[NumericParameter] = None
    bodyWeightKg: Optional[NumericParameter] = None
    averagingTimeDays: Optional[NumericParameter] = None

# DermalPermeabilityResponse dataclass
@dataclass
class DermalPermeabilityResponse:
    parameters: Optional[DermalPermeabilityParameters] = None
    dermalPermeabilityCoefficient: Optional[float] = None
    dermalAbsorbedDose: Optional[float] = None
    dermalAbsorbedDosePerEvent: Optional[float] = None
    lagTimePerEventHours: Optional[float] = None
    timeToReachSteadyStateHours: Optional[float] = None
    output: Optional[str] = None

# Main Result Class
@dataclass
class ResultEPISuite:
    parameters: Optional[Parameters] = None
    chemicalProperties: Optional[ChemicalProperties] = None
    logKow: Optional[LogKowResponse] = None
    meltingPoint: Optional[MeltingPointResponse] = None
    boilingPoint: Optional[BoilingPointResponse] = None
    vaporPressure: Optional[VaporPressureResponse] = None
    waterSolubilityFromLogKow: Optional[WaterSolubilityFromLogKowResponse] = None
    waterSolubilityFromWaterNt: Optional[WaterSolubilityFromWaterNtResponse] = None
    henrysLawConstant: Optional[HenrysLawConstantResponse] = None
    logKoa: Optional[LogKoaResponse] = None
    biodegradationRate: Optional[BiodegradationRateResponse] = None
    hydrocarbonBiodegradationRate: Optional[HydrocarbonBiodegradationRateResponse] = None
    aerosolAdsorptionFraction: Optional[AerosolAdsorptionFractionResponse] = None
    atmosphericHalfLife: Optional[AtmosphericHalfLifeResponse] = None
    logKoc: Optional[LogKocResponse] = None
    hydrolysis: Optional[HydrolysisResponse] = None
    bioconcentration: Optional[BioconcentrationResponse] = None
    waterVolatilization: Optional[WaterVolatilizationResponse] = None
    sewageTreatmentModel: Optional[SewageTreatmentModelResponse] = None
    fugacityModel: Optional[FugacityModelResponse] = None
    dermalPermeability: Optional[DermalPermeabilityResponse] = None
    analogs: Optional[List[str]] = None
    logKowAnalogs: Optional[List[str]] = None # possibly a bug in the web app

@dataclass
class EcosarParameters:
    smiles: Optional[str] = None
    cas: Optional[str] = None
    logKow: Optional[NumericParameter] = None
    waterSolubility: Optional[NumericParameter] = None
    meltingPoint: Optional[NumericParameter] = None

@dataclass
class ModelResult:
    qsarClass: Optional[str] = None
    organism: Optional[str] = None
    duration: Optional[str] = None
    endpoint: Optional[str] = None
    concentration: Optional[float] = None
    maxLogKow: Optional[float] = None
    flags: Optional[List[str]] = field(default_factory=list)  # Assuming flags are strings

@dataclass
class ResultEcoSAR:
    parameters: Optional[EcosarParameters] = None
    modelResults: Optional[List[ModelResult]] = None
    output: Optional[str] = None
    alerts: Optional[List[str]] = None