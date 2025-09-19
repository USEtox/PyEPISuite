# models.py
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

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
    name: Optional[str]
    smiles: Optional[str]
    cas: Optional[str]

@dataclass
class Parameter:
    value: Optional[float]
    units: Optional[str]
    valueType: Optional[str]

@dataclass
class Coefficient:
    type: Optional[str]
    value: Optional[float]
    unit: Optional[str]

@dataclass
class Parameters:
    cas: Optional[str]
    smiles: Optional[str]
    caseNumber: Optional[str]
    userLogKow: Optional[Parameter]
    userMeltingPoint: Optional[Parameter]
    userBoilingPoint: Optional[Parameter]
    userWaterSolubility: Optional[Parameter]
    userVaporPressure: Optional[Parameter]
    userHenrysLawConstant: Optional[Parameter]
    userLogKoa: Optional[Parameter]
    userLogKoc: Optional[Parameter]
    userHydroxylReactionRateConstant: Optional[Parameter]
    userDermalPermeabilityCoefficient: Optional[Parameter]
    userBiodegradationRateRemoveMetals: Optional[Parameter]
    userAtmosphericHydroxylRadicalConcentration: Optional[Parameter]
    userAtmosphericOzoneConcentration: Optional[Parameter]
    userAtmosphericDaylightHours: Optional[Parameter]
    userStpHalfLifePrimaryClarifier: Optional[Parameter]
    userStpHalfLifeAerationVessel: Optional[Parameter]
    userStpHalfLifeSettlingTank: Optional[Parameter]
    userFugacityHalfLifeAir: Optional[Parameter]
    userFugacityHalfLifeWater: Optional[Parameter]
    userFugacityHalfLifeSoil: Optional[Parameter]
    userFugacityHalfLifeSediment: Optional[Parameter]
    userFugacityEmissionRateAir: Optional[Parameter]
    userFugacityEmissionRateWater: Optional[Parameter]
    userFugacityEmissionRateSoil: Optional[Parameter]
    userFugacityEmissionRateSediment: Optional[Parameter]
    userFugacityAdvectionTimeAir: Optional[Parameter]
    userFugacityAdvectionTimeWater: Optional[Parameter]
    userFugacityAdvectionTimeSoil: Optional[Parameter]
    userFugacityAdvectionTimeSediment: Optional[Parameter]
    modules: Optional[List[str]] = None

@dataclass
class ChemicalProperties:
    name: Optional[str]
    systematicName: Optional[str]
    cas: Optional[str]
    smiles: Optional[str]
    molecularWeight: Optional[float]
    molecularFormula: Optional[str]
    molecularFormulaHtml: Optional[str]
    organic: Optional[bool]
    organicAcid: Optional[bool]
    aminoAcid: Optional[bool]
    nonStandardMetal: Optional[bool]
    flags: Optional[Dict[str, bool]]

# Common Response Classes
@dataclass
class Flag:
    isOrganicAcid: Optional[bool]
    isAminoAcid: Optional[bool]

@dataclass
class KowFactor:
    type: Optional[str]
    description: Optional[str]
    fragmentCount: Optional[int]
    coefficient: Optional[float]
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
    model: Optional[KowModel]
    value: Optional[float]
    units: Optional[str]
    valueType: Optional[str]

@dataclass
class ExperimentalValue:
    author: Optional[str]
    year: Optional[int]
    order: Optional[int]
    value: Optional[float]
    units: Optional[str]
    valueType: Optional[str]

@dataclass
class SelectedValue:
    value: Optional[float]
    units: Optional[str]
    valueType: Optional[str]

# Specific Response Classes
@dataclass
class LogKowResponse:
    estimatedValue: Optional[logKowEstimatedValue]
    experimentalValues: Optional[List[ExperimentalValue]]
    selectedValue: Optional[SelectedValue]

# MeltingPointFactor dataclass
@dataclass
class MeltingPointFactor:
    type: Optional[str]
    description: Optional[str]
    fragmentCount: Optional[int]
    coefficient: Optional[float]
    totalCoefficient: Optional[float]

