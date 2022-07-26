import os, sys
import pandas as pd

from datetime import datetime

def dt(hour, minute, second=0):
    return datetime(2021, 1, 1, hour, minute, second)

# data = [
#     (None, None, dt(1, 2), dt(1, 10)),  # Nan IDs, 8 min duration
#     (1, 1, dt(1, 2), dt(1, 10)),        # ID 1, 1, 8 minute duration
#     (1, 1, dt(1, 2, 0), dt(1, 2, 50)),  # ID 1 1, 50 second duration
#     (1, 1, dt(1, 2, 0), dt(2, 2, 1)),   # ID 1 1, 61 minute duration
# ]
# columns = ['PUlocationID', 'DOlocationID', 'pickup_datetime', 'dropOff_datetime']
# df_input = pd.DataFrame(data, columns=columns)

S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')
options = {
    'client_kwargs': {
        'endpoint_url': S3_ENDPOINT_URL
    }
}

year = 2021
month = 1
input_file = f's3://nyc-duration/taxi_type=fhv/year={year:04d}/month={month:02d}/predictions.parquet'

# df_input.to_parquet(
#     input_file,
#     engine='pyarrow',
#     compression=None,
#     index=False,
#     storage_options=options
# )

my_dir = os.path.dirname(sys.argv[0])
os.system('%s %s %s %s' % (sys.executable, 
                        os.path.join(my_dir, '../batch.py'),
                        os.path.join('2021'),
                        os.path.join('1')))

df = pd.read_parquet('s3://nyc-duration/out/2021-01.parquet', storage_options=options)

print(df['predicted_duration'].sum())
