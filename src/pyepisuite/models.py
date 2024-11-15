# models.py
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

# Base Classes
@dataclass
class Identifiers:
    name: str
    smiles: str
    cas: str

@dataclass
class Parameter:
    value: float
    units: Optional[str]
    valueType: str

@dataclass
class Coefficient:
    type: str
    value: float
    unit: Optional[str]

@dataclass
class Parameters:
    cas: str
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
    name: str
    systematicName: str
    cas: str
    smiles: Optional[str]
    molecularWeight: float
    molecularFormula: str
    molecularFormulaHtml: str
    organic: bool
    organicAcid: bool
    aminoAcid: bool
    nonStandardMetal: bool
    flags: Optional[Dict[str, bool]]

# Common Response Classes
@dataclass
class Flag:
    isOrganicAcid: bool
    isAminoAcid: bool

@dataclass
class KowFactor:
    type: str
    description: str
    fragmentCount: int
    coefficient: float
    contribution: Optional[float] = None
    trainingCount: Optional[int] = None
    validationCount: Optional[int] = None

@dataclass
class KowModel:
    logKow: Optional[float] = None
    factors: List[KowFactor] = None
    output: Optional[str] = None
    notes: Optional[str] = None
    flags: Optional[Flag] = None

@dataclass
class logKowEstimatedValue:
    model: KowModel
    value: float
    units: Optional[str]
    valueType: str

@dataclass
class ExperimentalValue:
    author: Optional[str]
    year: int
    order: int
    value: float
    units: Optional[str]
    valueType: str

@dataclass
class SelectedValue:
    value: Optional[float]
    units: Optional[str]
    valueType: str

# Specific Response Classes
@dataclass
class LogKowResponse:
    estimatedValue: logKowEstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

# MeltingPointFactor dataclass
@dataclass
class MeltingPointFactor:
    type: str
    description: str
    fragmentCount: int
    coefficient: float
    totalCoefficient: float

# MeltingPointModel dataclass
@dataclass
class MeltingPointModel:
    factors: List[MeltingPointFactor]
    meltingPointKelvins: float
    meltingPointLimitKelvins: float
    meltingPointCelsius: float
    meltingPointAdaptedJoback: float
    meltingPointGoldOgle: float
    meltingPointMean: float
    meltingPointSelected: float

# MeltingPointEstimatedValue dataclass
@dataclass
class MeltingPointEstimatedValue:
    model: MeltingPointModel
    value: float
    units: str
    valueType: str

# MeltingPointResponse dataclass
@dataclass
class MeltingPointResponse:
    estimatedValue: MeltingPointEstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

# BoilingPointFactor dataclass
@dataclass
class BoilingPointFactor:
    type: str
    description: str
    fragmentCount: int
    coefficient: float
    totalCoefficient: float

# BoilingPointModel dataclass
@dataclass
class BoilingPointModel:
    factors: List[BoilingPointFactor]
    boilingPointKelvinsUncorrected: float
    boilingPointKelvinsCorrected: float
    boilingPointCelsius: float

# BoilingPointEstimatedValue dataclass
@dataclass
class BoilingPointEstimatedValue:
    model: BoilingPointModel
    value: float
    units: str
    valueType: str

# BoilingPointResponse dataclass
@dataclass
class BoilingPointResponse:
    estimatedValue: BoilingPointEstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

# VaporPressureModelItem dataclass
@dataclass
class VaporPressureModelItem:
    type: str
    mmHg: float
    pa: float

# VaporPressureEstimatedValue dataclass
@dataclass
class VaporPressureEstimatedValue:
    model: List[VaporPressureModelItem]
    value: float
    units: str
    valueType: str

# VaporPressureResponse dataclass
@dataclass
class VaporPressureResponse:
    estimatedValue: VaporPressureEstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

@dataclass
class WaterSolubilityFromLogKowFactor:
    type: str
    description: Optional[str]
    fragmentCount: int
    coefficient: float
    totalCoefficient: float
    trainingCount: Optional[int] = None
    maxFragmentCount: Optional[int] = None

