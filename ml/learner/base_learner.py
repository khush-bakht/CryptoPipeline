from abc import ABC, abstractmethod
import optuna
import pandas as pd
import joblib
import os
import json
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from typing import Dict, Any

class BaseLearner(ABC):
    def __init__(self, symbol: str, time_horizon: str, model_name: str):
        self.symbol = symbol
        self.time_horizon = time_horizon
        self.model_name = model_name
        self.best_model = None
        self.best_params = None
        self.best_score = float('inf')
        self.metrics = {}
        
    @abstractmethod
    def get_search_space(self, trial: optuna.Trial) -> Dict[str, Any]:
        """Define hyperparameter search space for Optuna"""
        pass
        
    @abstractmethod
    def train_model(self, X_train: pd.DataFrame, y_train: pd.Series, params: Dict[str, Any]):
        """Train model with given parameters"""
        pass
        
    def objective(self, trial: optuna.Trial, X_train: pd.DataFrame, y_train: pd.Series, 
                 X_val: pd.DataFrame, y_val: pd.Series) -> float:
        """Optuna objective function"""
        params = self.get_search_space(trial)
        model = self.train_model(X_train, y_train, params)
        
        # Evaluate model
        predictions = model.predict(X_val)
        error = mean_squared_error(y_val, predictions)
        
        # Track additional metrics
        self.metrics[trial.number] = {
            'mae': mean_absolute_error(y_val, predictions),
            'mse': mean_squared_error(y_val, predictions),
            'rmse': mean_squared_error(y_val, predictions, squared=False),
            'r2': r2_score(y_val, predictions),
            'params': params
        }
        
        return error
        
    def save_model(self, path: str):
        """Save trained model to disk"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({
            'model': self.best_model,
            'params': self.best_params,
            'metrics': self.metrics
        }, path)
        
    def load_model(self, path: str):
        """Load trained model from disk"""
        saved_data = joblib.load(path)
        self.best_model = saved_data['model']
        self.best_params = saved_data['params']
        self.metrics = saved_data.get('metrics', {})
        return self.best_model
    def predict(self, X):
        return self.best_model.predict(X)