# Summary
- Use homework.py (notebook from 01 converted)
- Need to schedule running this in Prefect
	1. Run once a month
	2. Takes parameter `date`
		a. Defaults to `None`
		b. If `None`, set as current day.
			- Train. data: data from 2 months back
			- Valid. data: data from 1 month back
		c. If not `None`:
			- Train. data: data from 2 months before `date`
			- Valid. data:	data from 1 month before `date`
		d. i.e. `date` is '2021-03-15':
			- Train. data: 'fhv_tripdata_2021_01.parquet'
			- Valid. data: 'fhv_tripdata_2021_02.parquet'
	3. Save model as 'model-{date}.bin' as 'YYYY-MM-DD' from `date`
		- Makes getting models easy in practice as it is simply the latest
	4. Use and reuse DictVectorizer for future data. Save as 'dv-{date}.b'
		- `date` '2021-03-15' gives files 'model-2021-03-15.bin' and 'dv-2021-03-15.b'
- Not a strict convention in industry. Might use different scheme or want to train on all data
- On deploy side, easy to just pull in latest data and predict using latest model/vectorizer
	- MLflow could do this very well
- This homework is about the **batch training**

1. Convert script to a Flow
2. Change parameters to take in `date`. Make this parameter dynamic
3. Scheduling batch training job that outputs the latest model somewhere

## Answers

1. Before setting `.result()`:
	(prefect-env) andre $ python homework.py 
	17:39:00.017 | INFO    | prefect.engine - Created flow run 'emerald-kangaroo' for flow 'main'
	17:39:00.017 | INFO    | Flow run 'emerald-kangaroo' - Using task runner 'SequentialTaskRunner'
	17:39:00.192 | INFO    | Flow run 'emerald-kangaroo' - Created task run 'read_data-4c7f9de4-0' for task 'read_data'
	17:39:33.564 | INFO    | Flow run 'emerald-kangaroo' - Created task run 'prepare_features-4ee39d9f-0' for task 'prepare_features'
	17:39:36.666 | INFO    | Flow run 'emerald-kangaroo' - Created task run 'read_data-4c7f9de4-1' for task 'read_data'
	17:42:22.300 | INFO    | Task run 'read_data-4c7f9de4-1' - Finished in state Completed()
	17:42:22.397 | INFO    | Flow run 'emerald-kangaroo' - Created task run 'prepare_features-4ee39d9f-1' for task 'prepare_features'
	17:42:22.714 | INFO    | Task run 'prepare_features-4ee39d9f-1' - The mean duration of validation is 16.859265811074096
	17:43:15.903 | INFO    | Task run 'prepare_features-4ee39d9f-1' - Finished in state Completed()
	17:43:15.998 | INFO    | Flow run 'emerald-kangaroo' - Created task run 'train_model-7c866860-0' for task 'train_model'
	17:43:16.089 | ERROR   | Flow run 'emerald-kangaroo' - Encountered exception during execution:
	Traceback (most recent call last):
	    ...
	    **lr, dv = train_model(df_train_processed, categorical)#.result()**
	TypeError: cannot unpack non-iterable PrefectFuture object
	17:43:16.147 | ERROR   | Flow run 'emerald-kangaroo' - Finished in state Failed('Flow run encountered an exception.')
   After setting `lr, dv = train_model(df_train_processed, categorical).result()`
	(prefect-env) andre $ python homework.py 
	17:56:51.920 | INFO    | prefect.engine - Created flow run 'deft-kittiwake' for flow 'main'
	17:56:51.920 | INFO    | Flow run 'deft-kittiwake' - Using task runner 'SequentialTaskRunner'
	17:56:52.058 | INFO    | Flow run 'deft-kittiwake' - Created task run 'read_data-4c7f9de4-0' for task 'read_data'
	17:57:37.532 | INFO    | Task run 'read_data-4c7f9de4-0' - Finished in state Completed()
	17:57:37.616 | INFO    | Flow run 'deft-kittiwake' - Created task run 'prepare_features-4ee39d9f-0' for task 'prepare_features'
	17:57:37.938 | INFO    | Task run 'prepare_features-4ee39d9f-0' - The mean duration of training is 16.2472533682457
	17:58:31.437 | INFO    | Task run 'prepare_features-4ee39d9f-0' - Finished in state Completed()
	17:58:31.520 | INFO    | Flow run 'deft-kittiwake' - Created task run 'read_data-4c7f9de4-1' for task 'read_data'
	17:59:12.515 | INFO    | Task run 'read_data-4c7f9de4-1' - Finished in state Completed()
	17:59:12.602 | INFO    | Flow run 'deft-kittiwake' - Created task run 'prepare_features-4ee39d9f-1' for task 'prepare_features'
	17:59:12.879 | INFO    | Task run 'prepare_features-4ee39d9f-1' - The mean duration of validation is 16.859265811074096
	18:00:01.626 | INFO    | Task run 'prepare_features-4ee39d9f-1' - Finished in state Completed()
	18:00:01.731 | INFO    | Flow run 'deft-kittiwake' - Created task run 'train_model-7c866860-0' for task 'train_model'
	18:00:05.057 | INFO    | Task run 'train_model-7c866860-0' - The shape of X_train is (1109826, 525)
	18:00:05.057 | INFO    | Task run 'train_model-7c866860-0' - The DictVectorizer has 525 features
	18:00:09.400 | INFO    | Task run 'train_model-7c866860-0' - The MSE of training is: 10.528519403716007
	18:00:09.629 | INFO    | Task run 'train_model-7c866860-0' - Finished in state Completed()
	18:00:09.687 | INFO    | Flow run 'deft-kittiwake' - Created task run 'run_model-6559300c-0' for task 'run_model'
	18:00:12.494 | INFO    | Task run 'run_model-6559300c-0' - The MSE of validation is: 11.014287719752
	18:00:12.601 | INFO    | Task run 'run_model-6559300c-0' - Finished in state Completed()
	18:00:18.295 | INFO    | Flow run 'deft-kittiwake' - Finished in state Completed('All states completed.')
   **train_model** needed .result().

