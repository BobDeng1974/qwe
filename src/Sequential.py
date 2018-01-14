from src.Activation import Activation
from src.BasicNN import BasicNN
from src.LostFunction import LostFunction
from src.Optimizer import Optimizer
import numpy as np

class Sequential(object):
    def __init__(self, layers=None):
        self.layers = []
        for layer in layers:
            self.add(layer)

    def add(self, layer):
        if self.layers == []:
            if layer.input_size == 0:
                raise Exception('must define input data size')
        else:
            last_layer = self.layers[-1]
            layer.set_input_size(last_layer.node_size)
        self.layers.append(layer)

    def compile(self, loss='cross_entropy', optimizer='sgd'):
        self.loss = LostFunction.cross_entropy
        self.loss_der = LostFunction.cross_entropy_derivative
        self.optimizer = Optimizer.BGD

    def calc_lost(self, y_label):
        return self.loss(self.layers[-1].data_forward, y_label)

    def fit(self,x_train, y_train, epochs=10, learning_rate=0.01, batch_size=32):
        self.optimizer(x_train,y_train,self,epochs,learning_rate,batch_size)

    def predict(self, x_test):
        return self.forward(x_test)

    def forward(self, input_data):
        input_data_ = input_data
        for layer in self.layers:
            input_data = layer.forward(input_data)
        return input_data
    def backward(self,y_train, learning_rate):
        m = y_train.shape[0]
        dA = self.loss_der(self.layers[-1].data_forward, y_train)
        layer_len = len(self.layers)

        for idx in range(layer_len-2,-1,-1):
            cur_layer = self.layers[idx]
            grad_W, grad_b, dA = cur_layer.backward(dA)
            # print(idx, 'cur_layer_W:',cur_layer.W)
            # print(idx, 'cur_layer_b:',cur_layer.b)
            cur_layer.W = cur_layer.W - learning_rate * grad_W
            cur_layer.b = cur_layer.b - learning_rate * grad_b

if __name__ == '__main__':

    TEST_DIM = 2
    TEST_DATA_SIZE = 1000
    TEST_DATA_TRAIN = int(TEST_DATA_SIZE * 0.8)
    TEST_THRESHOLD = 0.98
    seq = Sequential([BasicNN(4,input_size=TEST_DIM), Activation(), BasicNN(1,1), Activation('sigmoid')])
    seq.compile()
    np.random.seed(10)
    x_train = np.random.rand(100,TEST_DIM)
    y_train = np.zeros((x_train.shape[0],1))
    y_train[(x_train[:, 0] < 0.5) & (x_train[:, 1] < 0.5)] = 1

    # print('y_train:\n',y_train)
    # print('x_train:\n',x_train)

    # seq.forward(x_train)
    # print('W[0]:',seq.layers[0].W)
    # print('b[0]:',seq.layers[0].b)
    # print('W[1]:',seq.layers[1].W)
    # print('b[1]:',seq.layers[1].b)
    # output = seq.layers[-1].data_forward
    # print('forward:',output)   # forward success
    # backward = seq.backward(output,0.2)
    # print('backward:',backward)
    #
    seq.fit(x_train[:TEST_DATA_TRAIN], y_train[:TEST_DATA_TRAIN],10,0.1)
    output = seq.predict(x_train[:10])
    print(y_train[:10],output)
    # print(seq.predict(x_train[TEST_DATA_TRAIN:]))
    # print(seq.predict(x_train[TEST_DATA_TRAIN:]) > TEST_THRESHOLD)
    # print(y_train[TEST_DATA_TRAIN:])
