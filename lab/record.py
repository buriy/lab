import hashlib
import json
import time
from typing import Union

from experiments.base import Experiment


def get_hash(obj):
    h = hashlib.md5()
    j = json.dumps(obj, ensure_ascii=False, sort_keys=True)
    h.update(j.encode())
    return h.digest().hex()[:12]


class Record:
    """
    Experiments are entities that store task info and task results
    Experiments can be compared, and skipped if the same experiment was done already
    """
    kind: str
    opts: dict
    task: str
    seed: str
    hash: str
    time_start: float
    time_spent: Union[float, None]
    metrics: dict

    def __init__(self, kind, task: Experiment, opts):
        self.metrics = {}
        self.kind = kind
        self.task = task.name
        self.opts = opts
        self.seed = task.get_seed()
        self.hash = get_hash(
            {
                "task": self.task,
                "kind": self.kind,
                "seed": self.seed,
                "opts": opts,
            }
        )
        self.time_start = time.time()
        self.time_spent = 0

    def set_result(self, metrics: dict):
        self.time_spent = time.time() - self.time_start
        self.metrics = metrics
        print(f"Running {self.kind:5s}", 'on', self.task, f'took {self.time_spent:6.3f}', '=>', metrics)

    def json(self):
        return {k: v for k, v in self.__dict__.items() if k[:1] != "_"}

    def start(self):
        self.time_start = time.time()
