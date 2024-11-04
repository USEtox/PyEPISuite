# pyepisuite/models/base.py
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class BaseValue:
    value: float
    units: Optional[str]
    valueType: str

@dataclass
class Parameter:
    value: float
    units: str
    valueType: str

@dataclass
class ChemicalProperties:
    name: str
    systematicName: str
    cas: str
    smiles: str
    molecularWeight: float
    molecularFormula: str
    molecularFormulaHtml: str
    organic: bool
    organicAcid: bool
    aminoAcid: bool
    nonStandardMetal: bool
    flags: Optional[Dict]

    def __str__(self):
        return f"Chemical(name: {self.name}, CAS: {self.cas})"

@dataclass
class Parameters:
    cas: str
    smiles: Optional[str]
    caseNumber: Optional[str]
    userLogKow: Parameter
    userMeltingPoint: Parameter
    userBoilingPoint: Parameter
    userWaterSolubility: Parameter
    userVaporPressure: Parameter
    userHenrysLawConstant: Parameter
    userLogKoa: Parameter
    userLogKoc: Parameter
    userHydroxylReactionRateConstant: Parameter
    userDermalPermeabilityCoefficient: Parameter
    userAtmosphericHydroxylRadicalConcentration: Parameter
    userAtmosphericOzoneConcentration: Parameter
    userAtmosphericDaylightHours: Parameter
    userStpHalfLifePrimaryClarifier: Parameter
    userStpHalfLifeAerationVessel: Parameter
    userStpHalfLifeSettlingTank: Parameter
    userFugacityHalfLifeAir: Parameter
    userFugacityHalfLifeWater: Parameter
    userFugacityHalfLifeSoil: Parameter
    userFugacityHalfLifeSediment: Parameter
    userFugacityEmissionRateAir: Parameter
    userFugacityEmissionRateWater: Parameter
    userFugacityEmissionRateSoil: Parameter
    userFugacityEmissionRateSediment: Parameter
    userFugacityAdvectionTimeAir: Parameter
    userFugacityAdvectionTimeWater: Parameter
    userFugacityAdvectionTimeSoil: Parameter
    userFugacityAdvectionTimeSediment: Parameter

    def __str__(self):
        return f"Parameters(cas: {self.cas})"