# WaterSolubilityModel dataclass
@dataclass
class WaterSolubilityModel:
    waterSolubility: float
    factors: List[WaterSolubilityFromLogKowFactor]
    equation: str
    notes: str
    output: str

# WaterSolubilityEstimatedValue dataclass
@dataclass
class WaterSolubilityEstimatedValue:
    model: WaterSolubilityModel
    value: float
    units: str
    valueType: str

# WaterSolubilityFromLogKowParameters dataclass
@dataclass
class WaterSolubilityFromLogKowParameters:
    smiles: str
    cas: str
    logKow: Parameter
    meltingPoint: Parameter

# WaterSolubilityFromLogKowResponse dataclass
@dataclass
class WaterSolubilityFromLogKowResponse:
    parameters: WaterSolubilityFromLogKowParameters
    estimatedValue: WaterSolubilityEstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

# WaterSolubilityFromWaterNtFactor dataclass
@dataclass
class WaterSolubilityFromWaterNtFactor:
    type: str
    description: Optional[str]
    fragmentCount: int
    coefficient: float
    totalCoefficient: float
    trainingCount: int
    maxFragmentCount: int

# WaterSolubilityFromWaterNtModel dataclass
@dataclass
class WaterSolubilityFromWaterNtModel:
    waterSolubility: float
    factors: List[WaterSolubilityFromWaterNtFactor]
    equation: str
    notes: str
    output: str

# WaterSolubilityFromWaterNtEstimatedValue dataclass
@dataclass
class WaterSolubilityFromWaterNtEstimatedValue:
    model: WaterSolubilityFromWaterNtModel
    value: float
    units: str
    valueType: str

# WaterSolubilityFromWaterNtParameters dataclass
@dataclass
class WaterSolubilityFromWaterNtParameters:
    smiles: str
    cas: str

# WaterSolubilityFromWaterNtResponse dataclass
@dataclass
class WaterSolubilityFromWaterNtResponse:
    parameters: WaterSolubilityFromWaterNtParameters
    estimatedValue: WaterSolubilityFromWaterNtEstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

# HenrysLawConstantFactor dataclass
@dataclass
class HenrysLawConstantFactor:
    type: str
    description: Optional[str]
    fragmentCount: int
    totalCoefficient: float
    trainingCount: int
    maxFragmentCount: int

# HenrysLawConstantModelItem dataclass
@dataclass
class HenrysLawConstantModelItem:
    name: str
    value: float
    factors: Optional[List[HenrysLawConstantFactor]]
    hlcAtm: float
    hlcUnitless: float
    hlcPaMol: float
    notes: str

# HenrysLawConstantEstimatedValue dataclass
@dataclass
class HenrysLawConstantEstimatedValue:
    model: List[HenrysLawConstantModelItem]
    value: float
    units: str
    valueType: str

# HenrysLawConstantParameters dataclass
@dataclass
class HenrysLawConstantParameters:
    smiles: str
    cas: str
    waterSolubility: Parameter
    vaporPressure: Parameter
    molecularWeight: Parameter

# HenrysLawConstantResponse dataclass
@dataclass
class HenrysLawConstantResponse:
    parameters: HenrysLawConstantParameters
    estimatedValue: HenrysLawConstantEstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

# LogKoaModel dataclass
@dataclass
class LogKoaModel:
    kow: float
    kaw: float
    koa: float
    logKoa: float

# LogKoaEstimatedValue dataclass
@dataclass
class LogKoaEstimatedValue:
    model: LogKoaModel
    value: float
    units: str
    valueType: str

# LogKoaParameters dataclass
@dataclass
class LogKoaParameters:
    smiles: str
    cas: str
    logKow: Parameter
    henrysLawConstant: Parameter

# LogKoaResponse dataclass
@dataclass
class LogKoaResponse:
    parameters: LogKoaParameters
    estimatedValue: LogKoaEstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

# BiodegradationRateFactor dataclass
@dataclass
class BiodegradationRateFactor:
    type: str
    description: str
    fragmentCount: int
    coefficient: float
    totalCoefficient: float
    trainingCount: int
    maxFragmentCount: int

# BiodegradationRateModel dataclass
@dataclass
class BiodegradationRateModel:
    name: str
    value: float
    factors: List[BiodegradationRateFactor]

