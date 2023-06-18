class Experiment:
    seed = 0

    def train(self):
        pass

    @property
    def name(self):
        return f"{self.__module__}.{self.__class__.__name__}"

    def test(self):
        pass

    def get_seed(self):
        return self.seed

    def get_scores(self):
        return {}
