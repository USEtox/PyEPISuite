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
class ModuleError:
    """A module that failed to estimate, returned in place of its result.

    The three fields are deliberately required: that lets dacite tell an error
    payload apart from a real module result when resolving the
    ``Union[ModuleError, ...]`` used for every module on ``ResultEPISuite``.
    A normal result has none of these keys, so it falls through to the result
    type; only a genuine error object matches here.
    """
    module: str
    code: str
    message: str

@dataclass
class Value:
    """A measured, estimated or user-supplied quantity with its provenance.

    The v1.1.0 API models every value this way, whether it is an estimate, one
    of a property's experimental values, the selected value, or an echoed
    request parameter.
    """
    author: Optional[str] = None
    year: Optional[int] = None
    order: Optional[int] = None
    value: Optional[float] = None
    units: Optional[str] = None
    source: Optional[str] = None
    valueType: Optional[str] = None
    method: Optional[str] = None
    evidenceType: Optional[str] = None
    sourceDatabase: Optional[str] = None
    sourceTable: Optional[str] = None
    sourceId: Optional[int] = None
    referenceId: Optional[int] = None
    temperatureC: Optional[float] = None
    pressureMmHg: Optional[float] = None
    notes: Optional[str] = None

# The API models experimental values, selected values and echoed parameters
# with the single `Value` schema. These names are kept as aliases so existing
# attribute access keeps working.
Parameter = Value
ExperimentalValue = Value
SelectedValue = Value

# Many "parameters" fields that echo request inputs are returned by the API
# either as a bare scalar (when supplied directly) or as a full Value object
# carrying provenance (e.g. {"value": ..., "units": ..., "source": ...,
# "valueType": ...}) when resolved from a default or another module's output.
# Fields subject to this ambiguity are typed with these aliases instead of a
# single fixed type.
NumericParameter = Union[float, Value]
BoolParameter = Union[bool, Value]

@dataclass
class Coefficient:
    type: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None

@dataclass
class Parameters:
    """Request inputs echoed back by the API.

    Only the inputs actually supplied are present; everything else is absent.
    Names follow the v1.1.0 submit query parameters.
    """
    smiles: Optional[str] = None
    cas: Optional[str] = None
    chemicalName: Optional[str] = None
    logKow: Optional[NumericParameter] = None
    molecularWeight: Optional[NumericParameter] = None
    waterSolubilityMgPerL: Optional[NumericParameter] = None
    meltingPointC: Optional[NumericParameter] = None
    vaporPressureMmHg: Optional[NumericParameter] = None
    henryAtmM3PerMol: Optional[NumericParameter] = None
    logKoa: Optional[NumericParameter] = None
    koc: Optional[NumericParameter] = None
    boilingPointC: Optional[NumericParameter] = None
    subcooledVaporPressureMmHg: Optional[NumericParameter] = None
    aopRateConstant: Optional[NumericParameter] = None
    biowinScore: Optional[NumericParameter] = None
    biowin3: Optional[NumericParameter] = None
    biowin5: Optional[NumericParameter] = None
    tspUgPerM3: Optional[NumericParameter] = None
    theta: Optional[NumericParameter] = None
    userKpCmPerHour: Optional[NumericParameter] = None
    waterConcentrationMgPerCm3: Optional[NumericParameter] = None
    waterConcentrationMgPerLiter: Optional[NumericParameter] = None
    eventFrequencyPerDay: Optional[NumericParameter] = None
    exposureDurationYears: Optional[NumericParameter] = None
    exposureFrequencyDaysPerYear: Optional[NumericParameter] = None
    skinSurfaceAreaCm2: Optional[NumericParameter] = None
    bodyWeightKg: Optional[NumericParameter] = None
    averagingTimeDays: Optional[NumericParameter] = None
    fractionAbsorbed: Optional[NumericParameter] = None
    eventDurationHours: Optional[NumericParameter] = None
    halfLifeHoursPrimaryClarifier: Optional[NumericParameter] = None
    halfLifeHoursAerationVessel: Optional[NumericParameter] = None
    halfLifeHoursSettlingTank: Optional[NumericParameter] = None
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
    ohConcentrationE6OhPerCm3: Optional[NumericParameter] = None
    ozoneConcentrationE11MolPerCm3: Optional[NumericParameter] = None
    daylightHours: Optional[NumericParameter] = None
    riverWindMPerSec: Optional[NumericParameter] = None
    riverCurrentMPerSec: Optional[NumericParameter] = None
    riverDepthMeters: Optional[NumericParameter] = None
    lakeWindMPerSec: Optional[NumericParameter] = None
    lakeCurrentMPerSec: Optional[NumericParameter] = None
    lakeDepthMeters: Optional[NumericParameter] = None
    vaporPressureTemperatureC: Optional[NumericParameter] = None
    waterSolubilityProvider: Optional[str] = None
    removeMetals: Optional[BoolParameter] = None
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
    source: Optional[str] = None

