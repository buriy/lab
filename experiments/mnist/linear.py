from datasets.mnist.mnist import MNIST
from experiments.base import Experiment
from experiments.models.linear import LinearModel, RidgeModel, PerceptronModel


class MNISTLinear(Experiment):
    seed = 0
    opts = {

    }

    def __init__(self):
        self.task = MNIST()
        self.model = LinearModel(**self.opts)


class MNISTRidge(Experiment):
    seed = 0
    opts = {
        'alpha': 1
    }

    def __init__(self):
        self.task = MNIST()
        self.model = RidgeModel(**self.opts)


class MNISTPerceptron(Experiment):
    seed = 0
    opts = {

    }

    def __init__(self):
        self.task = MNIST()
        self.model = PerceptronModel(**self.opts)
