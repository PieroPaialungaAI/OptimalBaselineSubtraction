import numpy as np 
import pandas as pd 
from constants import * 
from utils import * 
import warnings

class TimeSeriesData():
    def __init__(self, data_folder = DEFAULT_DATA_PATH):
        warnings.simplefilter("ignore")  # Ignore all warnings
        self.city_attribute_data = pd.read_csv(data_folder+'/city_attributes.csv')
        self.temperature_data = pd.read_csv(data_folder +'/temperature.csv')
        self.preprocess_temperature_data()
        self.build_temperature_dict_data()



    def select_city(self, city):

        self.selected_city_data = self.temperature_data[['datetime',city]].copy()
        self.selected_city_data = self.selected_city_data.reset_index().drop('index',axis=1)
        self.selected_city_data  = standardize_data(self.selected_city_data,city)
        return self.selected_city_data

    
    def preprocess_temperature_data(self):
        self.temperature_data = self.temperature_data.dropna().reset_index().drop('index',axis=1)
        self.temperature_data['datetime'] = pd.to_datetime(self.temperature_data['datetime'])

    
    def build_temperature_dict_data(self):
        city_list = set(self.temperature_data.columns.tolist())
        city_list.remove('datetime')
        self.temperature_dict_data = {}
        for city in city_list:
            self.select_city(city)
            self.temperature_dict_data[city] = self.selected_city_data





