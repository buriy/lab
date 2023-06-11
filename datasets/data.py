import random
from typing import Collection, Union, Sequence, Mapping

from sklearn.model_selection import train_test_split


class Dataset:
    data: Union[Sequence, Mapping]

    def __init__(self, data: Union[Sequence, Mapping]):
        self.data = data

    def __len__(self):
        return len(self.data)

    @property
    def indices(self):
        if isinstance(self.data, dict):
            return list(self.data.keys())
        else:
            return list(range(len(self.data)))

    def __getitem__(self, idx):
        return self.data[idx]


class SupervisedDataset(Dataset):
    labels: list

    def __init__(self, data: list, labels: list):
        super().__init__(data)
        self.labels = labels

    def split(self, test_size):
        xy = (self.data, self.labels)
        x1, y1, x2, y2 = train_test_split(xy, test_size=test_size)
        return SupervisedDataset(x1, y1), SupervisedDataset(x2, y2)


class Task:
    ds_train: SupervisedDataset
    ds_test: SupervisedDataset

    def __init__(self, ds_train, ds_test):
        self.ds_train = ds_train
        self.ds_test = ds_test


class DataLoader:
    def __init__(self, dataset: Dataset, batch_size: int, shuffle: bool = False):
        self.dataset = dataset
        self.batch_size = batch_size
        self.shuffle = shuffle

    def __iter__(self):
        indices = self.dataset.indices
        if self.shuffle:
            random.shuffle(indices)

        for start_idx in range(0, len(indices), self.batch_size):
            end_idx = min(start_idx + self.batch_size, len(indices))
            batch_indices = indices[start_idx:end_idx]
            yield [self.dataset[idx] for idx in batch_indices]