2. Running with `main(date="2021-08-15")`:
	(prefect-env) andre@DESKTOP-U5K6US2:/mnt/e/andre/OneDrive - The University of Western Ontario/mlops-zoomcamp/03-orchestration$ python my_homework.py 
	00:20:24.176 | INFO    | prefect.engine - Created flow run 'impartial-woodlouse' for flow 'main'
	00:20:24.176 | INFO    | Flow run 'impartial-woodlouse' - Using task runner 'ConcurrentTaskRunner'
	00:20:24.226 | INFO    | Flow run 'impartial-woodlouse' - Created task run 'get_paths-6e696e34-0' for task 'get_paths'
	00:20:24.268 | INFO    | Task run 'get_paths-6e696e34-0' - Finished in state Completed()
	00:20:24.288 | INFO    | Flow run 'impartial-woodlouse' - Created task run 'read_data-4c7f9de4-0' for task 'read_data'
	00:20:24.315 | INFO    | Flow run 'impartial-woodlouse' - Created task run 'prepare_features-4ee39d9f-0' for task 'prepare_features'
	00:20:30.479 | INFO    | Task run 'read_data-4c7f9de4-0' - Finished in state Completed()
	00:20:30.904 | INFO    | Task run 'prepare_features-4ee39d9f-0' - The mean duration of training is 18.230538791569113
	00:20:37.886 | INFO    | Task run 'prepare_features-4ee39d9f-0' - Finished in state Completed()
	00:20:37.912 | INFO    | Flow run 'impartial-woodlouse' - Created task run 'read_data-4c7f9de4-1' for task 'read_data'
	00:20:37.958 | INFO    | Flow run 'impartial-woodlouse' - Created task run 'prepare_features-4ee39d9f-1' for task 'prepare_features'
	00:20:43.745 | INFO    | Task run 'read_data-4c7f9de4-1' - Finished in state Completed()
	00:20:44.190 | INFO    | Task run 'prepare_features-4ee39d9f-1' - The mean duration of validation is 17.91113046137945
	00:20:50.858 | INFO    | Task run 'prepare_features-4ee39d9f-1' - Finished in state Completed()
	00:20:50.881 | INFO    | Flow run 'impartial-woodlouse' - Created task run 'train_model-7c866860-0' for task 'train_model'
	00:20:55.049 | INFO    | Task run 'train_model-7c866860-0' - The shape of X_train is (1222031, 525)
	00:20:55.050 | INFO    | Task run 'train_model-7c866860-0' - The DictVectorizer has 525 features
	00:20:59.136 | INFO    | Task run 'train_model-7c866860-0' - The MSE of training is: 11.789353672062306
	00:20:59.280 | INFO    | Task run 'train_model-7c866860-0' - Finished in state Completed()
	00:20:59.303 | INFO    | Flow run 'impartial-woodlouse' - Created task run 'run_model-6559300c-0' for task 'run_model'
	00:21:02.942 | INFO    | Task run 'run_model-6559300c-0' - **The MSE of validation is: 11.637032341248355**
	00:21:03.033 | INFO    | Task run 'run_model-6559300c-0' - Finished in state Completed()
	00:21:09.458 | INFO    | Flow run 'impartial-woodlouse' - Finished in state Completed('All states completed.')  
