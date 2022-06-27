from prefect.deployments import DeploymentSpec
from prefect.orion.schemas.schedules import CronSchedule
from prefect.flow_runners import SubprocessFlowRunner


DeploymentSpec(
    flow_location="my_score.py",
    name="ride_duration_prediction",
    parameters={
        "taxi_type": "green",
        "run_id": "cd0a53fdc9b74cae82cbcd0c1d4c6b77",
    },
    flow_storage="71cf14fc-b503-4ab2-b9e9-89358e61c6b6",
    schedule=CronSchedule(cron="0 3 2 * *"),
    flow_runner=SubprocessFlowRunner(),
)