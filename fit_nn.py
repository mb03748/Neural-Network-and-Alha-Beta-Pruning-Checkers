from NN import NeuralNetwork as nn
import pandas as pd
import random


df = pd.read_csv('data.csv')

labels = df.iloc[:,-2].to_numpy() / df.iloc[:, -1].to_numpy()

data = df.iloc[:, :-2].to_numpy()

ind = int(0.7 * len(data))

trainX = data[:ind]
testX = data[ind:]
trainY = labels[:ind]
testY = labels[ind:]


def iiter(data, labels, n):
    indexes = [i for i in range(len(data))]
    random.shuffle(indexes)
    for i in range(0, len(data), n):
        d = data[indexes[i: min(len(data), i + n)]]
        l = labels[indexes[i: min(len(data), i + n)]]
        yield d,l


def error(y, y_pred):
    return ((y - y_pred) ** 2).mean()


def accuracy(y, y_pred):
	pred = y_pred.reshape(-1)
	a = (pred == y).mean()
	p = (y[pred == 1]).mean()
	r = (pred[y == 1]).mean()
	return a, p, r


lr = 0.003
inp = 8 * 8
hidden = 10
epoch = 10
batch_size = 32

n = nn(inp, hidden, lr)

for i in range(epoch):
	for X,y in iiter(trainX, trainY, batch_size):
		n.feedforward(X)
		n.Loss(y)
		n.backprop()

	n.feedforward(trainX)
	print("train loss\t", error(trainY, n.output))
	n.feedforward(testX)
	print("test loss\t", error(testY, n.output))
	print("measures: \t")


#n.tofile()
