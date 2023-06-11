import hashlib
import json
import time
from dataclasses import dataclass
from typing import Union


def get_hash(obj):
    h = hashlib.md5()
    j = json.dumps(obj, ensure_ascii=False, sort_keys=True)
    h.update(str(j).encode())
    return h.digest().hex()[:12]


@dataclass
class Record:
    """
    Experiments are entities that store task info and task results
    Experiments can be compared, and skipped if the same experiment was done already
    """
    opts: dict
    task: str
    seed: str
    hash: str
    time_start: float
    time_spent: Union[float, None]
    metrics: dict

    def __init__(self, task, opts):
        self.metrics = {}
        self.task = task.name
        self.opts = opts
        self.seed = task.get_seed()
        self.hash = get_hash({
            'task': self.task,
            'seed': self.seed,
            'opts': opts,
        })
        self.time_start = time.time()
        self.time_spent = 0

    def set_result(self, metrics: dict):
        self.time_spent = time.time() - self.time_start
        self.metrics = metrics

    def json(self):
        return {k: v for k, v in self.__dict__.items() if k[:1] != '_'}
