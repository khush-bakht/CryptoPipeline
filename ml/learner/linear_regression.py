from sklearn.linear_model import LinearRegression
from ml.learner.base_learner import BaseLearner

class LinearRegressionLearner(BaseLearner):
    def __init__(self, symbol, time_horizon, model_name):
        super().__init__(symbol, time_horizon, model_name)

    def get_search_space(self, trial):
        return {}

    def train_model(self, X_train, y_train, params):
        model = LinearRegression()
        model.fit(X_train, y_train)
        return model
