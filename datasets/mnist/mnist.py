import gzip
import os
import urllib.request
from pathlib import Path
from typing import Union

import numpy as np
from sklearn.metrics import accuracy_score

from datasets.data import SupervisedDataset, Task

# Define download URLs and file names
urls = [
    "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz",
    "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz",
    "http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz",
    "http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz",
]


def download_mnist(folder_path: Union[str, Path]):
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
    metrics = {'accuracy': accuracy_score}

    def __init__(self):
        download_mnist(self.DATA_PATH)
        self.ds_train = SupervisedDataset(*load_mnist(self.DATA_PATH, kind="train"))
        self.ds_test = SupervisedDataset(*load_mnist(self.DATA_PATH, kind="t10k"))

#
# class CIFAR10:
#     def __init__(self):
#         from tensorflow.keras.datasets import cifar10
#         (x_train, y_train), (x_test, y_test) = cifar10.load_data()
#         self.ds_train = (x_train.reshape((50000, 3072)), y_train.ravel())
#         self.ds_test = (x_test.reshape((10000, 3072)), y_test.ravel())
#         self.metrics = [accuracy_score]
#
#
# class SVHN:
#     def __init__(self):
#         from scipy.io import loadmat
#         train = loadmat('train_32x32.mat')
#         test = loadmat('test_32x32.mat')
#         self.ds_train = (train['X'].reshape((73257, 3072)), train['y'].ravel() % 10)
#         self.ds_test = (test['X'].reshape((26032, 3072)), test['y'].ravel() % 10)
#         self.metrics = [accuracy_score]
