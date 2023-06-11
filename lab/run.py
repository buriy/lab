import sys
from pathlib import Path
from typing import Union

from experiments.base import Experiment
from finder import find_classes_in_files, find_class_by_name
from lab.record import Record
from lab.store import Store


def list_experiments():
    root = Path(__file__).parent.parent / 'experiments'
    return find_classes_in_files(root, Experiment)


class Planner:
    def __init__(self):
        self.store = Store('../data/experiments.json')

    def run_experiment(self, exp_class: Union[str, Experiment]):
        if isinstance(exp_class, str):
            exp_class = find_class_by_name(exp_class)
            if not exp_class:
                print("No experiment:", exp_class)
        assert issubclass(exp_class, Experiment)
        exp = exp_class()
        rec = Record(exp, {})
        exp.train()
        exp.test()
        scores = exp.get_scores()
        rec.set_result(scores)
        self.store.add_result(rec)

    def run_multiple(self, *args):
        if not args or args == 'all':
            args = [e[1] for e in list_experiments()]
        for arg in args:
            self.run_experiment(arg)


if __name__ == '__main__':
    Planner().run_multiple(*sys.argv[1:])
