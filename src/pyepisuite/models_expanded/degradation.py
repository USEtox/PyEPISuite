# pyepisuite/models/degradation.py
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class BiodegradationModel:
    name: str
    value: float
    factors: List[Dict[str, Any]]

@dataclass
class HydrolysisHalfLife:
    ph: float
    value: float
    unit: Optional[str]
    baseCatalyzed: bool
    acidCatalyzed: bool
    phosphorusEster: bool
    isomer: Optional[str]

@dataclass
class HydrolysisFragment:
    type: str
    visual: str
    groups: List[Any]

@dataclass
class HydrolysisResponse:
    halfLives: List[HydrolysisHalfLife]
    phosphorusEsterHalfLives: List[Any]
    fragments: List[HydrolysisFragment]
    baseCatalyzedRateConstant: float
    acidCatalyzedRateConstant: float
    acidCatalyzedRateConstantForTransIsomer: float
    neutralRateConstant: float
    output: str