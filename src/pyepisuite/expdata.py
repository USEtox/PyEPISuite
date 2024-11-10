import pandas as pd
import os


def data_folder():
    return os.path.join(os.path.dirname(__file__), '..', '..', 'data')

def henry_data_file():
    return os.path.join(data_folder(), 'henrywin', 'Henry_PhysProp_Data.csv')

def boiling_point_data_file():
    return os.path.join(data_folder(), 'mpbpvp', 'Boiling_Point_PhysChem.csv')

def melting_point_data_file():
    return os.path.join(data_folder(), 'mpbpvp', 'Melting_Point_PhysChem.csv')

def vapor_pressure_data_file():
    return os.path.join(data_folder(), 'mpbpvp', 'Vapor_Pressure_PhysChem.csv')

def solubility_data_file():
    return os.path.join(data_folder(), 'wskowwin', 'solubility_data_clean.csv')

class HenryData:
    def __init__(self) -> None:
        self.data = pd.read_csv(os.path.join(henry_data_file()))

    def HLC(self, cas: str) -> dict:
        """
        Returns the Henry's Law Constant for a given CAS number with th following dictionary format:
        {'CASRN': '64-17-5', 
        'name': 'Ethanol',
        'value': 0.0001, 
        'unit': 'atm-m3/mole',
        'Temp (C)': 25.0,
        'type': 'EXP' or 'EST'}
        """

        val = self.data[self.data['CAS Number'] == cas]['HenryLC (atm-m3/mole)'].values[0]
        name = self.data[self.data['CAS Number'] == cas]['Name'].values[0]
        T = self.data[self.data['CAS Number'] == cas]['HLC Temp'].values[0]
        unit = 'atm-m3/mole'
        type_hlc = self.data[self.data['CAS Number'] == cas]['HLC type'].values[0]
        return {'CASRN': cas, 'name': name, 'value': val, 'unit': unit, 'Temp (C)': T, 'type': type_hlc}
    
class BoilingPointData:
    def __init__(self) -> None:
        self.data = pd.read_csv(boiling_point_data_file())

    def boiling_point(self, cas: str) -> dict:
        """
        Returns the boiling point for a given CAS number with the following dictionary format:
        {'CASRN': '64-17-5',
        'name': 'Ethanol',
        'value': 78.37,
        'unit': 'C'
        """

        val = self.data[self.data['CAS'] == cas]['Boiling Pt (deg C)'].values[0]
        name = self.data[self.data['CAS'] == cas]['Name'].values[0]
        unit = 'C'
        return {'CASRN': cas, 'name': name, 'value': val, 'unit': unit}

class MeltingPointData:
    def __init__(self) -> None:
        self.data = pd.read_csv(melting_point_data_file())

    def melting_point(self, cas: str) -> float:
        """
        Returns the melting point for a given CAS number with the following dictionary format:
        {'CASRN': '64-17-5',
        'name': 'Ethanol',
        'value': -114.1,
        'unit': 'C'}
        """

        val = self.data[self.data['CAS'] == cas]['Melt Pt (deg C)'].values[0]
        name = self.data[self.data['CAS'] == cas]['Name'].values[0]
        unit = 'C'
        return {'CASRN': cas, 'name': name, 'value': val, 'unit': unit}

class VaporPressureData:
    def __init__(self) -> None:
        self.data = pd.read_csv(vapor_pressure_data_file())

    def vapor_pressure(self, cas: str) -> dict:
        """
        Returns the vapor pressure for a given CAS number with the following dictionary format:
        {'CASRN': '64-17-5',
        'name': 'Ethanol',
        'value': 59.3,
        'unit': 'mmHg',
        'Temp (C)': 20.0,
        'type': 'EXP' or 'EXT'}
        """

        val = self.data[self.data['CAS'] == cas]['VP (mm Hg)'].values[0]
        name = self.data[self.data['CAS'] == cas]['Name'].values[0]
        T = self.data[self.data['CAS'] == cas]['VP temp (degC)'].values[0]
        unit = 'mmHg'
        type_vp = self.data[self.data['CAS'] == cas]['VP type'].values[0]
        return {'CASRN': cas, 'name': name, 'value': val, 'unit': unit, 'Temp (C)': T, 'type': type_vp}

class SolubilityData:
    def __init__(self) -> None:
        self.data = pd.read_csv(solubility_data_file())

    def solubility(self, cas: str) -> dict:
        """
        Returns the solubility for a given CAS number with the following dictionary format:
        {'CASRN': '64-17-5',
        'name': 'Ethanol',
        'class': 'Alcohol',
        'logKow': -0.24,
        'water_solubility_mg_per_L': 50.0,
        'log_mol_per_L': -3.1,
        """

        name = self.data[self.data['CAS'] == cas]['NAME'].values[0]
        class_compound = self.data[self.data['CAS'] == cas]['class_name'].values[0]
        logKow = self.data[self.data['CAS'] == cas]['LOGP'].values[0]
        water_solubility_mg_per_L = self.data[self.data['CAS'] == cas]['WSOL'].values[0]
        log_mol_per_L = self.data[self.data['CAS'] == cas]['LOGMOLAR'].values[0]
        return {'CASRN': cas, 
                'name': name, 
                'class': class_compound, 
                'logKow': logKow, 
                'water_solubility_mg_per_L': water_solubility_mg_per_L, 
                'log_mol_per_L': log_mol_per_L}