# BiodegradationRateParameters dataclass
@dataclass
class BiodegradationRateParameters:
    smiles: str
    cas: str
    removeMetals: bool

# BiodegradationRateResponse dataclass
@dataclass
class BiodegradationRateResponse:
    parameters: BiodegradationRateParameters
    models: List[BiodegradationRateModel]
    notes: str
    output: str

# HydrocarbonBiodegradationRateModelFactor dataclass
@dataclass
class HydrocarbonBiodegradationRateModelFactor:
    type: str
    description: Optional[str]
    fragmentCount: int
    coefficient: float
    totalCoefficient: float
    trainingCount: int
    maxFragmentCount: int

# HydrocarbonBiodegradationRateModel dataclass
@dataclass
class HydrocarbonBiodegradationRateModel:
    halfLifeDays: Optional[float]
    logHalfLifeDays: Optional[float]
    factors: List[HydrocarbonBiodegradationRateModelFactor]
    notes: str
    output: str

# HydrocarbonBiodegradationRateEstimatedValue dataclass
@dataclass
class HydrocarbonBiodegradationRateEstimatedValue:
    model: HydrocarbonBiodegradationRateModel
    value: Optional[float]
    units: str
    valueType: str

# HydrocarbonBiodegradationRateParameters dataclass
@dataclass
class HydrocarbonBiodegradationRateParameters:
    smiles: str
    cas: str

# HydrocarbonBiodegradationRateResponse dataclass
@dataclass
class HydrocarbonBiodegradationRateResponse:
    parameters: HydrocarbonBiodegradationRateParameters
    estimatedValue: HydrocarbonBiodegradationRateEstimatedValue
    selectedValue: SelectedValue

# AerosolAdsorptionFractionModel dataclass
@dataclass
class AerosolAdsorptionFractionModel:
    mackayParticleGasPartitionCoefficient: float
    koaParticleGasPartitionCoefficient: float
    mackayAdsorptionFraction: float
    koaAdsorptionFraction: float
    jungePankowAdsorptionFraction: float

# AerosolAdsorptionFractionEstimatedValue dataclass
@dataclass
class AerosolAdsorptionFractionEstimatedValue:
    model: AerosolAdsorptionFractionModel
    value: float
    units: str
    valueType: str

# AerosolAdsorptionFractionParameters dataclass
@dataclass
class AerosolAdsorptionFractionParameters:
    logKoa: Parameter
    subcooledVaporPressure: Parameter

# AerosolAdsorptionFractionResponse dataclass
@dataclass
class AerosolAdsorptionFractionResponse:
    parameters: AerosolAdsorptionFractionParameters
    estimatedValue: AerosolAdsorptionFractionEstimatedValue
    selectedValue: SelectedValue

# ReactionFactor dataclass
@dataclass
class ReactionFactor:
    type: str
    value: float
    unit: str

# ReactionModel dataclass
@dataclass
class ReactionModel:
    type: str
    rateConstant: float
    halfLifeHours: float
    factors: Optional[List[ReactionFactor]] = None

# EstimatedValueModel dataclass
@dataclass
class EstimatedValueModel:
    models: List[ReactionModel]
    notes: str
    output: str

# EstimatedValue dataclass
@dataclass
class EstimatedValue:
    model: EstimatedValueModel
    value: Optional[float]
    units: str
    valueType: str

# EstimatedHydroxylRadicalReactionRateConstantModel dataclass
@dataclass
class EstimatedHydroxylRadicalReactionRateConstantModel:
    type: str
    rateConstant: float
    halfLifeHours: float
    factors: Optional[List[ReactionFactor]] = None

# EstimatedHydroxylRadicalReactionRateConstant dataclass
@dataclass
class EstimatedHydroxylRadicalReactionRateConstant:
    model: EstimatedHydroxylRadicalReactionRateConstantModel
    value: float
    units: str
    valueType: str

# EstimatedOzoneReactionRateConstantModel dataclass
@dataclass
class EstimatedOzoneReactionRateConstantModel:
    type: str
    rateConstant: float
    halfLifeHours: float
    factors: Optional[List[ReactionFactor]] = None

