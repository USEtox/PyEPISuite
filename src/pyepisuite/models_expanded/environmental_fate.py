# pyepisuite/models/environmental_fate.py
from dataclasses import dataclass
from typing import List, Optional, Any
from .base import BaseValue

@dataclass
class FugacityModelParameters:
    henrysLawConstant: BaseValue
    logKow: BaseValue
    logKoc: BaseValue
    molecularWeight: BaseValue
    meltingPoint: BaseValue
    vaporPressure: BaseValue
    waterSolubility: BaseValue
    atmosphericHydroxylRateConstant: BaseValue
    ultimateBiodegradation: BaseValue
    halfLifeAir: BaseValue
    halfLifeWater: BaseValue
    halfLifeSoil: BaseValue
    halfLifeSediment: BaseValue
    emissionRateAir: BaseValue
    emissionRateWater: BaseValue
    emissionRateSoil: BaseValue
    emissionRateSediment: BaseValue
    advectionTimeAir: BaseValue
    advectionTimeWater: BaseValue
    advectionTimeSoil: BaseValue
    advectionTimeSediment: BaseValue

@dataclass
class FugacityModelCompartment:
    MassAmount: float
    HalfLife: float
    Emissions: float

@dataclass
class FugacityModel:
    Air: List[Optional[FugacityModelCompartment]]
    Water: List[Optional[FugacityModelCompartment]]
    Soil: List[Optional[FugacityModelCompartment]]
    Sediment: List[Optional[FugacityModelCompartment]]
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
    aNotes: List[Any]