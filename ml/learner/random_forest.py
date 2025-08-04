from sklearn.ensemble import RandomForestRegressor
from .base_learner import BaseLearner
import optuna

class RandomForestLearner(BaseLearner):
    def get_search_space(self, trial):
        return {
            'n_estimators': trial.suggest_int('n_estimators', 50, 500),
            'max_depth': trial.suggest_int('max_depth', 3, 20),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10),
            'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2', None]),
            'bootstrap': trial.suggest_categorical('bootstrap', [True, False])
        }

    def train_model(self, X_train, y_train, params):
        model = RandomForestRegressor(
            **params,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)
        return model