# MeltingPointModel dataclass
@dataclass
class MeltingPointModel:
    factors: Optional[List[MeltingPointFactor]]
    meltingPointKelvins: Optional[float]
    meltingPointLimitKelvins: Optional[float]
    meltingPointCelsius: Optional[float]
    meltingPointAdaptedJoback: Optional[float]
    meltingPointGoldOgle: Optional[float]
    meltingPointMean: Optional[float]
    meltingPointSelected: Optional[float]

# MeltingPointEstimatedValue dataclass
@dataclass
class MeltingPointEstimatedValue:
    model: Optional[MeltingPointModel]
    value: Optional[float]
    units: Optional[str]
    valueType: Optional[str]

# MeltingPointResponse dataclass
@dataclass
class MeltingPointResponse:
    estimatedValue: Optional[MeltingPointEstimatedValue]
    experimentalValues: Optional[List[ExperimentalValue]]
    selectedValue: Optional[SelectedValue]

# BoilingPointFactor dataclass
@dataclass
class BoilingPointFactor:
    type: Optional[str]
    description: Optional[str]
    fragmentCount: Optional[int]
    coefficient: Optional[float]
    totalCoefficient: Optional[float]

# BoilingPointModel dataclass
@dataclass
class BoilingPointModel:
    factors: Optional[List[BoilingPointFactor]]
    boilingPointKelvinsUncorrected: Optional[float]
    boilingPointKelvinsCorrected: Optional[float]
    boilingPointCelsius: Optional[float]

# BoilingPointEstimatedValue dataclass
@dataclass
class BoilingPointEstimatedValue:
    model: Optional[BoilingPointModel]
    value: Optional[float]
    units: Optional[str]
    valueType: Optional[str]

# BoilingPointResponse dataclass
@dataclass
class BoilingPointResponse:
    estimatedValue: Optional[BoilingPointEstimatedValue]
    experimentalValues: Optional[List[ExperimentalValue]]
    selectedValue: Optional[SelectedValue]

# VaporPressureModelItem dataclass
@dataclass
class VaporPressureModelItem:
    type: Optional[str]
    mmHg: Optional[float]
    pa: Optional[float]

# VaporPressureEstimatedValue dataclass
@dataclass
class VaporPressureEstimatedValue:
    model: Optional[List[VaporPressureModelItem]]
    value: Optional[float]
    units: Optional[str]
    valueType: Optional[str]

# VaporPressureResponse dataclass
@dataclass
class VaporPressureResponse:
    estimatedValue: Optional[VaporPressureEstimatedValue]
    experimentalValues: Optional[List[ExperimentalValue]]
    selectedValue: Optional[SelectedValue]

@dataclass
class WaterSolubilityFromLogKowFactor:
    type: Optional[str]
    description: Optional[str]
    fragmentCount: Optional[int]
    coefficient: Optional[float]
    totalCoefficient: Optional[float]
    trainingCount: Optional[int] = None
    maxFragmentCount: Optional[int] = None

# WaterSolubilityModel dataclass
@dataclass
class WaterSolubilityModel:
    waterSolubility: Optional[float]
    factors: Optional[List[WaterSolubilityFromLogKowFactor]]
    equation: Optional[str]
    notes: Optional[str]
    output: Optional[str]

# WaterSolubilityEstimatedValue dataclass
@dataclass
class WaterSolubilityEstimatedValue:
    model: Optional[WaterSolubilityModel]
    value: Optional[float]
    units: Optional[str]
    valueType: Optional[str]

# WaterSolubilityFromLogKowParameters dataclass
@dataclass
class WaterSolubilityFromLogKowParameters:
    smiles: Optional[str]
    cas: Optional[str]
    logKow: Optional[Parameter]
    meltingPoint: Optional[Parameter]

# WaterSolubilityFromLogKowResponse dataclass
@dataclass
class WaterSolubilityFromLogKowResponse:
    parameters: Optional[WaterSolubilityFromLogKowParameters]
    estimatedValue: Optional[WaterSolubilityEstimatedValue]
    experimentalValues: Optional[List[ExperimentalValue]]
    selectedValue: Optional[SelectedValue]

