import pandas as pd
import os


def data_folder():
    return os.path.join(os.path.dirname(__file__), '..', '..', 'data')

def henry_data_file():
    return pd.read_csv(os.path.join(data_folder(), 'henrywin', 'Henry_PhysProp_Data.csv'))

class HenryData:
    def __init__(self) -> None:
        self.data = pd.read_csv(os.path.join(henry_data_file()))

    def HLC(self, cas: str) -> float:
        return self.data[self.data['CAS Number'] == cas]['HenryLC (atm-m3/mole)'].values[0]

