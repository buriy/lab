import random
from typing import Union, Sequence, Mapping, List, Callable, Dict

from sklearn.model_selection import train_test_split


class Dataset:
    data: dict

    def __init__(self, data: Union[Sequence, Mapping]):
        if not isinstance(data, Mapping):
            data = dict(enumerate(data))
        self.data = data

    def __len__(self):
        return len(self.data)

    def keys(self):
        return self.data.keys()

    def labeled(self):
        return []

    def __getitem__(self, idx):
        return self.data[idx]


class SupervisedDataset(Dataset):
    labels: dict

    def __init__(self, data: list, labels: list):
        super().__init__(data)
        self.labels = dict(enumerate(labels))

    def labeled(self):
        return self.labels.keys()

    def as_lists(self):
        return [self[k] for k in self.labeled()], [self.labels[k] for k in self.labeled()]

    def __iter__(self):
        for k in self.labeled():
            yield self[k], self.labels[k]

    def split(self, test_size):
        xy = (self.data, self.labels)
        x1, y1, x2, y2 = train_test_split(xy, test_size=test_size)
        return SupervisedDataset(x1, y1), SupervisedDataset(x2, y2)


class Task:
    ds_train: SupervisedDataset
    ds_test: SupervisedDataset
    seed: int = 0
    metrics: Dict[str, Callable]

    def get_seed(self):
        return self.seed


class DataLoader:
    def __init__(self, dataset: Dataset, seed: int, batch_size: int, shuffle: bool = False):
        self.dataset = dataset
        self.batch_size = batch_size
        self.shuffle = shuffle
        self._seed = seed

    def __iter__(self):
        indices = self.dataset.indices
        if self.shuffle:
            random.seed(self._seed)
            self._seed = random.random()
            random.shuffle(indices)

        for start_idx in range(0, len(indices), self.batch_size):
            end_idx = min(start_idx + self.batch_size, len(indices))
            batch_indices = indices[start_idx:end_idx]
            yield [self.dataset[idx] for idx in batch_indices]
