from sklearn.svm import SVR
from .base_learner import BaseLearner
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import optuna


class SVRLearner(BaseLearner):
    def get_search_space(self, trial):
        kernel = trial.suggest_categorical('svr__kernel', ['linear', 'poly', 'rbf'])

        params = {
            'svr__C': trial.suggest_float('svr__C', 0.1, 10, log=True),
            'svr__epsilon': trial.suggest_float('svr__epsilon', 0.01, 1),
            'svr__kernel': kernel,
        }

        if kernel == 'rbf':
            params['svr__gamma'] = trial.suggest_float('svr__gamma', 0.01, 1, log=True)
        else:
            params['svr__gamma'] = 'auto'

        if kernel == 'poly':
            params['svr__degree'] = trial.suggest_int('svr__degree', 2, 5)
        else:
            params['svr__degree'] = 3  

        return params

    def train_model(self, X_train, y_train, params):
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('svr', SVR())
        ])
        pipeline.set_params(**params)
        pipeline.fit(X_train, y_train)
        return pipeline
