from fastapi import FastAPI
import uvicorn
import joblib

import gcsfs

from pydantic_types import InputIris, OutputPredict

gsc_client = gcsfs.GCSFileSystem()

TARGET_NAMES = ['setosa', 'versicolor', 'virginica']

model_destination_uri = 'gs://ue-models-enrique/iris_clasification/model.pkl'
with gsc_client.open(model_destination_uri, 'rb') as f:
    pipe = joblib.load(f)

app = FastAPI(title='Iris')

@app.post('/predict', response_model=OutputPredict)
def predict(input_iris: InputIris):
    probs = pipe.predict_proba([[input_iris.petal_length, input_iris.petal_width]])
    return {
        'results': [
            {name: prob for name, prob in zip(TARGET_NAMES, p)}
            for p in probs
        ][0]
    }

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)