# Specific Response Classes
@dataclass
class LogKowResponse:
    estimatedValue: Optional[logKowEstimatedValue] = None
    experimentalValues: Optional[List[ExperimentalValue]] = None
    selectedValue: Optional[SelectedValue] = None
    parameters: Optional[Dict[str, Any]] = None
    output: Optional[str] = None

# MeltingPointFactor dataclass
@dataclass
class MeltingPointFactor:
    type: Optional[str] = None
    description: Optional[str] = None
    count: Optional[int] = None
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
    source: Optional[str] = None

# MeltingPointResponse dataclass
@dataclass
class MeltingPointResponse:
    estimatedValue: Optional[MeltingPointEstimatedValue] = None
    experimentalValues: Optional[List[ExperimentalValue]] = None
    selectedValue: Optional[SelectedValue] = None
    parameters: Optional[Dict[str, Any]] = None
    output: Optional[str] = None

# BoilingPointFactor dataclass
@dataclass
class BoilingPointFactor:
    type: Optional[str] = None
    description: Optional[str] = None
    count: Optional[int] = None
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
    source: Optional[str] = None

# BoilingPointResponse dataclass
@dataclass
class BoilingPointResponse:
    estimatedValue: Optional[BoilingPointEstimatedValue] = None
    experimentalValues: Optional[List[ExperimentalValue]] = None
    selectedValue: Optional[SelectedValue] = None
    parameters: Optional[Dict[str, Any]] = None
    output: Optional[str] = None

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
    source: Optional[str] = None

# VaporPressureResponse dataclass
@dataclass
class VaporPressureResponse:
    estimatedValue: Optional[VaporPressureEstimatedValue] = None
    experimentalValues: Optional[List[ExperimentalValue]] = None
    selectedValue: Optional[SelectedValue] = None
    parameters: Optional[Dict[str, Any]] = None
    output: Optional[str] = None

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
    source: Optional[str] = None

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
    output: Optional[str] = None

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
    source: Optional[str] = None

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
    output: Optional[str] = None

# HenrysLawConstantFactor dataclass
@dataclass
class HenrysLawConstantFactor:
    type: Optional[str] = None
    description: Optional[str] = None
    comment: Optional[str] = None
    fragmentCount: Optional[int] = None
    coefficient: Optional[float] = None
    totalCoefficient: Optional[float] = None
    trainingCount: Optional[int] = None
    maxFragmentCount: Optional[int] = None
    correction: Optional[bool] = None

# HenrysLawConstantModelItem dataclass
#
# One HLC estimation method (bond, group or VP/WSol). `complete` says whether
# the method could run; `unavailableReason` and `missingValues` explain why not.
@dataclass
class HenrysLawConstantModelItem:
    name: Optional[str] = None
    complete: Optional[bool] = None
    unavailableReason: Optional[str] = None
    nativeValue: Optional[float] = None
    nativeUnits: Optional[str] = None
    value: Optional[float] = None
    hlcAtmM3PerMol: Optional[float] = None
    hlcUnitless: Optional[float] = None
    hlcPaM3PerMol: Optional[float] = None
    hasCorrectionFactor: Optional[bool] = None
    factors: Optional[List[HenrysLawConstantFactor]] = None
    missingValues: Optional[List[str]] = None
    notes: Optional[List[str]] = None

# HenrysLawConstantEstimatedValue dataclass
@dataclass
class HenrysLawConstantEstimatedValue:
    model: Optional[List[HenrysLawConstantModelItem]] = None
    value: Optional[float] = None
    units: Optional[str] = None
    valueType: Optional[str] = None
    source: Optional[str] = None

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
    selectedMethod: Optional[str] = None
    selectionReason: Optional[str] = None
    output: Optional[str] = None

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
    source: Optional[str] = None

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
    output: Optional[str] = None

