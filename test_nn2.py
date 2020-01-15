from NN import NeuralNetwork as nn
import numpy as np

n = nn(3,2, 0.8)

n.weights1 = np.array([[0.35, 0],[0.15, -0.1],[-0.2, 0.2]])
n.weights2 = np.array([[0.4],[0.25]])
n.bias1 = np.array([0,0]).reshape(1,2)
n.bias2 = np.array([0]).reshape(1,1)
n.lr = 0.8

x = np.array([0.5,0.3,0.9]).reshape(1,3)

n.feedforward(x)
n.Loss(0.8)
n.backprop()

print(n.weights2)
print(n.weights1)