# WaterSolubilityFromWaterNtFactor dataclass
@dataclass
class WaterSolubilityFromWaterNtFactor:
    type: Optional[str]
    description: Optional[str]
    fragmentCount: Optional[int]
    coefficient: Optional[float]
    totalCoefficient: Optional[float]
    trainingCount: Optional[int]
    maxFragmentCount: Optional[int]

# WaterSolubilityFromWaterNtModel dataclass
@dataclass
class WaterSolubilityFromWaterNtModel:
    waterSolubility: Optional[float]
    factors: Optional[List[WaterSolubilityFromWaterNtFactor]]
    equation: Optional[str]
    notes: Optional[str]
    output: Optional[str]

# WaterSolubilityFromWaterNtEstimatedValue dataclass
@dataclass
class WaterSolubilityFromWaterNtEstimatedValue:
    model: Optional[WaterSolubilityFromWaterNtModel]
    value: Optional[float]
    units: Optional[str]
    valueType: Optional[str]

# WaterSolubilityFromWaterNtParameters dataclass
@dataclass
class WaterSolubilityFromWaterNtParameters:
    smiles: Optional[str]
    cas: Optional[str]

# WaterSolubilityFromWaterNtResponse dataclass
@dataclass
class WaterSolubilityFromWaterNtResponse:
    parameters: Optional[WaterSolubilityFromWaterNtParameters]
    estimatedValue: Optional[WaterSolubilityFromWaterNtEstimatedValue]
    experimentalValues: Optional[List[ExperimentalValue]]
    selectedValue: Optional[SelectedValue]

# HenrysLawConstantFactor dataclass
@dataclass
class HenrysLawConstantFactor:
    type: Optional[str]
    description: Optional[str]
    fragmentCount: Optional[int]
    totalCoefficient: Optional[float]
    trainingCount: Optional[int]
    maxFragmentCount: Optional[int]

# HenrysLawConstantModelItem dataclass
@dataclass
class HenrysLawConstantModelItem:
    name: Optional[str]
    value: Optional[float]
    factors: Optional[List[HenrysLawConstantFactor]]
    hlcAtm: Optional[float]
    hlcUnitless: Optional[float]
    hlcPaMol: Optional[float]
    notes: Optional[str]

# HenrysLawConstantEstimatedValue dataclass
@dataclass
class HenrysLawConstantEstimatedValue:
    model: Optional[List[HenrysLawConstantModelItem]]
    value: Optional[float]
    units: Optional[str]
    valueType: Optional[str]

# HenrysLawConstantParameters dataclass
@dataclass
class HenrysLawConstantParameters:
    smiles: Optional[str]
    cas: Optional[str]
    waterSolubility: Optional[Parameter]
    vaporPressure: Optional[Parameter]
    molecularWeight: Optional[Parameter]

# HenrysLawConstantResponse dataclass
@dataclass
class HenrysLawConstantResponse:
    parameters: Optional[HenrysLawConstantParameters]
    estimatedValue: Optional[HenrysLawConstantEstimatedValue]
    experimentalValues: Optional[List[ExperimentalValue]]
    selectedValue: Optional[SelectedValue]

# LogKoaModel dataclass
@dataclass
class LogKoaModel:
    kow: Optional[float]
    kaw: Optional[float]
    koa: Optional[float]
    logKoa: Optional[float]

# LogKoaEstimatedValue dataclass
@dataclass
class LogKoaEstimatedValue:
    model: Optional[LogKoaModel]
    value: Optional[float]
    units: Optional[str]
    valueType: Optional[str]

# LogKoaParameters dataclass
@dataclass
class LogKoaParameters:
    smiles: Optional[str]
    cas: Optional[str]
    logKow: Optional[Parameter]
    henrysLawConstant: Optional[Parameter]

# LogKoaResponse dataclass
@dataclass
class LogKoaResponse:
    parameters: Optional[LogKoaParameters]
    estimatedValue: Optional[LogKoaEstimatedValue]
    experimentalValues: Optional[List[ExperimentalValue]]
    selectedValue: Optional[SelectedValue]

