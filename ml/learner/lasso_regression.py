from sklearn.linear_model import Lasso
from .base_learner import BaseLearner
import optuna

class LassoRegressionLearner(BaseLearner):
    def get_search_space(self, trial):
        return {
            'alpha': trial.suggest_float('alpha', 0.0001, 1.0, log=True),
            'selection': trial.suggest_categorical('selection', ['cyclic', 'random'])
        }
        
    def train_model(self, X_train, y_train, params):
        model = Lasso(**params)
        model.fit(X_train, y_train)
        return model