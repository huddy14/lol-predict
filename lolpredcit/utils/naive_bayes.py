import csv
import os
from enum import Enum

from sklearn.naive_bayes import GaussianNB


class Data(Enum):
    DEFAULT = 0
    SUMMARIZED = 1
    MULTIPLIED = 2


class NBClassifier:
    def __init__(self, data_type):
        self.clf = GaussianNB()
        self.data_type = data_type
        data = _handle_data(data_type)
        self.data = data
        self.total_size = data['total_size']
        self.training_size = data['split_size']
        self.test_size = self.total_size - self.training_size
        self.clf.fit(data['train_x'], data['train_y'])
        self.score = self.clf.score(data['test_x'], data['test_y'])


def _handle_data(data, path=os.getcwd() + '/database/matchData', split_ratio=.7):
    X = []
    Y = []
    for line in _read_lines(path):
        Y.append(line[-1])
        if data == Data.DEFAULT:
            X.append(line[:-1])
        else:
            x = []
            for i in range(0, len(line) - 1, 4):
                if data == Data.SUMMARIZED:
                    x.append(line[i + 1])
                elif data == Data.MULTIPLIED:
                    x.append(line[i + 1] * line[i + 2])
                i += 4
                if i >= len(line) - 1: break
            blue = sum(x[:5])
            red = sum(x[5:])

            X.append([blue, red])

    return _split_to_test_and_training_sets(X, Y, split_ratio)


def _read_lines(trainingset_path):
    with open(trainingset_path, 'r') as data:
        reader = csv.reader(data)
        # skipping headers
        next(reader)

        for line in reader:
            yield [float(i) for i in line]


def _split_to_test_and_training_sets(X, Y, ratio):
    size = len(Y)
    if len(X) == size:
        split = int(size * ratio)
        return {
            'train_x': X[:split], 'train_y': Y[:split],  # training data sets
            'test_x': X[split:], 'test_y': Y[split:],  # test data sets
            'total_size': size, 'split_size': split  # sizes
        }


def generate_plot():
    pass


bayes = {data: NBClassifier(data) for data in Data}
print(bayes[Data.DEFAULT].score)
