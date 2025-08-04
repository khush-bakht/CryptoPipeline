from sklearn.neural_network import MLPRegressor
from .base_learner import BaseLearner
import optuna
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

class MLPRegressorLearner(BaseLearner):
    def get_search_space(self, trial):
        return {
            'mlp__hidden_layer_sizes': trial.suggest_categorical('mlp__hidden_layer_sizes', 
                [(50,), (100,), (50, 50), (100, 50), (100, 100)]),
            'mlp__activation': trial.suggest_categorical('mlp__activation', ['relu', 'tanh', 'logistic']),
            'mlp__alpha': trial.suggest_float('mlp__alpha', 0.0001, 0.1, log=True),
            'mlp__learning_rate': trial.suggest_categorical('mlp__learning_rate', ['constant', 'invscaling', 'adaptive']),
            'mlp__learning_rate_init': trial.suggest_float('mlp__learning_rate_init', 0.001, 0.1, log=True),
            'mlp__batch_size': trial.suggest_categorical('mlp__batch_size', [32, 64, 128, 256]),
            'mlp__max_iter': trial.suggest_int('mlp__max_iter', 100, 500),
            'mlp__early_stopping': trial.suggest_categorical('mlp__early_stopping', [True, False])
        }

    def train_model(self, X_train, y_train, params):
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('mlp', MLPRegressor(random_state=42))
        ])
        pipeline.set_params(**params)
        pipeline.fit(X_train, y_train)
        return pipeline