# BiodegradationRateFactor dataclass
@dataclass
class BiodegradationRateFactor:
    type: Optional[str] = None
    description: Optional[str] = None
    count: Optional[int] = None
    coefficient: Optional[float] = None
    totalCoefficient: Optional[float] = None
    trainingCount: Optional[int] = None
    maxCount: Optional[int] = None

# BiodegradationRateModel dataclass
#
# One BIOWIN sub-model. The v1.1.0 API reports the raw model output as
# `nativeValue` and the value after unit/scale conversion as `calculatedValue`;
# there is no single `value` field any more.
@dataclass
class BiodegradationRateModel:
    index: Optional[int] = None
    number: Optional[int] = None
    name: Optional[str] = None
    shortName: Optional[str] = None
    nativeValue: Optional[float] = None
    calculatedValue: Optional[float] = None
    interpretation: Optional[str] = None
    factorCount: Optional[int] = None
    functionSemantic: Optional[str] = None
    formula: Optional[str] = None
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
    notes: Optional[List[str]] = None
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
    validationCount: Optional[int] = None

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
    source: Optional[str] = None

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
    experimentalValues: Optional[List[ExperimentalValue]] = None
    output: Optional[str] = None

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
    source: Optional[str] = None

# AerosolAdsorptionFractionParameters dataclass
@dataclass
class AerosolAdsorptionFractionParameters:
    logKoa: Optional[NumericParameter] = None
    subcooledVaporPressure: Optional[NumericParameter] = None
    smiles: Optional[str] = None
    cas: Optional[str] = None
    jungePankowCTheta: Optional[NumericParameter] = None
    totalSuspendedParticleConcentration: Optional[NumericParameter] = None

# AerosolAdsorptionFractionResponse dataclass
@dataclass
class AerosolAdsorptionFractionResponse:
    parameters: Optional[AerosolAdsorptionFractionParameters] = None
    estimatedValue: Optional[AerosolAdsorptionFractionEstimatedValue] = None
    selectedValue: Optional[SelectedValue] = None
    experimentalValues: Optional[List[ExperimentalValue]] = None
    output: Optional[str] = None

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
    source: Optional[str] = None

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
    source: Optional[str] = None

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
    source: Optional[str] = None

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
    daylightHours: Optional[NumericParameter] = None

# AtmosphericHalfLifeResponse dataclass
@dataclass
class AtmosphericHalfLifeResponse:
    parameters: Optional[AtmosphericHalfLifeParameters] = None
    estimatedValue: Optional[EstimatedValue] = None
    estimatedHydroxylRadicalReactionRateConstant: Optional[EstimatedHydroxylRadicalReactionRateConstant] = None
    estimatedOzoneReactionRateConstant: Optional[EstimatedOzoneReactionRateConstant] = None
    experimentalHydroxylRadicalReactionRateConstantValues: Optional[List[Value]] = None
    experimentalOzoneReactionRateConstantValues: Optional[List[Value]] = None
    experimentalNitrateReactionRateConstantValues: Optional[List[Value]] = None
    selectedHydroxylRadicalReactionRateConstant: Optional[SelectedValue] = None
    selectedOzoneReactionRateConstantValues: Optional[SelectedValue] = None
    output: Optional[str] = None

# LogKocFactor dataclass
@dataclass
class LogKocFactor:
    count: Optional[int] = None
    trainingCount: Optional[int] = None
    maxCount: Optional[int] = None
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
    source: Optional[str] = None

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
    output: Optional[str] = None

# Hydrolysis is reported per reactive site and per reaction pathway in
# v1.1.0. The flat acid/base/neutral rate constants of the previous API are
# now nested under `rates`, and half-lives carry their mechanism and pH.
@dataclass
class HydrolysisMessage:
    code: Optional[str] = None
    severity: Optional[str] = None
    text: Optional[str] = None

@dataclass
class HydrolysisSubstituent:
    attachment: Optional[str] = None
    fragment: Optional[str] = None

@dataclass
class HydrolysisRate:
    mechanism: Optional[str] = None
    status: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None
    logValue: Optional[float] = None
    logUnit: Optional[str] = None
    isomer: Optional[str] = None

@dataclass
class HydrolysisSite:
    atomNumber: Optional[int] = None
    chemicalClass: Optional[str] = None
    functionalGroup: Optional[str] = None
    substituents: Optional[List[HydrolysisSubstituent]] = None
    rates: Optional[List[HydrolysisRate]] = None
    messages: Optional[List[HydrolysisMessage]] = None

