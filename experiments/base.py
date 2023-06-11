class Experiment:
    def train(self):
        pass

    @property
    def name(self):
        return self.__module__ + '.' + self.__class__.__name__

    def test(self):
        pass

    def get_seed(self):
        return 0

    def get_scores(self):
        return {
        }
