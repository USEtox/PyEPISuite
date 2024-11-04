# pyepisuite/models/__init__.py
from .base import *
from .physical_properties import *
from .partition_coefficients import *
from .degradation import *
from .transport import *
from .responses import *
from .environmental_fate import *

# Main response class that combines everything
@dataclass
class SubmitResponse:
    parameters: Parameters
    chemicalProperties: ChemicalProperties
    logKow: LogKowResponse
    meltingPoint: MeltingPointResponse
    boilingPoint: BoilingPointResponse
    vaporPressure: VaporPressureResponse
    waterSolubilityFromLogKow: WaterSolubilityResponse
    waterSolubilityFromWaterNt: WaterSolubilityResponse
    henrysLawConstant: HenrysLawConstantResponse
    logKoa: LogKoaResponse
    biodegradationRate: BiodegradationResponse
    hydrocarbonBiodegradationRate: HydrocarbonBiodegradationResponse
    aerosolAdsorptionFraction: AerosolAdsorptionResponse
    atmosphericHalfLife: AtmosphericHalfLifeResponse
    logKoc: LogKocResponse
    hydrolysis: HydrolysisResponse
    bioconcentration: BioconcentrationResponse
    waterVolatilization: WaterVolatilizationResponse
    sewageTreatmentModel: SewageTreatmentModelResponse
    fugacityModel: FugacityModelResponse
    dermalPermeability: DermalPermeabilityResponse