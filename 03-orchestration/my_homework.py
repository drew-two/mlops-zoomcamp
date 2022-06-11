import pandas as pd

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from prefect import flow, task
from prefect.task_runners import SequentialTaskRunner
from prefect.logging import get_run_logger

from datetime import date

import pickle

@task
def get_paths(date):

    logger = get_run_logger()

    if date == None:
        date = date.today()
        logger.debug(date)
    
    # Getting year and month as integers
    date_split = date.split('-')
    year = int(date_split[0])
    month = int(date_split[1])

    train_month = month - 2
    train_year = year
    if train_month <= 0: # If train month is 0 or less, the data is from last year
        train_year = year - 1 # Go back a year if last year
        train_month = 12 + train_month  # Add negative value to 12 to get month from last year
    
    train_path = f"./data/fhv_tripdata_{train_year:02d}-{train_month:02d}.parquet"

    val_month = month - 1
    val_year = year
    if val_month <= 0:
        val_year = year - 1 # Same logic
        val_month = 12 + train_month

    val_path = f"./data/fhv_tripdata_{val_year:02d}-{val_month:02d}.parquet"

    logger.debug(train_path)
    logger.debug(val_path)

    return train_path, val_path    

@task
def read_data(path):
    df = pd.read_parquet(path)
    return df

@task
def prepare_features(df, categorical, train=True):

    logger = get_run_logger()
    logger.debug(f"Preparing for {train}")

    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    mean_duration = df.duration.mean()
    if train:
        logger.info(f"The mean duration of training is {mean_duration}")
    else:
        logger.info(f"The mean duration of validation is {mean_duration}")
    
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    logger.debug(df.head())
    return df

@task
def train_model(df, categorical):

    logger = get_run_logger()
    logger.debug("Getting Dict")

    train_dicts = df[categorical].to_dict(orient='records')
    logger.debug("Got Dict")
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts) 
    y_train = df.duration.values

    logger.info(f"The shape of X_train is {X_train.shape}")
    logger.info(f"The DictVectorizer has {len(dv.feature_names_)} features")

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_train)
    mse = mean_squared_error(y_train, y_pred, squared=False)
    logger.info(f"The MSE of training is: {mse}")
    return lr, dv

@task
def run_model(df, categorical, dv, lr):
    logger = get_run_logger()

    val_dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(val_dicts) 
    y_pred = lr.predict(X_val)
    y_val = df.duration.values

    mse = mean_squared_error(y_val, y_pred, squared=False)
    logger.info(f"The MSE of validation is: {mse}")
    return

@flow#(task_runner=SequentialTaskRunner())
def main(date=None):
    train_path, val_path = get_paths(date).result()
    # rest of flow below

    categorical = ['PUlocationID', 'DOlocationID']

    df_train = read_data(train_path)
    df_train_processed = prepare_features(df_train, categorical).wait()
    
    df_val = read_data(val_path)
    df_val_processed = prepare_features(df_val, categorical, False).wait()

    # train the model
    lr, dv = train_model(df_train_processed, categorical).result()
    run_model(df_val_processed, categorical, dv, lr)

    # saving artifacts
    with open(f"./model-{date}.bin", 'wb') as f_out:
        pickle.dump(lr, f_out)

    with open(f"./dv-{date}.bin", 'wb') as f_out:
        pickle.dump(dv, f_out)

# main(date="2021-08-15")

from prefect.deployments import DeploymentSpec
from prefect.orion.schemas.schedules import CronSchedule
from prefect.flow_runners import SubprocessFlowRunner
from datetime import timedelta

DeploymentSpec(
    flow=main,
    name="model_training",
    schedule=CronSchedule(
        cron="0 9 10 * *",
        timezone="America/New_York"),
    flow_runner=SubprocessFlowRunner(),
    tags=["ml"]
)