@dataclass
class HydrolysisPathwayHalfLife:
    mechanism: Optional[str] = None
    pH: Optional[int] = None
    isomer: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None

@dataclass
class HydrolysisPathway:
    family: Optional[str] = None
    chemicalClass: Optional[str] = None
    status: Optional[str] = None
    sites: Optional[List[HydrolysisSite]] = None
    rates: Optional[List[HydrolysisRate]] = None
    halfLives: Optional[List[HydrolysisPathwayHalfLife]] = None
    evidenceText: Optional[str] = None
    messages: Optional[List[HydrolysisMessage]] = None

# HydrolysisHalfLife dataclass
@dataclass
class HydrolysisHalfLife:
    status: Optional[str] = None
    mechanism: Optional[str] = None
    pH: Optional[int] = None
    isomer: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None
    originalValue: Optional[float] = None
    originalUnit: Optional[str] = None

@dataclass
class HydrolysisRateEstimate:
    status: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None
    basis: Optional[str] = None
    isomer: Optional[str] = None

@dataclass
class HydrolysisRates:
    baseCatalyzed: Optional[HydrolysisRateEstimate] = None
    acidCatalyzedPrimary: Optional[HydrolysisRateEstimate] = None
    acidCatalyzedTrans: Optional[HydrolysisRateEstimate] = None
    neutral: Optional[HydrolysisRateEstimate] = None

@dataclass
class HydrolysisPhosphorusEster:
    mode: Optional[str] = None

@dataclass
class HydrolysisFlags:
    zwitterion: Optional[bool] = None
    hasHydrolyzableFunctions: Optional[bool] = None
    hasPhosphorusEster: Optional[bool] = None
    hasAlerts: Optional[bool] = None

@dataclass
class HydrolysisReportParts:
    smiles: Optional[str] = None
    molecularWeight: Optional[str] = None
    summary: Optional[str] = None
    details: Optional[str] = None

# HydrolysisResponse dataclass
@dataclass
class HydrolysisResponse:
    parameters: Optional[Dict[str, Any]] = None
    disposition: Optional[str] = None
    pathways: Optional[List[HydrolysisPathway]] = None
    messages: Optional[List[HydrolysisMessage]] = None
    rates: Optional[HydrolysisRates] = None
    halfLives: Optional[List[HydrolysisHalfLife]] = None
    phosphorusEster: Optional[HydrolysisPhosphorusEster] = None
    flags: Optional[HydrolysisFlags] = None
    fragments: Optional[List[Dict[str, Any]]] = None
    notes: Optional[List[str]] = None
    alerts: Optional[List[str]] = None
    reportParts: Optional[HydrolysisReportParts] = None
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
    count: Optional[int] = None
    coefficient: Optional[float] = None
    totalCoefficient: Optional[float] = None
    trainingCount: Optional[int] = None
    trainingMaxCount: Optional[int] = None

# BiotransformationRateConstant dataclass
@dataclass
class BiotransformationRateConstant:
    type: Optional[str] = None
    rateConstant: Optional[float] = None
    units: Optional[str] = None

# BioconcentrationFactor dataclass
@dataclass
class BioconcentrationFactor:
    type: Optional[str] = None
    description: Optional[str] = None
    value: Optional[float] = None
    trainingCount: Optional[int] = None
    trainingMaxCount: Optional[int] = None

# ArnotGobasBcfBafEstimate dataclass
#
# v1.1.0 reports one titled estimate per row (e.g. "Estimated Log BCF (upper
# trophic)") instead of the previous per-trophic-level breakdown.
@dataclass
class ArnotGobasBcfBafEstimate:
    title: Optional[str] = None
    value: Optional[float] = None
    logValue: Optional[float] = None
    unit: Optional[str] = None

@dataclass
class BioconcentrationExperimentalEvidence:
    logBioconcentrationFactor: Optional[Value] = None
    logBiotransformationHalfLifeDays: Optional[Value] = None

@dataclass
class BioconcentrationFlags:
    ionic: Optional[bool] = None
    inorganic: Optional[bool] = None
    metalRemoved: Optional[bool] = None
    zwitterion: Optional[bool] = None
    hasAlerts: Optional[bool] = None

