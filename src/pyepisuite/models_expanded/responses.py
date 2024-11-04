# pyepisuite/models/responses.py
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from .base import BaseValue, BaseResponse, BaseExperimentalValue

@dataclass
class VaporPressureModel:
    type: str
    mmHg: float
    pa: float

@dataclass
class VaporPressureResponse(BaseResponse):
    estimatedValue: Dict[str, List[VaporPressureModel]]
    experimentalValues: List[BaseExperimentalValue]
    selectedValue: BaseValue

@dataclass
class WaterSolubilityModel:
    waterSolubility: float
    factors: List[Dict[str, Any]]
    equation: str
    notes: str
    output: str

@dataclass
class WaterSolubilityResponse(BaseResponse):
    estimatedValue: Dict[str, WaterSolubilityModel]
    experimentalValues: List[BaseExperimentalValue]
    selectedValue: BaseValue

@dataclass
class HenrysLawConstantModel:
    name: str
    value: float
    factors: Optional[List[Dict[str, Any]]]
    hlcAtm: float
    hlcUnitless: float
    hlcPaMol: float
    notes: str

@dataclass
class HenrysLawConstantResponse(BaseResponse):
    estimatedValue: Dict[str, List[HenrysLawConstantModel]]
    experimentalValues: List[BaseExperimentalValue]
    selectedValue: BaseValue

@dataclass
class LogKoaResponse(BaseResponse):
    estimatedValue: Dict[str, Any]
    experimentalValues: List[BaseExperimentalValue]
    selectedValue: BaseValue

@dataclass
class BiodegradationModel:
    name: str
    value: float
    factors: List[Dict[str, Any]]

@dataclass
class BiodegradationResponse(BaseResponse):
    models: List[BiodegradationModel]
    notes: str
    output: str

@dataclass
class HydrocarbonBiodegradationResponse(BaseResponse):
    estimatedValue: Dict[str, Any]
    selectedValue: BaseValue

@dataclass
class AerosolAdsorptionModel:
    mackayParticleGasPartitionCoefficient: float
    koaParticleGasPartitionCoefficient: float
    mackayAdsorptionFraction: float
    koaAdsorptionFraction: float
    jungePankowAdsorptionFraction: float

@dataclass
class AerosolAdsorptionResponse(BaseResponse):
    estimatedValue: Dict[str, AerosolAdsorptionModel]
    selectedValue: BaseValue

@dataclass
class AtmosphericHalfLifeResponse(BaseResponse):
    estimatedValue: Dict[str, Any]
    estimatedHydroxylRadicalReactionRateConstant: Dict[str, Any]
    estimatedOzoneReactionRateConstant: Dict[str, Any]
    experimentalValues: List[BaseExperimentalValue]
    selectedValue: BaseValue

@dataclass
class BioconcentrationFactor:
    type: str
    description: str
    fragmentCount: int
    coefficient: float
    totalCoefficient: float
    trainingCount: int
    maxFragmentCount: int

@dataclass
class BioconcentrationResponse(BaseResponse):
    bioconcentrationFactor: float
    experimentalBioconcentrationFactor: Optional[float]
    logBioconcentrationFactor: float
    biotransformationHalfLife: float
    bioaccumulationFactor: float
    logBioaccumulationFactor: float
    biotransformationFactors: List[BioconcentrationFactor]
    notes: str
    output: str

@dataclass
class SewageTreatmentModelResponse(BaseResponse):
    model: Dict[str, Any]

@dataclass
class FugacityModelResponse(BaseResponse):
    model: Dict[str, Any]

@dataclass
class DermalPermeabilityResponse(BaseResponse):
    dermalPermeabilityCoefficient: float
    dermalAbsorbedDose: float
    dermalAbsorbedDosePerEvent: float
    lagTimePerEventHours: float
    timeToReachSteadyStateHours: float
    output: str