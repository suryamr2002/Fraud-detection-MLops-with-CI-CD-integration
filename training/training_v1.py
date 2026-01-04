import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

# lets import mlflow for model tracking
import mlflow
import mlflow.sklearn

import os	
# Disable MLflow usage tracking
os.environ["MLFLOW_DISABLE_TELEMETRY"] = "true"

EXPERIMENT_NAME = "fraud_detection_v1" 



if __name__ == "__main__":
    # create / get experiment
    mlflow.set_experiment(EXPERIMENT_NAME) 
    
    with mlflow.start_run(run_name='logistc_regression_v1'):
        # load the data
        df = pd.read_parquet("spark/processed_train.parquet")
        print('Data loaded for training.')

        X = df.drop(columns=["isFraud"])
        y = df["isFraud"]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        print('Model created for training.')
        model = LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        )

        # log parameters
        mlflow.log_param('model_type', 'LogisticRegression')
        mlflow.log_param('max_iter', 1000)
        mlflow.log_param("class_weight", "balanced")  
        mlflow.log_param("num_features", X_train.shape[1])
    
        # Train	
        model.fit(X_train, y_train)

        print('Model trained.')
        preds = model.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, preds)

        # Log metric
        mlflow.log_metric('roc_auc',auc)

        # log model artifact
        mlflow.sklearn.log_model(
            model,
            name='model'
        )

        print(f"V1 Model AUC: {auc:.4f}")
