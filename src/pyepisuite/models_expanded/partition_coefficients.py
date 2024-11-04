# pyepisuite/models/partition_coefficients.py
from dataclasses import dataclass
from typing import List, Dict, Any
from .base import BaseModel

@dataclass
class LogKowFragment:
    type: str
    description: str
    fragmentCount: int
    coefficient: float
    contribution: float
    trainingCount: int
    validationCount: int

@dataclass
class LogKowModel(BaseModel):
    logKow: float
    factors: List[LogKowFragment]
    flags: Dict[str, bool]

@dataclass
class LogKocFactor:
    fragmentCount: int
    trainingCount: int
    maxFragmentCount: int
    description: str
    coefficient: float
    totalCoefficient: float

@dataclass
class LogKocModel(BaseModel):
    logKoc: float
    models: List[Dict[str, Any]]  # Complex nested structure

@dataclass
class LogKoaModel(BaseModel):
    kow: float
    kaw: float
    koa: float
    logKoa: float