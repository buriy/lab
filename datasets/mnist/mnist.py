import gzip
import os
from pathlib import Path
from typing import Union

import numpy as np

from datasets.data import SupervisedDataset, Task

import urllib.request
import os

# Define download URLs and file names
urls = [
    "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz",
    "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz",
    "http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz",
    "http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz",
]


def download(folder_path: Union[str, Path]):
    for url in urls:
        file_name = url.rsplit("/", 1)[-1]
        file_path = Path(folder_path, file_name)
        if not file_path.exists():
            print("Downloading MNIST from", url)
            file_path.parent.mkdir(exist_ok=True, parents=True)
            urllib.request.urlretrieve(url, file_path)


def load_mnist(path, kind="train"):
    """Загрузка датасета MNIST"""
    labels_path = os.path.join(path, f"{kind}-labels-idx1-ubyte.gz")
    images_path = os.path.join(path, f"{kind}-images-idx3-ubyte.gz")

    with gzip.open(labels_path, "rb") as lbpath:
        labels = np.frombuffer(lbpath.read(), dtype=np.uint8, offset=8)

    with gzip.open(images_path, "rb") as imgpath:
        images = np.frombuffer(imgpath.read(), dtype=np.uint8, offset=16).reshape(
            len(labels), 784
        )

    return images, labels


class MNIST(Task):
    DATA_PATH = "../data/mnist"

    def __init__(self):
        download(self.DATA_PATH)
        ds_train = SupervisedDataset(*load_mnist(self.DATA_PATH, kind="train"))
        ds_test = SupervisedDataset(*load_mnist(self.DATA_PATH, kind="t10k"))
        super().__init__(ds_train, ds_test)