# EstimatedOzoneReactionRateConstant dataclass
@dataclass
class EstimatedOzoneReactionRateConstant:
    model: EstimatedOzoneReactionRateConstantModel
    value: float
    units: str
    valueType: str

# ExperimentalReactionRateConstant dataclass
@dataclass
class ExperimentalReactionRateConstant:
    author: Optional[str]
    year: int
    order: int
    value: float
    units: str
    valueType: str

# AtmosphericHalfLifeParameters dataclass
@dataclass
class AtmosphericHalfLifeParameters:
    smiles: str
    cas: str
    hydroxylRadicalConcentration: float
    ozoneConcentration: float
    twelveHourDay: bool

# AtmosphericHalfLifeResponse dataclass
@dataclass
class AtmosphericHalfLifeResponse:
    parameters: AtmosphericHalfLifeParameters
    estimatedValue: EstimatedValue
    estimatedHydroxylRadicalReactionRateConstant: EstimatedHydroxylRadicalReactionRateConstant
    estimatedOzoneReactionRateConstant: EstimatedOzoneReactionRateConstant
    experimentalHydroxylRadicalReactionRateConstantValues: List[ExperimentalReactionRateConstant]
    experimentalOzoneReactionRateConstantValues: List[ExperimentalReactionRateConstant]
    experimentalNitrateReactionRateConstantValues: List[ExperimentalReactionRateConstant]
    selectedHydroxylRadicalReactionRateConstant: SelectedValue
    selectedOzoneReactionRateConstantValues: SelectedValue

# LogKocFactor dataclass
@dataclass
class LogKocFactor:
    fragmentCount: int
    trainingCount: int
    maxFragmentCount: int
    description: str
    coefficient: float
    totalCoefficient: float

# LogKocModelItem dataclass
@dataclass
class LogKocModelItem:
    firstOrderMCI: Optional[float]
    name: str
    factors: List[LogKocFactor]
    nonCorrectedLogKoc: float
    correctedLogKoc: float
    koc: float
    logKow: Optional[float] = None

# LogKocModel dataclass
@dataclass
class LogKocModel:
    logKoc: float
    models: List[LogKocModelItem]
    notes: str
    output: str

# LogKocEstimatedValue dataclass
@dataclass
class LogKocEstimatedValue:
    model: LogKocModel
    value: Optional[float]
    units: str
    valueType: str

# LogKocParameters dataclass
@dataclass
class LogKocParameters:
    smiles: str
    cas: str
    logKow: Parameter

# LogKocResponse dataclass
@dataclass
class LogKocResponse:
    parameters: LogKocParameters
    experimentalValues: List[ExperimentalValue]
    estimatedValue: LogKocEstimatedValue
    selectedValue: SelectedValue

# HydrolysisHalfLife dataclass
@dataclass
class HydrolysisHalfLife:
    ph: float
    value: float
    unit: Optional[str]
    baseCatalyzed: bool
    acidCatalyzed: bool
    phosphorusEster: bool
    isomer: Optional[str]

# HydrolysisFragment dataclass
@dataclass
class HydrolysisFragment:
    # Define fields if available
    pass

# HydrolysisResponse dataclass
@dataclass
class HydrolysisResponse:
    halfLives: List[HydrolysisHalfLife]
    phosphorusEsterHalfLives: List[HydrolysisHalfLife]
    fragments: List[HydrolysisFragment]
    baseCatalyzedRateConstant: float
    acidCatalyzedRateConstant: float
    acidCatalyzedRateConstantForTransIsomer: float
    neutralRateConstant: float
    output: str

# BioconcentrationParameters dataclass
@dataclass
class BioconcentrationParameters:
    smiles: str
    cas: str
    logKow: Parameter

# BiotransformationFactor dataclass
@dataclass
class BiotransformationFactor:
    type: str
    description: str
    fragmentCount: int
    coefficient: float
    totalCoefficient: float
    trainingCount: int
    maxFragmentCount: int

# BiotransformationRateConstant dataclass
@dataclass
class BiotransformationRateConstant:
    type: str
    value: float
    unit: str

