# pyepisuite/models/transport.py
from dataclasses import dataclass
from .base import BaseValue

@dataclass
class WaterVolatilizationParameters:
    molecularWeight: float
    henrysLawConstant: BaseValue
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

@dataclass
class DermalPermeabilityParameters:
    smiles: str
    logKow: BaseValue
    molecularWeight: BaseValue
    dermalPermeabilityCoefficient: BaseValue
    waterConcentrationMgPerLiter: BaseValue
    eventDurationHours: float
    fractionAbsorbedWater: float
    skinSurfaceAreaCm2: float
    exposureEventsPerDay: int
    exposureDurationYears: int
    exposureDaysPerYear: int
    bodyWeightKg: float
    averagingTimeDays: int