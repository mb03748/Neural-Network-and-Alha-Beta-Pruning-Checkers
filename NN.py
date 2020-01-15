import numpy as np
import pandas as pd


class NeuralNetwork:
	def __init__(self, layer1, layer2, lr):
		self.weights1 = np.random.normal(size=(layer1, layer2), scale = 0.01)
		self.weights2 = np.random.normal(size=(layer2, 1), scale = 0.01)
		self.bias1 = np.zeros(shape=(1, layer2))
		self.bias2 = np.zeros(shape=(1, 1))
		self.lr = lr


	def feedforward(self, x):
		self.input = x
		xW = np.dot(self.input, self.weights1)
		Z = xW + self.bias1
		self.layer1 = self.sigmoid(Z)
		self.output = self.sigmoid(np.dot(self.layer1, self.weights2) + self.bias2)


	def sigmoid(self, Z):
		return 1/(1+np.exp(-Z))


	def sigmoid_derivative(self, Z):
		s = 1/(1+np.exp(-Z))
		temp = s * (1-s)
		return temp


	def Loss(self, y_actual):
		self.y = y_actual.reshape(-1, 1)
		self.loss = y_actual - self.output


	def backprop(self):

		error_output = (self.y - self.output) * self.sigmoid_derivative(self.output)
		

		error_output = error_output / len(error_output)
		d_weights2 = np.dot(self.layer1.T, error_output)
		d_weights1 = np.dot(self.input.T,  (np.dot(error_output, self.weights2.T) * self.sigmoid_derivative(self.layer1)))

		d_bias2 = error_output.sum()
		d_bias1 = (np.dot(error_output, self.weights2.T) * self.sigmoid_derivative(self.layer1)).sum(axis = 0)
		
		self.weights1 = self.weights1 + d_weights1 * self.lr
		self.weights2 = self.weights2 + d_weights2 * self.lr

		self.bias1 = self.bias1 + d_bias1 * self.lr
		self.bias2 = self.bias2 + d_bias2 * self.lr


	def tofile(self):
		pd.DataFrame(self.weights1).to_csv('weights1.csv', index = False)
		pd.DataFrame(self.weights2).to_csv('weights2.csv', index = False)
		pd.DataFrame(self.bias1).to_csv('bias1.csv', index = False)
		pd.DataFrame(self.bias2).to_csv('bias2.csv', index = False)
		
	
	def readfile(self):
		self.weights1 = pd.read_csv('weights1.csv', header = 0).to_numpy()
		self.weights2 = pd.read_csv('weights2.csv', header = 0).to_numpy()
		self.bias1 = pd.read_csv('bias1.csv', header = 0).to_numpy()
		self.bias2 = pd.read_csv('bias2.csv', header = 0).to_numpy()
		
	
	def heuristic(self, state, maximizingPlayer, depth):
		newstate = []
		for i in state.state:
			for j in i:
				newstate.append(j)
		newstate = np.array(newstate).reshape(1, -1)
		self.feedforward(newstate)
		return self.output


