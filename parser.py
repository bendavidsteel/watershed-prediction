import pandas as pd

file_names = {
    "aggregate_early" : "runoff_aggregrateh_early.asp",
    "aggregate_late" : "runoff_aggregateh_later.asp",
    "event_early" : "runoff_eventh_early.asp",
    "event_late" : "runoff_eventh_later.asp"
}

dataset_path = "../dataset/"

def get_flume_areas():
    # all files have same areas values
    with open(dataset_path + file_names["aggregate_early"], "rt") as f:
        for line_num in range(len(f)):
            if f[line_num] == "#Flume areas in acres:":
                area_line_num = line_num + 1
                break

        area_line = f[area_line_num]

    # strip superfluous chars
    area_line = area_line.replace('#', '')

    area_strings = area_line.split(',')
    areas = {}
    for area_string in area_strings:
        flume, area_str = area_string.split(':')
        areas[flume] = float(area)

    return areas

def get_aggregate_data():
    

def get_dataframe_from_file(file_path):
    return pd.read_csv(file_path, header=9)
