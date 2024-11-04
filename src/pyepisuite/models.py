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
    removeMetals: Optional[bool]
    waterSolubility: Optional[Parameter]
    vaporPressure: Optional[Parameter]
    molecularWeight: Optional[Parameter]
    henrysLawConstant: Optional[Parameter]
    logKow: Optional[Parameter]
    subcooledVaporPressure: Optional[Parameter]
    hydroxylRadicalConcentration: Optional[float]
    ozoneConcentration: Optional[float]
    twelveHourDay: Optional[bool]
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
class Factor:
    type: str
    description: str
    fragmentCount: int
    coefficient: float
    totalCoefficient: Optional[float] = None
    contribution: Optional[float] = None
    trainingCount: Optional[int] = None
    validationCount: Optional[int] = None
    totalCoefficient: Optional[float] = None
    maxFragmentCount: Optional[int] = None

@dataclass
class Model:
    logKow: Optional[float] = None
    factors: List[Factor] = None
    output: Optional[str] = None
    notes: Optional[str] = None
    flags: Optional[Flag] = None

@dataclass
class EstimatedValue:
    model: Model
    value: float
    units: Optional[str]
    valueType: str

@dataclass
class ExperimentalValue:
    author: str
    year: int
    order: int
    value: float
    units: Optional[str]
    valueType: str

@dataclass
class SelectedValue:
    value: float
    units: Optional[str]
    valueType: str

# Specific Response Classes
@dataclass
class LogKowResponse:
    estimatedValue: EstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

@dataclass
class MeltingPointResponse:
    estimatedValue: EstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

@dataclass
class BoilingPointResponse:
    estimatedValue: EstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

@dataclass
class VaporPressureResponse:
    estimatedValue: EstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

@dataclass
class WaterSolubilityFromLogKowResponse:
    estimatedValue: EstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

@dataclass
class WaterSolubilityFromWaterNtResponse:
    estimatedValue: EstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

@dataclass
class HenrysLawConstantResponse:
    estimatedValue: EstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

@dataclass
class LogKoaResponse:
    estimatedValue: EstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

@dataclass
class BiodegradationRateResponse:
    estimatedValue: EstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

@dataclass
class HydrocarbonBiodegradationRateResponse:
    estimatedValue: EstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

@dataclass
class AerosolAdsorptionFractionResponse:
    estimatedValue: EstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

@dataclass
class AtmosphericHalfLifeResponse:
    estimatedValue: EstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

@dataclass
class LogKocResponse:
    estimatedValue: EstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

@dataclass
class HydrolysisResponse:
    estimatedValue: EstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

@dataclass
class ArnotGobatBcfBaf:
    """
    "trophicLevel": "Upper Trophic",
    "trophicLevelNote": null,
    "bioconcentrationFactor": 1.0564629108622166,
    "logBioconcentrationFactor": 0.023854254923004505,
    "bioaccumulationFactor": 1.0564629136752755,
    "logBioaccumulationFactor": 0.023854256079406628,
    "unit": "L/kg wet-wt"
    """
    trophicLevel: str
    trophicLevelNote: Optional[str]
    bioconcentrationFactor: float
    logBioconcentrationFactor: float
    bioaccumulationFactor: float
    logBioaccumulationFactor: float
    unit: str

@dataclass
class BioconcentrationResponse:
    bioconcentrationFactor: float
    experimentalBioconcentrationFactor: Optional[float]
    experimentalBioTransformationRate: float
    logBioconcentrationFactor: float
    biotransformationHalfLife: float
    bioaccumulationFactor: float
    logBioaccumulationFactor: float
    biotransformationFactors: List[Factor]
    biotransformationRateConstants: List[Coefficient]
    bioconcentrationFactors: List[Factor]
    biocontrationFactorEquation: str
    biocontrationFactorEquationSum: float
    arnotGobasBcfBafEstimates: list[ArnotGobatBcfBaf]
    estimatedValue: EstimatedValue
    experimentalValues: List[ExperimentalValue]
    selectedValue: SelectedValue

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
    analogs: Optional[List[Dict[str, Any]]] = None
    logKowAnalogs: Optional[List[Parameter]] = None

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
    alerts: Optional[str] = None