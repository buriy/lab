import numpy as np


class Vectorizer:
    def __init__(self):
        pass

    def transform(self, x):
        return x


class Trainer:
    def __init__(self, model, optimizer, criterion):
        self.model = model
        self.optimizer = optimizer
        self.criterion = criterion

    def train_step(self, x, y):
        self.model.zero_grad()
        y_pred = self.model.forward(x)
        loss = self.criterion.forward(y_pred, y)
        dLdy = self.criterion.backward(y_pred, y)
        self.model.backward(dLdy)
        self.optimizer.step()
        return loss


class Net:
    def __init__(self, input_size, output_size):
        self.weights = np.random.randn(input_size, output_size) * np.sqrt(2 / (input_size + output_size))
        self.bias = np.zeros(output_size)
        self.inputs = None

    def forward(self, x):
        self.inputs = x
        return np.dot(x, self.weights) + self.bias

    def backward(self, dLdy):
        dLdW = np.dot(self.inputs.T, dLdy)
        dLdx = np.dot(dLdy, self.weights.T)
        self.weights -= self.optimizer.lr * dLdW
        self.bias -= self.optimizer.lr * np.sum(dLdy, axis=0)
        return dLdx


class Evaluator:
    def __init__(self, model, criterion):
        self.model = model
        self.criterion = criterion

    def evaluate(self, dataloader):
        total_loss = 0.0
        total_correct = 0

        for batch in dataloader:
            x, y = [np.array(b) for b in zip(*batch)]
            y_pred = self.model.forward(x)
            loss = self.criterion.forward(y_pred, y)
            total_loss += loss.item()
            total_correct += np.sum(np.argmax(y_pred, axis=1) == y)

        return {'loss': total_loss / len(dataloader), 'accuracy': total_correct / len(dataloader.dataset)}


class Logger:
    def __init__(self, epochs):
        self.epochs = epochs

    def log(self, epoch, loss, train_acc=None, val_acc=None):
        print(f'Epoch {epoch}/{self.epochs} | Train Loss: {loss:.4f}', end=' ')
        if train_acc is not None:
            print(f'| Train Acc: {train_acc:.2%}', end=' ')
        if val_acc is not None:
            print(f'| Val Acc: {val_acc:.2%}')
        else:
            print()
