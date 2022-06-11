# Overall notes for Prefect

## 3.1
- Prefect is ML-oriented workflow orchestration software
- Can handle fully-featured, interconnected pipelines
- Handles conditional pipelines and has built-in, graceful retries

## 3.2
- Prefect is modern, active, has cloud and free/local options
- Moving to 2.0; overhaul to remove DAG requirement for pipelines
	- Devs were often "fighting" the pipeline
- Focused on transparent, observable workflow and rules
- Easy integration with @flow and @task annotations

- Need to convert Jupyter notebooks to scripts as they are more ideal for production
	- Want to convert things in functions as granular as you want visibility
		- More or less the same as functions you normally would make
	- These functions appear in Prefect flow runs as points of visibility

## 3.3
- Prefect normally used to retrain models over time
- Add @flow to start of flow you want to track
	- Add @task for each function you want to track in that flow
- Prefect flow can take in Prefect or Python code, just need to call .result()
        - E.g. add_features(...).result()
- Use Prefect server to make web dashboard to view flows and runs, port 4200
- Can see all flow runs and logs of it worked
- Sometimes need to set flow_runner=SequentialTaskRunner() in @flow
	- May not play nice with MLflow; need to disable concurrency
- Can use pydantic with Prefect to check input type for functions
- Creates Prefect logs without running Prefect

# 3.4
- Need to open HTTP, HTTPS, 4200 ports (UDP and TCP)
- Where running server, set: prefect config set PREFECT_ORION_UI_API_URL="http://<external-ip>:4200/api"
	- If issue, check: prefect config view. May need to unset PREFECT_ORION_UI_API_URL
- Start Orion with: prefect orion start --host 0.0.0.0
- In code running terminal run: prefect config set PREFECT_API_URL="http://<external-ip>:4200/api"
- Prefect cloud has authentication and API tokens
        - Free/local/open-source has no authentication

# 3.5
- 3 things needed for flow run:
        1. Storage for flows - can be local, cloud, NAS etc
        2. Deployment - can be on local, docker, kube etc
        3. Work Queue - can have filter what it can pick. Gives agent
        4. Run agent locally or docker host

- To integrate with MLflow
        - Could write a flow that writes every week for model training
                - Compares model with model in production
                - If better, promote to production
        - This is more of a real example of Prefect in industry
