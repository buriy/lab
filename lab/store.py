import hashlib
import json
from pathlib import Path

from lab.record import Record


def get_hash(obj):
    h = hashlib.md5()
    j = json.dumps(obj, ensure_ascii=False, sort_keys=True)
    h.update(str(j).encode())
    return h.digest().hex()[:12]


class Store:
    def __init__(self, fn):
        self.fn = fn
        self.db = None

    def add_result(self, rec: Record):
        self._load()
        self.db[rec.hash] = rec.json()
        self._save()

    def results(self):
        self._load()
        db = json.loads(Path(self.fn).read_text())
        return db.items()

    def _load(self):
        if self.db is None:
            fpath = Path(self.fn)
            if not fpath.exists():
                print("Creating new empty experiments DB:", fpath)
                self.db = {}
            else:
                self.db = json.loads(Path(self.fn).read_text())

    def _save(self):
        dump = json.dumps(self.db, indent=2, ensure_ascii=False)
        Path(self.fn).parent.mkdir(exist_ok=True, parents=True)
        Path(self.fn).write_text(dump, encoding='utf-8')
