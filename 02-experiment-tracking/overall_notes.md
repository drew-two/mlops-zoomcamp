## Logging models in mlflow
Two options:
- Log model as artifact
	- Not very useful
- Log model with mlflow.<framework>.log_model
	- Stored much more information that let us load it very easily
	- Can be saved in two flavours : PYthon and the framework
	- Can be opened in Python, Jupyter, docker, Spark, Kube, AWS Sagemaker etc

## MLflowClient Class
- Creates client for:
	- MLflow Tracking Server for creating/managing experiments/runs
	- MLflow Registry Server for creating/managing models/model versions
- To instantiate we need to pass tracking URI and/or registry URI:
	- from mlflow.tracking import MlflowClient
	
	  MLFLOW_TRACKING_URI = "sqlite:///mlflow.db" 
	- Otherwise MLflow will assume you're checking local folders
	- Can also call remote server

## Model Management in MLflow
- Model Registry component is a **centralized model store**, set of APIs, and UI
- Allows collaborative management of full lifecycle of MLflow model.
- Provides:
	- Mode lineage - have all the information of how model was built, link to model run 
	- Model versioning - Auto versioning
	- Stage transitions - Set stage, can automatically set last production model to archive
	- Annotations
