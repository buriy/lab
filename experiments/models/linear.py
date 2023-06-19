from sklearn.base import BaseEstimator
from sklearn.linear_model import LinearRegression, Ridge, Perceptron

from datasets.data import SupervisedDataset
from experiments.base import Model


class SKModel(Model):
    model: BaseEstimator

    def train(self, ds_train: SupervisedDataset):
        x_train, y_train = ds_train.as_lists()
        self.model.fit(x_train, y_train)
        return {}

    def predict(self, x_test: list):
        return self.model.predict(x_test)


class LinearModel(SKModel):
    def __init__(self, **opts):
        self.model = LinearRegression(**opts)


class RidgeModel(SKModel):
    def __init__(self, **opts):
        self.model = Ridge(**opts)


class PerceptronModel(SKModel):
    def __init__(self, **opts):
        self.model = Perceptron(**opts)