# BiodegradationRateFactor dataclass
@dataclass
class BiodegradationRateFactor:
    type: Optional[str]
    description: Optional[str]
    fragmentCount: Optional[int]
    coefficient: Optional[float]
    totalCoefficient: Optional[float]
    trainingCount: Optional[int]
    maxFragmentCount: Optional[int]

# BiodegradationRateModel dataclass
@dataclass
class BiodegradationRateModel:
    name: Optional[str]
    value: Optional[float]
    factors: Optional[List[BiodegradationRateFactor]]

# BiodegradationRateParameters dataclass
@dataclass
class BiodegradationRateParameters:
    smiles: Optional[str]
    cas: Optional[str]
    removeMetals: Optional[bool]

# BiodegradationRateResponse dataclass
@dataclass
class BiodegradationRateResponse:
    parameters: Optional[BiodegradationRateParameters]
    models: Optional[List[BiodegradationRateModel]]
    notes: Optional[str]
    output: Optional[str]

# HydrocarbonBiodegradationRateModelFactor dataclass
@dataclass
class HydrocarbonBiodegradationRateModelFactor:
    type: Optional[str]
    description: Optional[str]
    fragmentCount: Optional[int]
    coefficient: Optional[float]
    totalCoefficient: Optional[float]
    trainingCount: Optional[int]
    maxFragmentCount: Optional[int]

# HydrocarbonBiodegradationRateModel dataclass
@dataclass
class HydrocarbonBiodegradationRateModel:
    halfLifeDays: Optional[float]
    logHalfLifeDays: Optional[float]
    factors: Optional[List[HydrocarbonBiodegradationRateModelFactor]]
    notes: Optional[str]
    output: Optional[str]

# HydrocarbonBiodegradationRateEstimatedValue dataclass
@dataclass
class HydrocarbonBiodegradationRateEstimatedValue:
    model: Optional[HydrocarbonBiodegradationRateModel]
    value: Optional[float]
    units: Optional[str]
    valueType: Optional[str]

# HydrocarbonBiodegradationRateParameters dataclass
@dataclass
class HydrocarbonBiodegradationRateParameters:
    smiles: Optional[str]
    cas: Optional[str]

# HydrocarbonBiodegradationRateResponse dataclass
@dataclass
class HydrocarbonBiodegradationRateResponse:
    parameters: Optional[HydrocarbonBiodegradationRateParameters]
    estimatedValue: Optional[HydrocarbonBiodegradationRateEstimatedValue]
    selectedValue: Optional[SelectedValue]

# AerosolAdsorptionFractionModel dataclass
@dataclass
class AerosolAdsorptionFractionModel:
    mackayParticleGasPartitionCoefficient: Optional[float]
    koaParticleGasPartitionCoefficient: Optional[float]
    mackayAdsorptionFraction: Optional[float]
    koaAdsorptionFraction: Optional[float]
    jungePankowAdsorptionFraction: Optional[float]

# AerosolAdsorptionFractionEstimatedValue dataclass
@dataclass
class AerosolAdsorptionFractionEstimatedValue:
    model: Optional[AerosolAdsorptionFractionModel]
    value: Optional[float]
    units: Optional[str]
    valueType: Optional[str]

# AerosolAdsorptionFractionParameters dataclass
@dataclass
class AerosolAdsorptionFractionParameters:
    logKoa: Optional[Parameter]
    subcooledVaporPressure: Optional[Parameter]

# AerosolAdsorptionFractionResponse dataclass
@dataclass
class AerosolAdsorptionFractionResponse:
    parameters: Optional[AerosolAdsorptionFractionParameters]
    estimatedValue: Optional[AerosolAdsorptionFractionEstimatedValue]
    selectedValue: Optional[SelectedValue]

# ReactionFactor dataclass
@dataclass
class ReactionFactor:
    type: Optional[str]
    value: Optional[float]
    unit: Optional[str]

# ReactionModel dataclass
@dataclass
class ReactionModel:
    type: Optional[str]
    rateConstant: Optional[float]
    halfLifeHours: Optional[float]
    factors: Optional[List[ReactionFactor]] = None

