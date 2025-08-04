from sklearn.tree import DecisionTreeRegressor
from .base_learner import BaseLearner
import optuna
import pandas as pd

class DecisionTreeLearner(BaseLearner):
    def __init__(self, symbol, time_horizon, model_name):
        super().__init__(symbol, time_horizon, model_name)

    def get_search_space(self, trial):
        return {
            'max_depth': trial.suggest_int('max_depth', 3, 15),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10),
            'max_features': trial.suggest_categorical(
                'max_features', [None, 'sqrt', 'log2', 0.5]  
            ),
            'splitter': trial.suggest_categorical('splitter', ['best', 'random'])
        }

    def train_model(self, X_train: pd.DataFrame, y_train: pd.Series, params: dict):
        model = DecisionTreeRegressor(**params, random_state=42)
        model.fit(X_train, y_train)
        return model

