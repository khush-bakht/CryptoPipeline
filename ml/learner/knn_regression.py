from sklearn.neighbors import KNeighborsRegressor
from .base_learner import BaseLearner
import optuna
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

class KNNRegressionLearner(BaseLearner):
    def get_search_space(self, trial):
        return {
            'knn__n_neighbors': trial.suggest_int('knn__n_neighbors', 3, 50),
            'knn__weights': trial.suggest_categorical('knn__weights', ['uniform', 'distance']),
            'knn__p': trial.suggest_int('knn__p', 1, 2),  
            'knn__algorithm': trial.suggest_categorical('knn__algorithm', ['auto', 'ball_tree', 'kd_tree', 'brute'])
        }

    def train_model(self, X_train, y_train, params):
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('knn', KNeighborsRegressor())
        ])
        pipeline.set_params(**params)
        pipeline.fit(X_train, y_train)
        return pipeline
