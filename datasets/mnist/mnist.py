import gzip
import os

import numpy as np

from datasets.data import SupervisedDataset, Task


def download(path):
    # FIXME
    os.makedirs(path)


def load_mnist(path, kind='train'):
    """Загрузка датасета MNIST"""
    labels_path = os.path.join(path, '{}-labels-idx1-ubyte.gz'.format(kind))
    images_path = os.path.join(path, '{}-images-idx3-ubyte.gz'.format(kind))

    with gzip.open(labels_path, 'rb') as lbpath:
        labels = np.frombuffer(lbpath.read(), dtype=np.uint8, offset=8)

    with gzip.open(images_path, 'rb') as imgpath:
        images = np.frombuffer(imgpath.read(), dtype=np.uint8, offset=16).reshape(len(labels), 784)

    return images, labels


class MNIST(Task):
    def __init__(self):
        ds_train = SupervisedDataset(*load_mnist('data/mnist', kind='train'))
        ds_test = SupervisedDataset(*load_mnist('data/mnist', kind='t10k'))
        super().__init__(ds_train, ds_test)