# EstimatedValueModel dataclass
@dataclass
class EstimatedValueModel:
    models: Optional[List[ReactionModel]]
    notes: Optional[str]
    output: Optional[str]

# EstimatedValue dataclass
@dataclass
class EstimatedValue:
    model: Optional[EstimatedValueModel]
    value: Optional[float]
    units: Optional[str]
    valueType: Optional[str]

# EstimatedHydroxylRadicalReactionRateConstantModel dataclass
@dataclass
class EstimatedHydroxylRadicalReactionRateConstantModel:
    type: Optional[str]
    rateConstant: Optional[float]
    halfLifeHours: Optional[float]
    factors: Optional[List[ReactionFactor]] = None

# EstimatedHydroxylRadicalReactionRateConstant dataclass
@dataclass
class EstimatedHydroxylRadicalReactionRateConstant:
    model: Optional[EstimatedHydroxylRadicalReactionRateConstantModel]
    value: Optional[float]
    units: Optional[str]
    valueType: Optional[str]

# EstimatedOzoneReactionRateConstantModel dataclass
@dataclass
class EstimatedOzoneReactionRateConstantModel:
    type: Optional[str]
    rateConstant: Optional[float]
    halfLifeHours: Optional[float]
    factors: Optional[List[ReactionFactor]] = None

# EstimatedOzoneReactionRateConstant dataclass
@dataclass
class EstimatedOzoneReactionRateConstant:
    model: Optional[EstimatedOzoneReactionRateConstantModel]
    value: Optional[float]
    units: Optional[str]
    valueType: Optional[str]

# ExperimentalReactionRateConstant dataclass
@dataclass
class ExperimentalReactionRateConstant:
    author: Optional[str]
    year: Optional[int]
    order: Optional[int]
    value: Optional[float]
    units: Optional[str]
    valueType: Optional[str]

# AtmosphericHalfLifeParameters dataclass
@dataclass
class AtmosphericHalfLifeParameters:
    smiles: Optional[str]
    cas: Optional[str]
    hydroxylRadicalConcentration: Optional[float]
    ozoneConcentration: Optional[float]
    twelveHourDay: Optional[bool]

# AtmosphericHalfLifeResponse dataclass
@dataclass
class AtmosphericHalfLifeResponse:
    parameters: Optional[AtmosphericHalfLifeParameters]
    estimatedValue: Optional[EstimatedValue]
    estimatedHydroxylRadicalReactionRateConstant: Optional[EstimatedHydroxylRadicalReactionRateConstant]
    estimatedOzoneReactionRateConstant: Optional[EstimatedOzoneReactionRateConstant]
    experimentalHydroxylRadicalReactionRateConstantValues: Optional[List[ExperimentalReactionRateConstant]]
    experimentalOzoneReactionRateConstantValues: Optional[List[ExperimentalReactionRateConstant]]
    experimentalNitrateReactionRateConstantValues: Optional[List[ExperimentalReactionRateConstant]]
    selectedHydroxylRadicalReactionRateConstant: Optional[SelectedValue]
    selectedOzoneReactionRateConstantValues: Optional[SelectedValue]

# LogKocFactor dataclass
@dataclass
class LogKocFactor:
    fragmentCount: Optional[int]
    trainingCount: Optional[int]
    maxFragmentCount: Optional[int]
    description: Optional[str]
    coefficient: Optional[float]
    totalCoefficient: Optional[float]

# LogKocModelItem dataclass
@dataclass
class LogKocModelItem:
    firstOrderMCI: Optional[float]
    name: Optional[str]
    factors: Optional[List[LogKocFactor]]
    nonCorrectedLogKoc: Optional[float]
    correctedLogKoc: Optional[float]
    koc: Optional[float]
    logKow: Optional[float] = None

# LogKocModel dataclass
@dataclass
class LogKocModel:
    logKoc: Optional[float]
    models: Optional[List[LogKocModelItem]]
    notes: Optional[str]
    output: Optional[str]

# LogKocEstimatedValue dataclass
@dataclass
class LogKocEstimatedValue:
    model: Optional[LogKocModel]
    value: Optional[float]
    units: Optional[str]
    valueType: Optional[str]

