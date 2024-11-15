"""
EPISuite API Package
"""

__version__ = "0.1.0"

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
from .api_client import EpiSuiteAPIClient
from .models import Identifiers, ResultEPISuite, ResultEcoSAR
