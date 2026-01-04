# FastAPI - V1 simple API -> http://127.0.0.1:8000/docs

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import pandas as pd
import mlflow.sklearn

# -----------------------
# Import promethus client for metrics
# -----------------------
from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST
)
from fastapi.responses import Response
import time



# -----------------------
# CONFIG
# -----------------------

RUN_ID = "d68e2c6350b4442f88e217726763b0f0" # replace with your actual run ID
MODEL_URI = f"runs:/{RUN_ID}/model"

model= None

# -----------------------
# PROMETHEUS METRICS
# -----------------------

PREDICTIONS_TOTAL = Counter(
    "predictions_total",
    "Total number of prediction requests"
)

PREDICTION_ERRORS_TOTAL = Counter(
    "prediction_errors_total",
    "Total number of prediction errors"
)

PREDICTION_LATENCY = Histogram(
    "prediction_latency_seconds",
    "Prediction latency in seconds"
)

IN_PROGRESS = Gauge(
    "prediction_requests_in_progress",
    "Number of prediction requests in progress"
)


"""
# PROMETHEUS: Why global?
1.Prometheus metrics must be process-wide
2.Not per request
"""

# -----------------------
# LIFESPAN HANDLER
# -----------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        model = mlflow.sklearn.load_model(MODEL_URI)
    except Exception as e:
        raise RuntimeError(f"Failed to load model: {e}")

    if not hasattr(model, "feature_names_in_"):
        raise RuntimeError("Model does not expose feature names")

    app.state.model = model
    app.state.feature_columns = list(model.feature_names_in_)

    print("Model loaded successfully")
    print(f"Number of features: {len(app.state.feature_columns)}")

    yield  # App is running

    # Optional cleanup
    print("Shutting down API")
    

# “We use FastAPI lifespan handlers to load the MLflow model once at startup and store it in application state, 
# ensuring efficient memory usage and clean lifecycle management.”
    


# -----------------------
# APP INIT
# -----------------------

app = FastAPI(
	title="Fraud Detection API V1",
	description= 'Real-Time fraud prediction using MLflow model',
	version="1.0",
    lifespan=lifespan
)


# -----------------------
# REQUEST SCHEMA
# -----------------------

class PredictionRequest(BaseModel):
    data: dict # key: feature name, value: feature value
    
# -----------------------
# HEALTH CHECK
# -----------------------

@app.get("/health")
def health():
    return {"status": "ok"}

# @app.get("/ready")
# def ready():
#     if model is None:
#         return JSONResponse(
#             status_code=503,
#             content={"status": "model not loaded"}
#         )
#     return {"status": "ready"}


# -----------------------
# PREDICTION ENDPOINT
# -----------------------

# @app.post("/predict")
# def predict(request: PredictionRequest):
#     model = app.state.model
#     feature_columns = app.state.feature_columns

#     try:
#         input_df = pd.DataFrame([request.data])
#         input_df = input_df[feature_columns]

#         fraud_prob = model.predict_proba(input_df)[0][1]

#         return {
#             "fraud_probability": float(fraud_prob)
#         }

#     except KeyError as e:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Missing feature: {e}"
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )


# PROMETHEUS METRICS ENDPOINT
@app.get('/metrics')
def metrics():
    return Response(
		generate_latest(),
		media_type=CONTENT_TYPE_LATEST
	)



# -----------------------
# Updated PREDICTION ENDPOINT -> with Prometheus metrics
# -----------------------

@app.post("/predict")
def predict(request: PredictionRequest):
    model = app.state.model
    feature_columns = app.state.feature_columns
    
    start_time = time.time()
    IN_PROGRESS.inc()

    try:
        input_df = pd.DataFrame([request.data])
        input_df = input_df[feature_columns]

        fraud_prob = model.predict_proba(input_df)[0][1]

        PREDICTIONS_TOTAL.inc() # “One more prediction request happened.” > You never decrease a counter.
        return {
            "fraud_probability": float(fraud_prob)
        }

    except Exception as e:
        PREDICTION_ERRORS_TOTAL.inc()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
    finally:
        latency = time.time() - start_time
        PREDICTION_LATENCY.observe(latency)
        IN_PROGRESS.dec()