# BioconcentrationFactor dataclass
@dataclass
class BioconcentrationFactor:
    type: str
    description: str
    fragmentCount: int
    coefficient: float
    totalCoefficient: float
    trainingCount: int
    maxFragmentCount: int

# ArnotGobasBcfBafEstimate dataclass
@dataclass
class ArnotGobasBcfBafEstimate:
    trophicLevel: str
    trophicLevelNote: Optional[str]
    bioconcentrationFactor: float
    logBioconcentrationFactor: float
    bioaccumulationFactor: float
    logBioaccumulationFactor: float
    unit: str

# BioconcentrationResponse dataclass
@dataclass
class BioconcentrationResponse:
    parameters: BioconcentrationParameters
    bioconcentrationFactor: float
    experimentalBioconcentrationFactor: Optional[float]
    experimentalBioTransformationRate: float
    logBioconcentrationFactor: float
    biotransformationHalfLife: float
    bioaccumulationFactor: float
    logBioaccumulationFactor: float
    biotransformationFactors: List[BiotransformationFactor]
    biotransformationRateConstants: List[BiotransformationRateConstant]
    bioconcentrationFactors: List[BioconcentrationFactor]
    biocontrationFactorEquation: str
    biocontrationFactorEquationSum: float
    arnotGobasBcfBafEstimates: List[ArnotGobasBcfBafEstimate]
    notes: str
    output: str

@dataclass
class WaterVolatilizationParameters:
    molecularWeight: float
    henrysLawConstant: Parameter  # Reusing the existing Parameter dataclass
    riverWaterDepthMeters: float
    riverWindVelocityMetersPerSecond: float
    riverCurrentVelocityMetersPerSecond: float
    lakeWindVelocityMetersPerSecond: float
    lakeCurrentVelocityMetersPerSecond: float
    lakeWaterDepthMeters: float

@dataclass
class WaterVolatilizationResponse:
    parameters: WaterVolatilizationParameters
    riverHalfLifeHours: float
    lakeHalfLifeHours: float

# SewageTreatmentModelParameters dataclass
@dataclass
class SewageTreatmentModelParameters:
    molecularWeight: Parameter
    henrysLawConstant: Parameter
    waterSolubility: Parameter
    vaporPressure: Parameter
    logKow: Parameter
    biowin3: Parameter
    biowin5: Parameter
    halfLifeHoursPrimaryClarifier: Parameter
    halfLifeHoursAerationVessel: Parameter
    halfLifeHoursSettlingTank: Parameter

# Base ModelComponent dataclass
@dataclass
class SewageModelComponent:
    MassPerHour: float
    MolPerHour: float
    Percent: float

@dataclass
class SewageModelComponents:
    Influent: SewageModelComponent
    PrimarySludge: SewageModelComponent
    WasteSludge: SewageModelComponent
    TotalSludge: SewageModelComponent
    PrimVloitilization: SewageModelComponent
    SettlingVloitilization: SewageModelComponent
    AerationOffGas: SewageModelComponent
    TotalAir: SewageModelComponent
    PrimBiodeg: SewageModelComponent
    SettlingBiodeg: SewageModelComponent
    AerationBiodeg: SewageModelComponent
    TotalBiodeg: SewageModelComponent
    FinalEffluent: SewageModelComponent
    TotalRemoval: SewageModelComponent
    PrimaryRateConstant: SewageModelComponent
    AerationRateConstant: SewageModelComponent
    SettlingRateConstant: SewageModelComponent
    CalculationVariables: List[float]

@dataclass
class SewageTreatmentModelResponse:
    parameters: SewageTreatmentModelParameters
    model: SewageModelComponents

@dataclass
class FugacityModelParameters:
    henrysLawConstant: Parameter
    logKow: Parameter
    logKoc: Parameter
    molecularWeight: Parameter
    meltingPoint: Parameter
    vaporPressure: Parameter
    waterSolubility: Parameter
    atmosphericHydroxylRateConstant: Parameter
    ultimateBiodegradation: Parameter
    halfLifeAir: Parameter
    halfLifeWater: Parameter
    halfLifeSoil: Parameter
    halfLifeSediment: Parameter
    emissionRateAir: Parameter
    emissionRateWater: Parameter
    emissionRateSoil: Parameter
    emissionRateSediment: Parameter
    advectionTimeAir: Parameter
    advectionTimeWater: Parameter
    advectionTimeSoil: Parameter
    advectionTimeSediment: Parameter

