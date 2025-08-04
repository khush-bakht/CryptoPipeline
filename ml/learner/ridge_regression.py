from sklearn.linear_model import Ridge
from .base_learner import BaseLearner
import optuna

class RidgeRegressionLearner(BaseLearner):
    def get_search_space(self, trial):
        return {
            'alpha': trial.suggest_float('alpha', 0.1, 10.0, log=True),
            'solver': trial.suggest_categorical('solver', ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga'])
        }
        
    def train_model(self, X_train, y_train, params):
        model = Ridge(**params)
        model.fit(X_train, y_train)
        return model