# BioconcentrationResponse dataclass
@dataclass
class BioconcentrationResponse:
    parameters: Optional[BioconcentrationParameters] = None
    bioconcentrationFactor: Optional[float] = None
    experimentalBioconcentrationFactor: Optional[float] = None
    experimentalLogBioconcentrationFactor: Optional[float] = None
    experimentalBioTransformationRate: Optional[float] = None
    experimentalBiotransformationHalfLife: Optional[float] = None
    experimentalLogBiotransformationHalfLife: Optional[float] = None
    experimentalEvidence: Optional[BioconcentrationExperimentalEvidence] = None
    logBioconcentrationFactor: Optional[float] = None
    biotransformationHalfLife: Optional[float] = None
    bioaccumulationFactor: Optional[float] = None
    logBioaccumulationFactor: Optional[float] = None
    biotransformationFactors: Optional[List[BiotransformationFactor]] = None
    biotransformationRateConstants: Optional[List[BiotransformationRateConstant]] = None
    bioconcentrationFactors: Optional[List[BioconcentrationFactor]] = None
    arnotGobasBcfBafEstimates: Optional[List[ArnotGobasBcfBafEstimate]] = None
    notes: Optional[List[str]] = None
    flags: Optional[BioconcentrationFlags] = None
    alerts: Optional[List[str]] = None
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
    smiles: Optional[str] = None
    cas: Optional[str] = None
    vaporPressure: Optional[NumericParameter] = None
    waterSolubility: Optional[NumericParameter] = None

@dataclass
class WaterVolatilizationResponse:
    parameters: Optional[WaterVolatilizationParameters] = None
    riverHalfLifeHours: Optional[float] = None
    lakeHalfLifeHours: Optional[float] = None
    output: Optional[str] = None

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
    smiles: Optional[str] = None
    cas: Optional[str] = None

# One row of the sewage treatment mass balance, e.g. category "air",
# process "primary volatilization".
@dataclass
class SewageModelComponent:
    category: Optional[str] = None
    process: Optional[str] = None
    massPerHour: Optional[float] = None
    molPerHour: Optional[float] = None
    percent: Optional[float] = None

@dataclass
class SewageEstimates:
    totalRemovalPercent: Optional[float] = None
    totalBiodegradationPercent: Optional[float] = None
    totalSludgeAdsorptionPercent: Optional[float] = None
    totalAirPercent: Optional[float] = None
    finalEffluentPercent: Optional[float] = None

@dataclass
class SewageModelComponents:
    processBreakdown: Optional[List[SewageModelComponent]] = None
    estimates: Optional[SewageEstimates] = None

@dataclass
class SewageTreatmentModelResponse:
    parameters: Optional[SewageTreatmentModelParameters] = None
    model: Optional[SewageModelComponents] = None
    output: Optional[str] = None

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
    smiles: Optional[str] = None
    cas: Optional[str] = None
    koc: Optional[NumericParameter] = None

# One environmental compartment of the Level III fugacity model. `name` is
# one of "air", "water", "soil", "sediment".
@dataclass
class FugacityModelComponent:
    name: Optional[str] = None
    massPercent: Optional[float] = None
    halfLifeHours: Optional[float] = None
    emissionsKgPerHour: Optional[float] = None

@dataclass
class FugacityEstimates:
    persistenceHours: Optional[float] = None
    selectedKoc: Optional[float] = None
    originalEqcKocComparison: Optional[float] = None
    airPercent: Optional[float] = None
    waterPercent: Optional[float] = None
    soilPercent: Optional[float] = None
    sedimentPercent: Optional[float] = None

@dataclass
class FugacityModelComponents:
    compartments: Optional[List[FugacityModelComponent]] = None
    estimates: Optional[FugacityEstimates] = None

# FugacityModelResponse dataclass
@dataclass
class FugacityModelResponse:
    parameters: Optional[FugacityModelParameters] = None
    model: Optional[FugacityModelComponents] = None
    output: Optional[str] = None

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
    cas: Optional[str] = None
    waterConcentrationMgPerCm3: Optional[NumericParameter] = None

# DermalPermeabilityResponse dataclass
@dataclass
class DermalPermeabilityResponse:
    parameters: Optional[DermalPermeabilityParameters] = None
    dermalPermeabilityCoefficient: Optional[float] = None
    dermalAbsorbedDose: Optional[float] = None
    dermalAbsorbedDosePerEvent: Optional[float] = None
    lagTimePerEventHours: Optional[float] = None
    timeToReachSteadyStateHours: Optional[float] = None
    # False when no exposure scenario was supplied, in which case only the
    # permeability coefficient is populated and the dose fields are absent.
    doseAvailable: Optional[bool] = None
    alerts: Optional[List[str]] = None
    output: Optional[str] = None

