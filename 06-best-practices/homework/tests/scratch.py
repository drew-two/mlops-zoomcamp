import pandas as pd

from datetime import datetime

def prepare_data(df: pd.DataFrame, categorical):
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def dt(hour, minute, second=0):
    return datetime(2021, 1, 1, hour, minute, second)

def test_prepare_data():
    data = [
        (None, None, dt(1, 2), dt(1, 10)),  # Nan IDs, 8 min duration
        (1, 1, dt(1, 2), dt(1, 10)),        # ID 1, 1, 8 minute duration
        (1, 1, dt(1, 2, 0), dt(1, 2, 50)),  # ID 1 1, 50 second duration
        (1, 1, dt(1, 2, 0), dt(2, 2, 1)),   # ID 1 1, 61 minute duration
    ]

    categorical = ['PUlocationID', 'DOlocationID']
    columns = ['PUlocationID', 'DOlocationID', 'pickup_datetime', 'dropOff_datetime']
    df = pd.DataFrame(data, columns=columns)

    expected_data = [
        ('-1', '-1', dt(1, 2), dt(1, 10), (600 - 120) / 60),  # Nan IDs, 8 min duration
        ('1', '1', dt(1, 2), dt(1, 10), (600 - 120) / 60),        # ID 1, 1, 8 minute duration
    ]
    columns.append('duration')

    expected_df = pd.DataFrame(expected_data, columns=columns)

    actual_df = prepare_data(df, categorical)

    print(actual_df.compare(expected_df))
    pd.testing.assert_frame_equal(actual_df, expected_df)
    # assert actual_df == expected_df

test_prepare_data()