# LogKocParameters dataclass
@dataclass
class LogKocParameters:
    smiles: Optional[str]
    cas: Optional[str]
    logKow: Optional[Parameter]

# LogKocResponse dataclass
@dataclass
class LogKocResponse:
    parameters: Optional[LogKocParameters]
    experimentalValues: Optional[List[ExperimentalValue]]
    estimatedValue: Optional[LogKocEstimatedValue]
    selectedValue: Optional[SelectedValue]

# HydrolysisHalfLife dataclass
@dataclass
class HydrolysisHalfLife:
    ph: Optional[float]
    value: Optional[float]
    unit: Optional[str]
    baseCatalyzed: Optional[bool]
    acidCatalyzed: Optional[bool]
    phosphorusEster: Optional[bool]
    isomer: Optional[str]

# HydrolysisFragment dataclass
@dataclass
class HydrolysisFragment:
    # Define fields if available
    pass

# HydrolysisResponse dataclass
@dataclass
class HydrolysisResponse:
    halfLives: Optional[List[HydrolysisHalfLife]]
    phosphorusEsterHalfLives: Optional[List[HydrolysisHalfLife]]
    fragments: Optional[List[HydrolysisFragment]]
    baseCatalyzedRateConstant: Optional[float]
    acidCatalyzedRateConstant: Optional[float]
    acidCatalyzedRateConstantForTransIsomer: Optional[float]
    neutralRateConstant: Optional[float]
    output: Optional[str]

# BioconcentrationParameters dataclass
@dataclass
class BioconcentrationParameters:
    smiles: Optional[str]
    cas: Optional[str]
    logKow: Optional[Parameter]

# BiotransformationFactor dataclass
@dataclass
class BiotransformationFactor:
    type: Optional[str]
    description: Optional[str]
    fragmentCount: Optional[int]
    coefficient: Optional[float]
    totalCoefficient: Optional[float]
    trainingCount: Optional[int]
    maxFragmentCount: Optional[int]

# BiotransformationRateConstant dataclass
@dataclass
class BiotransformationRateConstant:
    type: Optional[str]
    value: Optional[float]
    unit: Optional[str]

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
    trophicLevel: Optional[str]
    trophicLevelNote: Optional[str]
    bioconcentrationFactor: Optional[float]
    logBioconcentrationFactor: Optional[float]
    bioaccumulationFactor: Optional[float]
    logBioaccumulationFactor: Optional[float]
    unit: Optional[str]

# BioconcentrationResponse dataclass
@dataclass
class BioconcentrationResponse:
    parameters: Optional[BioconcentrationParameters]
    bioconcentrationFactor: Optional[float]
    experimentalBioconcentrationFactor: Optional[float]
    experimentalBioTransformationRate: Optional[float]
    logBioconcentrationFactor: Optional[float]
    biotransformationHalfLife: Optional[float]
    bioaccumulationFactor: Optional[float]
    logBioaccumulationFactor: Optional[float]
    biotransformationFactors: Optional[List[BiotransformationFactor]]
    biotransformationRateConstants: Optional[List[BiotransformationRateConstant]]
    bioconcentrationFactors: Optional[List[BioconcentrationFactor]]
    biocontrationFactorEquation: Optional[str]
    biocontrationFactorEquationSum: Optional[float]
    arnotGobasBcfBafEstimates: Optional[List[ArnotGobasBcfBafEstimate]]
    notes: Optional[str]
    output: Optional[str]

@dataclass
class WaterVolatilizationParameters:
    molecularWeight: Optional[float]
    henrysLawConstant: Optional[Parameter]  # Reusing the existing Parameter dataclass
    riverWaterDepthMeters: Optional[float]
    riverWindVelocityMetersPerSecond: Optional[float]
    riverCurrentVelocityMetersPerSecond: Optional[float]
    lakeWindVelocityMetersPerSecond: Optional[float]
    lakeCurrentVelocityMetersPerSecond: Optional[float]
    lakeWaterDepthMeters: Optional[float]