# ECOSAR (organics) --------------------------------------------------------
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
    flags: Optional[List[str]] = field(default_factory=list)

@dataclass
class ResultEcoSAR:
    parameters: Optional[EcosarParameters] = None
    modelResults: Optional[List[ModelResult]] = None
    alerts: Optional[List[str]] = None
    output: Optional[str] = None


# ECOSAR (typed surfactant / polymer / dye submodels) ----------------------
@dataclass
class TypedEcosarPrediction:
    organism: Optional[str] = None
    duration: Optional[str] = None
    endpoint: Optional[str] = None
    concentration: Optional[float] = None
    unit: Optional[str] = None
    flag: Optional[str] = None

@dataclass
class TypedEcosarEstimates:
    predictionCount: Optional[int] = None
    concentrationUnit: Optional[str] = None
    polymerCheck: Optional[str] = None

@dataclass
class TypedEcosarResult:
    """One of the typed ECOSAR submodels (surfactant, polymer or dye).

    These run only when the caller supplies the submodel's own inputs (chain
    length, ethoxylate count, and so on), so for an ordinary organic submission
    every typed submodel comes back as a `ModuleError` instead.
    """
    model: Optional[str] = None
    module: Optional[str] = None
    submodule: Optional[str] = None
    success: Optional[bool] = None
    predictionCount: Optional[int] = None
    parameters: Optional[Dict[str, Any]] = None
    resolvedInputs: Optional[Dict[str, Any]] = None
    estimates: Optional[TypedEcosarEstimates] = None
    flags: Optional[Dict[str, Any]] = None
    modelDetails: Optional[Dict[str, Any]] = None
    predictions: Optional[List[TypedEcosarPrediction]] = None
    notes: Optional[List[str]] = None
    alerts: Optional[List[str]] = None
    smiles: Optional[str] = None
    input: Optional[str] = None
    parameterSchema: Optional[Dict[str, Any]] = None
    trace: Optional[Dict[str, Any]] = None
    output: Optional[str] = None


# Fish biotransformation rate (new in v1.1.0) -----------------------------
@dataclass
class FishBiotransformationResponse:
    smiles: Optional[str] = None
    cas: Optional[str] = None
    molecularWeight: Optional[float] = None
    hasLogKow: Optional[bool] = None
    logKow: Optional[float] = None
    parameters: Optional[Dict[str, Any]] = None
    fragmentContribution: Optional[float] = None
    molecularWeightContribution: Optional[float] = None
    logKowContribution: Optional[float] = None
    logHalfLifeDays: Optional[float] = None
    halfLifeDays: Optional[float] = None
    uncappedRateConstant10g: Optional[float] = None
    rateConstant10g: Optional[float] = None
    rateConstant100g: Optional[float] = None
    rateConstant1kg: Optional[float] = None
    rateConstant10kg: Optional[float] = None
    rateCapMaximum: Optional[float] = None
    rateCapApplied: Optional[bool] = None
    ionic: Optional[bool] = None
    inorganic: Optional[bool] = None
    metalRemoved: Optional[bool] = None
    zwitterion: Optional[bool] = None
    sodiumCount: Optional[int] = None
    potassiumCount: Optional[int] = None
    lithiumCount: Optional[int] = None
    generalFragmentCount: Optional[int] = None
    hydrocarbonFragmentCount: Optional[int] = None
    reportMolecularWeight: Optional[str] = None
    fragments: Optional[List[Dict[str, Any]]] = None
    rateConstants: Optional[List[Dict[str, Any]]] = None
    calculationTerms: Optional[List[Dict[str, Any]]] = None
    notes: Optional[List[str]] = None
    alerts: Optional[List[str]] = None
    output: Optional[str] = None


