import os
import pickle

import mlflow
from mlflow.tracking import MlflowClient
from flask import Flask, request, jsonify


# RUN_ID = os.getenv('RUN_ID')
RUN_ID = '86bf545d5c6c4a14b59b44c933a4c42b'

print(f"Getting model from {RUN_ID}")
# logged_model = f's3://mlflow-models-alexey/1/{RUN_ID}/artifacts/model'
logged_model = f'runs:/{RUN_ID}/model'

MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'
print(f"Connecting to MLflow at {MLFLOW_TRACKING_URI}...")
mlflow.set_tracking_uri("http://127.0.0.1:5000")
# mlflow.set_experiment("green-taxi-duration")
# client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)

model = mlflow.pyfunc.load_model(logged_model)

# path = client.download_artifacts(run_id=RUN_ID, path='dict_vectorizer.bin')
# print(f"Downloading the dict vectorizer to {path}")

# with open(path, 'rb') as f_out:
#     dv = pickle.load(f_out)

def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features


def predict(features):
    preds = model.predict(features)
    # X = dv.transform(features)
    # preds = model.predict(X)
    return float(preds[0])


app = Flask('duration-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()

    features = prepare_features(ride)
    pred = predict(features)

    result = {
        'duration': pred,
        'model_version': RUN_ID
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
