from datasets.data import Dataset, Task


class Model:
    def train(self, ds_train: Dataset) -> dict:
        return {}

    def predict(self, x_test: list):
        return 0


class Experiment:
    model: Model
    task: Task
    opts: dict = {}
    seed: int = 0

    @property
    def name(self):
        return f"{self.__module__}.{self.__class__.__name__}"

    def get_seed(self):
        return self.task.get_seed()

    def train(self) -> dict:
        metrics = {
            'size': len(self.task.ds_train)
        }
        metrics.update(self.model.train(self.task.ds_train))
        return metrics

    def test(self) -> dict:
        x_test, y_test = self.task.ds_test.as_lists()
        y_pred = self.model.predict(x_test)
        scores = {
            'size': len(y_test)
        }
        for name, metric in self.task.metrics.items():
            scores[name] = metric(y_test, [round(y) for y in y_pred])
        return scores
