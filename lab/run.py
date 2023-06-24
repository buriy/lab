import sys
from pathlib import Path
from typing import Union

from tqdm.auto import tqdm

from experiments.base import Experiment
from finder import find_classes_in_files, find_class_by_name
from lab.record import Record
from lab.store import Store


def list_experiments():
    root = Path(__file__).parent.parent / "experiments"
    return find_classes_in_files(root, Experiment)


class Trainer:
    def __init__(self):
        self.store = Store("../data/experiments.json")

    def run_experiment(self, exp_class: Union[str, Experiment]):
        if isinstance(exp_class, str):
            exp_class = find_class_by_name(exp_class)
            if not exp_class:
                print("No experiment:", exp_class)
        assert issubclass(exp_class, Experiment)
        experiment = exp_class()
        rec_train = Record('train', experiment, {})
        rec_test = Record('test', experiment, {})
        if self.store.has_record(rec_test):
            return
        rec_train.start()
        train_scores = experiment.train()
        rec_train.set_result(train_scores)
        self.store.add_result(rec_train)

        rec_test.start()
        test_scores = experiment.test()
        rec_test.set_result(test_scores)
        self.store.add_result(rec_test)

    def run(self, args):
        if not args or args == "all":
            args = [e[1] for e in list_experiments()]
        for arg in tqdm(args, desc='Experiments'):
            self.run_experiment(arg)


if __name__ == '__main__':
    Trainer().run(sys.argv[1:])
