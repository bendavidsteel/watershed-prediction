# uses functions from https://www.tensorflow.org/tutorials/structured_data/time_series

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import parser

def get_data():
    gage_precip, snowwater, streamflow = parser.get_raw_data()

    # combining all rows between tables with a shared date
    continuous_data = pd.merge(gage_precip, streamflow, how='inner', on='Date')

    # get average of available data for each date from snowwater
    snowwater["Mean"] = snowwater.replace(to_replace='-99', value=np.nan).mean(axis=1)
    # drop all but date and mean
    snowwater = snowwater.filter(['Winter', 'Date', 'Mean'])

    # merge dataframes
    all_data = pd.merge(continuous_data, snowwater, how='left', on='Date')

    # interpolate snow water data, using a limit of 30 days to ensure interpolation does not occur over summer dates
    all_data["Mean"] = all_data["Mean"].interpolate(limit=30)
    # replace NaNs in summer dates with zeros
    all_data = all_data.replace(to_replace=np.nan, value=0)

    return all_data

def univariate_data(dataset, start_index, end_index, history_size, target_size):
    data = []
    labels = []

    start_index = start_index + history_size
    if end_index is None:
        end_index = len(dataset) - target_size

    for i in range(start_index, end_index):
        indices = range(i-history_size, i)
        # Reshape data from (history_size,) to (history_size, 1)
        data.append(np.reshape(dataset[indices], (history_size, 1)))
        labels.append(dataset[i+target_size])
    return np.array(data), np.array(labels)


def multivariate_data(dataset, target, start_index, end_index, history_size,
                      target_size, step, single_step=False):
    data = []
    labels = []

    start_index = start_index + history_size
    if end_index is None:
        end_index = len(dataset) - target_size

    for i in range(start_index, end_index):
        indices = range(i-history_size, i, step)
        data.append(dataset[indices])

        if single_step:
            labels.append(target[i+target_size])
        else:
            labels.append(target[i:i+target_size])

    return np.array(data), np.array(labels)


def replace_nan_with_weighted_mean(dataset, weights):
    for index, row in dataset.iterrows():
        
def get_distance(gage_a, gage_b, weights):
    cell = weights.query('InputID=={0}&TargetID=={1}'.format(gage_a,gage_b))['Distance']
    return cell.values[0]

def replace_nan_with_weighted_mean(dataset, weights):
    for index, row in dataset.iterrows():
        present_values = {}
        for col, value in row.iteritems():
            if not math.isnan(value):
                present_values[col[2:]] = value
                
        for col, value in row.iteritems():
            if math.isnan(value):
                accu = 0
                total_dist = 0
                for key, val in present_values.items():
                    try:
                        dist = get_distance(key, col[2:], weights)
                    except IndexError:
                        dist = 1
                    accu += val * dist
                    total_dist += dist
                new_val = accu / total_dist
                dataset.at[index,col] = new_val   
    
    return dataset