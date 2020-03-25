import os
import pandas as pd

file_names = {
    "daily_gage_precip" : "dailyGagePrecip1956-2019.csv",
    "daily_watershed_precip" : "dailyWatershedPrecip1956-2019.csv",
    "daily_streamflow" : "HBEF_DailyStreamflow_1956-2017_longform.csv",
    "daily_snowwater" : "HBEF_snowwater1956-2018.csv"
}

this_path = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(this_path, "dataset")

def get_raw_data():
    
    gage_precip = pd.read_csv(os.path.join(dataset_path, file_names["daily_gage_precip"]), names=["Date", "RainGage", "Precipitation"], header=0)
    # reshape so that raingage is also column
    gage_precip = pd.pivot_table(gage_precip, values='Precipitation', 
                       index='Date',
                       columns='RainGage').reset_index('Date')

    snowwater = pd.read_csv(os.path.join(dataset_path, file_names["daily_snowwater"]), names=["Winter","Date","STA1","STA2","STA3","STA4","STA5", \
                                                                                              "STA6","STA7","STA8","STA9","STA10","STA11","STA12", \
                                                                                              "STA13","STA14","STA15","STA16","STA17","STA19","STA20","STA21","STAHQ"], header=0)

    streamflow = pd.read_csv(os.path.join(dataset_path, file_names["daily_streamflow"]), names=["Date", "Watershed", "Streamflow"], header=0)
    streamflow = pd.pivot_table(streamflow, values='Streamflow', 
                       index='Date',
                       columns='Watershed').reset_index('Date')

    return gage_precip, snowwater, streamflow