# ModelComponent dataclass
@dataclass
class FugacityModelComponent:
    MassAmount: float
    HalfLife: float
    Emissions: float

# ModelComponents dataclass containing all model components
@dataclass
class FugacityModelComponents:
    Air: List[Optional[FugacityModelComponent]]
    Water: List[Optional[FugacityModelComponent]]
    Soil: List[Optional[FugacityModelComponent]]
    Sediment: List[Optional[FugacityModelComponent]]
    Persistence: float
    aEmissionArray: List[float]
    aAdvectionTimeArray: List[float]
    aFugacities: List[float]
    aReaction: List[float]
    aAdvection: List[float]
    aReactionPercent: List[float]
    aAdvectionPercent: List[float]
    aSums: List[float]
    aTimes: List[float]
    HalfLifeArray: List[float]
    HalfLifeFactorArray: List[float]
    Emission: List[float]
    AdvectionTimesArray: List[float]
    aNotes: List[str]

# FugacityModelResponse dataclass
@dataclass
class FugacityModelResponse:
    parameters: FugacityModelParameters
    model: FugacityModelComponents

# DermalPermeabilityParameters dataclass
@dataclass
class DermalPermeabilityParameters:
    smiles: str
    logKow: Parameter
    molecularWeight: Parameter
    dermalPermeabilityCoefficient: Parameter
    waterConcentrationMgPerLiter: Parameter
    eventDurationHours: float
    fractionAbsorbedWater: float
    skinSurfaceAreaCm2: float
    exposureEventsPerDay: float
    exposureDurationYears: float
    exposureDaysPerYear: float
    bodyWeightKg: float
    averagingTimeDays: float

# DermalPermeabilityResponse dataclass
@dataclass
class DermalPermeabilityResponse:
    parameters: DermalPermeabilityParameters
    dermalPermeabilityCoefficient: float
    dermalAbsorbedDose: float
    dermalAbsorbedDosePerEvent: float
    lagTimePerEventHours: float
    timeToReachSteadyStateHours: float
    output: str

# Main Result Class
@dataclass
class ResultEPISuite:
    parameters: Parameters
    chemicalProperties: ChemicalProperties
    logKow: LogKowResponse
    meltingPoint: MeltingPointResponse
    boilingPoint: BoilingPointResponse
    vaporPressure: VaporPressureResponse
    waterSolubilityFromLogKow: WaterSolubilityFromLogKowResponse
    waterSolubilityFromWaterNt: WaterSolubilityFromWaterNtResponse
    henrysLawConstant: HenrysLawConstantResponse
    logKoa: LogKoaResponse
    biodegradationRate: BiodegradationRateResponse
    hydrocarbonBiodegradationRate: HydrocarbonBiodegradationRateResponse
    aerosolAdsorptionFraction: AerosolAdsorptionFractionResponse
    atmosphericHalfLife: AtmosphericHalfLifeResponse
    logKoc: LogKocResponse
    hydrolysis: HydrolysisResponse
    bioconcentration: BioconcentrationResponse
    waterVolatilization: WaterVolatilizationResponse
    sewageTreatmentModel: SewageTreatmentModelResponse
    fugacityModel: FugacityModelResponse
    dermalPermeability: DermalPermeabilityResponse
    analogs: Optional[List[str]] = None
    logKowAnalogs: Optional[List[str]] = None # possibly a bug in the web app

@dataclass
class EcosarParameters:
    smiles: str
    cas: str
    logKow: Parameter
    waterSolubility: Parameter
    meltingPoint: Parameter

@dataclass
class ModelResult:
    qsarClass: str
    organism: str
    duration: str
    endpoint: str
    concentration: float
    maxLogKow: float
    flags: List[str] = field(default_factory=list)  # Assuming flags are strings

@dataclass
class ResultEcoSAR:
    parameters: EcosarParameters
    modelResults: List[ModelResult]
    output: str
    alerts: Optional[List[str]] = None