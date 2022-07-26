import batch

import pandas as pd

from datetime import datetime

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
        ('-1', '-1', dt(1, 2), dt(1, 10), 8.0), # Nan IDs, 8 min duration
        ('1', '1', dt(1, 2), dt(1, 10), 8.0),   # ID 1, 1, 8 minute duration
    ]
    columns.append('duration')
    expected_df = pd.DataFrame(expected_data, columns=columns)
    
    actual_df = prepare_data(df, categorical)

    pd.testing.assert_frame_equal(actual_df, expected_df)