# Analog identification (replaces the old top-level `analogs` lists) ------
@dataclass
class AnalogIdentificationResponse:
    smiles: Optional[str] = None
    cas: Optional[str] = None
    rearrangedSmiles: Optional[str] = None
    ringIndex: Optional[str] = None
    fragmentIds: Optional[str] = None
    fragmentCounts: Optional[str] = None
    molecularWeight: Optional[float] = None
    totalHalogens: Optional[int] = None
    recordFieldCount: Optional[int] = None
    zwitterion: Optional[bool] = None
    analogDataAvailable: Optional[bool] = None
    parameters: Optional[Dict[str, Any]] = None
    fragments: Optional[List[Dict[str, Any]]] = None
    genericFragments: Optional[List[str]] = None
    generic2Fragments: Optional[List[str]] = None
    generic3Fragments: Optional[List[str]] = None
    halogenGenericFragments: Optional[List[str]] = None
    metalFragmentIds: Optional[List[str]] = None
    metalGenericFragments: Optional[List[str]] = None
    analogs: Optional[List[str]] = None
    logKowAnalogs: Optional[List[str]] = None
    notes: Optional[List[str]] = None
    alerts: Optional[List[str]] = None
    output: Optional[str] = None


# Main Result Class
#
# Every module is typed as Union[ModuleError, <result>]: the API substitutes a
# {module, code, message} error object for any module that could not run, so
# callers should check `isinstance(result.logKow, ModuleError)` (or read the
# `errors` list) before reading a module's values.
@dataclass
class ResultEPISuite:
    parameters: Optional[Parameters] = None
    chemicalProperties: Optional[ChemicalProperties] = None
    logKow: Optional[Union[ModuleError, LogKowResponse]] = None
    meltingPoint: Optional[Union[ModuleError, MeltingPointResponse]] = None
    boilingPoint: Optional[Union[ModuleError, BoilingPointResponse]] = None
    vaporPressure: Optional[Union[ModuleError, VaporPressureResponse]] = None
    waterSolubilityFromLogKow: Optional[Union[ModuleError, WaterSolubilityFromLogKowResponse]] = None
    waterSolubilityFromWaterNt: Optional[Union[ModuleError, WaterSolubilityFromWaterNtResponse]] = None
    henrysLawConstant: Optional[Union[ModuleError, HenrysLawConstantResponse]] = None
    logKoa: Optional[Union[ModuleError, LogKoaResponse]] = None
    biodegradationRate: Optional[Union[ModuleError, BiodegradationRateResponse]] = None
    hydrocarbonBiodegradationRate: Optional[Union[ModuleError, HydrocarbonBiodegradationRateResponse]] = None
    aerosolAdsorptionFraction: Optional[Union[ModuleError, AerosolAdsorptionFractionResponse]] = None
    atmosphericHalfLife: Optional[Union[ModuleError, AtmosphericHalfLifeResponse]] = None
    logKoc: Optional[Union[ModuleError, LogKocResponse]] = None
    hydrolysis: Optional[Union[ModuleError, HydrolysisResponse]] = None
    bioconcentration: Optional[Union[ModuleError, BioconcentrationResponse]] = None
    waterVolatilization: Optional[Union[ModuleError, WaterVolatilizationResponse]] = None
    sewageTreatmentModel: Optional[Union[ModuleError, SewageTreatmentModelResponse]] = None
    fugacityModel: Optional[Union[ModuleError, FugacityModelResponse]] = None
    dermalPermeability: Optional[Union[ModuleError, DermalPermeabilityResponse]] = None
    fishBiotransformationRate: Optional[Union[ModuleError, FishBiotransformationResponse]] = None
    analogIdentification: Optional[Union[ModuleError, AnalogIdentificationResponse]] = None
    ecosar: Optional[Union[ModuleError, ResultEcoSAR]] = None
    # The API returns these under dotted keys ("ecosar.nonionic-surfactant").
    # `normalize_response_keys` in utils.py rewrites them to these identifiers
    # before parsing.
    ecosar_nonionic_surfactant: Optional[Union[ModuleError, TypedEcosarResult]] = None
    ecosar_anionic_surfactant: Optional[Union[ModuleError, TypedEcosarResult]] = None
    ecosar_cationic_surfactant: Optional[Union[ModuleError, TypedEcosarResult]] = None
    ecosar_amphoteric_surfactant: Optional[Union[ModuleError, TypedEcosarResult]] = None
    ecosar_dye: Optional[Union[ModuleError, TypedEcosarResult]] = None
    ecosar_nonionic_polymer: Optional[Union[ModuleError, TypedEcosarResult]] = None
    ecosar_anionic_polymer: Optional[Union[ModuleError, TypedEcosarResult]] = None
    ecosar_amphoteric_polymer: Optional[Union[ModuleError, TypedEcosarResult]] = None
    ecosar_polycationic_polymer: Optional[Union[ModuleError, TypedEcosarResult]] = None
    errors: Optional[List[ModuleError]] = None