@dataclass
class WaterVolatilizationResponse:
    parameters: Optional[WaterVolatilizationParameters]
    riverHalfLifeHours: Optional[float]
    lakeHalfLifeHours: Optional[float]

# SewageTreatmentModelParameters dataclass
@dataclass
class SewageTreatmentModelParameters:
    molecularWeight: Optional[Parameter]
    henrysLawConstant: Optional[Parameter]
    waterSolubility: Optional[Parameter]
    vaporPressure: Optional[Parameter]
    logKow: Optional[Parameter]
    biowin3: Optional[Parameter]
    biowin5: Optional[Parameter]
    halfLifeHoursPrimaryClarifier: Optional[Parameter]
    halfLifeHoursAerationVessel: Optional[Parameter]
    halfLifeHoursSettlingTank: Optional[Parameter]

# Base ModelComponent dataclass
@dataclass
class SewageModelComponent:
    MassPerHour: Optional[float]
    MolPerHour: Optional[float]
    Percent: Optional[float]

@dataclass
class SewageModelComponents:
    Influent: Optional[SewageModelComponent]
    PrimarySludge: Optional[SewageModelComponent]
    WasteSludge: Optional[SewageModelComponent]
    TotalSludge: Optional[SewageModelComponent]
    PrimVloitilization: Optional[SewageModelComponent]
    SettlingVloitilization: Optional[SewageModelComponent]
    AerationOffGas: Optional[SewageModelComponent]
    TotalAir: Optional[SewageModelComponent]
    PrimBiodeg: Optional[SewageModelComponent]
    SettlingBiodeg: Optional[SewageModelComponent]
    AerationBiodeg: Optional[SewageModelComponent]
    TotalBiodeg: Optional[SewageModelComponent]
    FinalEffluent: Optional[SewageModelComponent]
    TotalRemoval: Optional[SewageModelComponent]
    PrimaryRateConstant: Optional[SewageModelComponent]
    AerationRateConstant: Optional[SewageModelComponent]
    SettlingRateConstant: Optional[SewageModelComponent]
    CalculationVariables: Optional[List[float]]

@dataclass
class SewageTreatmentModelResponse:
    parameters: Optional[SewageTreatmentModelParameters]
    model: Optional[SewageModelComponents]

@dataclass
class FugacityModelParameters:
    henrysLawConstant: Optional[Parameter]
    logKow: Optional[Parameter]
    logKoc: Optional[Parameter]
    molecularWeight: Optional[Parameter]
    meltingPoint: Optional[Parameter]
    vaporPressure: Optional[Parameter]
    waterSolubility: Optional[Parameter]
    atmosphericHydroxylRateConstant: Optional[Parameter]
    ultimateBiodegradation: Optional[Parameter]
    halfLifeAir: Optional[Parameter]
    halfLifeWater: Optional[Parameter]
    halfLifeSoil: Optional[Parameter]
    halfLifeSediment: Optional[Parameter]
    emissionRateAir: Optional[Parameter]
    emissionRateWater: Optional[Parameter]
    emissionRateSoil: Optional[Parameter]
    emissionRateSediment: Optional[Parameter]
    advectionTimeAir: Optional[Parameter]
    advectionTimeWater: Optional[Parameter]
    advectionTimeSoil: Optional[Parameter]
    advectionTimeSediment: Optional[Parameter]

# ModelComponent dataclass
@dataclass
class FugacityModelComponent:
    MassAmount: Optional[float]
    HalfLife: Optional[float]
    Emissions: Optional[float]

# ModelComponents dataclass containing all model components
@dataclass
class FugacityModelComponents:
    Air: List[Optional[FugacityModelComponent]]
    Water: List[Optional[FugacityModelComponent]]
    Soil: List[Optional[FugacityModelComponent]]
    Sediment: List[Optional[FugacityModelComponent]]
    Persistence: Optional[float]
    aEmissionArray: Optional[List[float]]
    aAdvectionTimeArray: Optional[List[float]]
    aFugacities: Optional[List[float]]
    aReaction: Optional[List[float]]
    aAdvection: Optional[List[float]]
    aReactionPercent: Optional[List[float]]
    aAdvectionPercent: Optional[List[float]]
    aSums: Optional[List[float]]
    aTimes: Optional[List[float]]
    HalfLifeArray: Optional[List[float]]
    HalfLifeFactorArray: Optional[List[float]]
    Emission: Optional[List[float]]
    AdvectionTimesArray: Optional[List[float]]
    aNotes: Optional[List[str]]

