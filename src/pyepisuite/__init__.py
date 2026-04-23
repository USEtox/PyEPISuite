"""
EPISuite API Package
"""

__version__ = "1.2.0"

__author__ = [
    "Ali A. Eftekhari",
]

__contact__ = "e.eftekhari@gmail.com"

__copyright__ = "Copyright 2024, The Authors"

__license__ = "MIT License"

from .utils import json_to_episuite, json_to_ecosar, search_episuite_by_cas, \
    search_episuite, submit_to_episuite, is_valid_cas
from .expdata import HenryData, BoilingPointData, MeltingPointData, \
    VaporPressureData, SolubilityData
from .usetox_input import USEtoxInput, create_usetox_input_from_cas_list
from .api_client import EpiSuiteAPIClient, LocalEpiSuiteAPIClient, stop_local_episuite_server
from .models import Identifiers, ResultEPISuite, ResultEcoSAR
from .dataframe_utils import (
    episuite_to_dataframe, 
    episuite_experimental_to_dataframe,
    ecosar_to_dataframe,
    combine_episuite_ecosar_dataframes,
    export_to_excel,
    create_summary_statistics
)
