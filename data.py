import numpy as np 
import pandas as pd 
from constants import * 

class TimeSeriesData():
    def __init__(self, data_folder = DEFAULT_DATA_PATH):
        self.city_attribute_data = pd.read_csv(data_folder+'/city_attributes.csv')
        self.temperature_data = pd.read_csv(data_folder +'/temperature.csv')
        self.preprocess_temperature_data()


    def select_city(self, city):
        self.selected_city_data = self.temperature_data[[city,'datetime']]
        self.selected_city_data = self.selected_city_data.reset_index().drop('index',axis=1)
        self.selected_city_data['datetime'] = pd.to_datetime(self.selected_city_data['datetime'])
        return self.selected_city_data

    
    def preprocess_temperature_data(self):
        self.temperature_data = self.temperature_data.dropna().reset_index().drop('index',axis=1)

