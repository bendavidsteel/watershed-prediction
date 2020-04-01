
import os

import numpy as np
import pandas as pd

import preprocessor

def get_distance_weight(gage_a, gage_b, weights):
    cell = weights.query('InputID=={0}&TargetID=={1}'.format(gage_a,gage_b))['Distance']
    return 1/cell.values[0]

def get_altitude_weight(a, b, weights):
    a_height = weights[weights['Gage'] == a][' Altitude'].values[0]
    b_height = weights[weights['Gage'] == b][' Altitude'].values[0]
    return 1/np.abs(a_height - b_height)

def interpolate_daily_precip_gages():
    this_path = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(this_path, "dataset")

    gage_distances = pd.read_csv(os.path.join(dataset_path, "distanceMatrix.csv"), 
                             usecols=[1,2,3],
                             delimiter="	")

    gage_precip = pd.read_csv(os.path.join(dataset_path, "dailyGagePrecip1956-2019.csv"), names=["Date", "RainGage", "Precipitation"], header=0)
    # reshape so that raingage is also column
    gage_precip = pd.pivot_table(gage_precip, values='Precipitation', 
                    index='Date',
                    columns='RainGage').reset_index('Date')

    gage_precip.head()

    interpolated = preprocessor.replace_nan_with_weighted_mean(gage_precip.drop(['Date', 'RG18'], axis=1), gage_distances, get_distance_weight)

    interpolated['Date'] = gage_precip['Date']
    interpolated.to_csv(os.path.join(dataset_path, "distanceInterpolatedDailyGagePrecip.csv"))

def interpolate_daily_snowwater():
    this_path = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(this_path, "dataset")

    gage_altitudes = pd.read_csv(os.path.join(dataset_path, "gageAltitudes.csv"))

    snowwater = pd.read_csv(os.path.join(dataset_path, "HBEF_snowwater1956-2018.csv"),
                            names=["Winter","Date","STA1","STA2","STA3","STA4","STA5", \
                                   "STA6","STA7","STA8","STA9","STA10","STA11","STA12", \
                                   "STA13","STA14","STA15","STA16","STA17","STA19","STA20","STA21","STA22"], header=0)

    interpolated = preprocessor.replace_nan_with_weighted_mean(snowwater.drop(['Date', 'Winter'], axis=1),
                                                               gage_altitudes, 
                                                               get_altitude_weight, 
                                                               nan_function=lambda x: x == -99, 
                                                               column_name_converter=lambda x: "RG" + x[3:])

    interpolated['Date'] = snowwater['Date']
    interpolated['Winter'] = snowwater['Winter']
    interpolated.to_csv(os.path.join(dataset_path, "altitudeInterpolatedDailySnowwater.csv"))

if __name__ == "__main__":

    interpolate_daily_snowwater()