#!/usr/bin/env python
# coding: utf-8

import sys
import pickle
import pandas as pd
import numpy as np


categorical = ['PUlocationID', 'DOlocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def save_results(df, y_pred, output_file):
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['pickup_datetime'] = df['pickup_datetime']
    df_result['PUlocationID'] = df['PUlocationID']
    df_result['DOlocationID'] = df['DOlocationID']
    df_result['actual_duration'] = df['duration']
    df_result['predicted_duration'] = y_pred
    df_result['diff'] = df_result['actual_duration'] - df_result['predicted_duration']

    df_result.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )

def apply_model(year, month):
    with open('model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)

    df = read_data(f'https://nyc-tlc.s3.amazonaws.com/trip+data/fhv_tripdata_{year:04d}-{month:02d}.parquet')
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)

    print(f'Mean predicted duration is {np.mean(y_pred)}')

    output_file = f'./output/fhv_tripdata{year:04d}-{month:02d}.parquet'
    save_results(df, y_pred, output_file)


def run():
    year = int(sys.argv[1]) # 2021
    month = int(sys.argv[2]) # 3

    apply_model(year=year, month=month)


if __name__ == '__main__':
    run()




