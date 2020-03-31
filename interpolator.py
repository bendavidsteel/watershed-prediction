
import os

import pandas as pd

import preprocessor

def get_distance_weight(gage_a, gage_b, weights):
    cell = weights.query('InputID=={0}&TargetID=={1}'.format(gage_a,gage_b))['Distance']
    return 1/cell.values[0]\

def get_altitude_weight(a, b, weights):
    

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

if __name__ == "__main__":

    interpolate_daily_precip_gages()