# FugacityModelResponse dataclass
@dataclass
class FugacityModelResponse:
    parameters: Optional[FugacityModelParameters]
    model: Optional[FugacityModelComponents]

# DermalPermeabilityParameters dataclass
@dataclass
class DermalPermeabilityParameters:
    smiles: Optional[str]
    logKow: Optional[Parameter]
    molecularWeight: Optional[Parameter]
    dermalPermeabilityCoefficient: Optional[Parameter]
    waterConcentrationMgPerLiter: Optional[Parameter]
    eventDurationHours: Optional[float]
    fractionAbsorbedWater: Optional[float]
    skinSurfaceAreaCm2: Optional[float]
    exposureEventsPerDay: Optional[float]
    exposureDurationYears: Optional[float]
    exposureDaysPerYear: Optional[float]
    bodyWeightKg: Optional[float]
    averagingTimeDays: Optional[float]

# DermalPermeabilityResponse dataclass
@dataclass
class DermalPermeabilityResponse:
    parameters: Optional[DermalPermeabilityParameters]
    dermalPermeabilityCoefficient: Optional[float]
    dermalAbsorbedDose: Optional[float]
    dermalAbsorbedDosePerEvent: Optional[float]
    lagTimePerEventHours: Optional[float]
    timeToReachSteadyStateHours: Optional[float]
    output: Optional[str]

# Main Result Class
@dataclass
class ResultEPISuite:
    parameters: Optional[Parameters]
    chemicalProperties: Optional[ChemicalProperties]
    logKow: Optional[LogKowResponse]
    meltingPoint: Optional[MeltingPointResponse]
    boilingPoint: Optional[BoilingPointResponse]
    vaporPressure: Optional[VaporPressureResponse]
    waterSolubilityFromLogKow: Optional[WaterSolubilityFromLogKowResponse]
    waterSolubilityFromWaterNt: Optional[WaterSolubilityFromWaterNtResponse]
    henrysLawConstant: Optional[HenrysLawConstantResponse]
    logKoa: Optional[LogKoaResponse]
    biodegradationRate: Optional[BiodegradationRateResponse]
    hydrocarbonBiodegradationRate: Optional[HydrocarbonBiodegradationRateResponse]
    aerosolAdsorptionFraction: Optional[AerosolAdsorptionFractionResponse]
    atmosphericHalfLife: Optional[AtmosphericHalfLifeResponse]
    logKoc: Optional[LogKocResponse]
    hydrolysis: Optional[HydrolysisResponse]
    bioconcentration: Optional[BioconcentrationResponse]
    waterVolatilization: Optional[WaterVolatilizationResponse]
    sewageTreatmentModel: Optional[SewageTreatmentModelResponse]
    fugacityModel: Optional[FugacityModelResponse]
    dermalPermeability: Optional[DermalPermeabilityResponse]
    analogs: Optional[List[str]] = None
    logKowAnalogs: Optional[List[str]] = None # possibly a bug in the web app

@dataclass
class EcosarParameters:
    smiles: Optional[str]
    cas: Optional[str]
    logKow: Optional[Parameter]
    waterSolubility: Optional[Parameter]
    meltingPoint: Optional[Parameter]

@dataclass
class ModelResult:
    qsarClass: Optional[str]
    organism: Optional[str]
    duration: Optional[str]
    endpoint: Optional[str]
    concentration: Optional[float]
    maxLogKow: Optional[float]
    flags: Optional[List[str]] = field(default_factory=list)  # Assuming flags are strings

@dataclass
class ResultEcoSAR:
    parameters: Optional[EcosarParameters]
    modelResults: Optional[List[ModelResult]]
    output: Optional[str]
    alerts: Optional[List[str]] = None