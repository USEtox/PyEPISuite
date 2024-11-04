# pyepisuite/models/physical_properties.py
from dataclasses import dataclass
from typing import List, Optional
from .base import BaseValue, BaseModel, BaseExperimentalValue, BaseResponse

# Melting Point
@dataclass
class MeltingPointFactor:
    type: str
    description: str
    fragmentCount: int
    coefficient: float
    totalCoefficient: float

@dataclass
class MeltingPointModel(BaseModel):
    factors: List[MeltingPointFactor]
    meltingPointKelvins: float
    meltingPointLimitKelvins: float
    meltingPointCelsius: float
    meltingPointAdaptedJoback: float
    meltingPointGoldOgle: float
    meltingPointMean: float
    meltingPointSelected: float

@dataclass
class MeltingPointResponse(BaseResponse):
    pass

# Boiling Point
@dataclass
class BoilingPointFactor:
    type: str
    description: str
    fragmentCount: int
    coefficient: float
    totalCoefficient: float

@dataclass
class BoilingPointModel(BaseModel):
    factors: List[BoilingPointFactor]
    boilingPointKelvinsUncorrected: float
    boilingPointKelvinsCorrected: float
    boilingPointCelsius: float

@dataclass
class BoilingPointResponse(BaseResponse):
    pass