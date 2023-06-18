from datasets.mnist.mnist import MNIST
from experiments.base import Experiment


class Linear(Experiment):
    ds = MNIST()
    seed = 0

    def train(self):
        pass

    def test(self):
        pass

    def get_scores(self):
        return {}
