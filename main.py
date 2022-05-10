import numpy as np
from neural_network import Network
from layer import FCLayer, ActivationLayer, Layer


def mse(y_true, y_pred):
    return np.mean(np.power(y_true - y_pred, 2))


def mse_prime(y_true, y_pred):
    return 2 * (y_pred - y_true) / y_true.size


def tanh(x):
    return np.tanh(x)


def tanh_prime(x):
    return 1 - np.tanh(x) ** 2


if __name__ == '__main__':
    # training data
    x_train = np.array([[0, 1, 0],
                        [1, 0, 1],
                        [0, 1, 0]])
    y_train = np.array([[0, 1, 0],
                        [1, 0, 1],
                        [0, 1, 0]])
    # network
    net = Network()
    net.add(FCLayer(9, 2))
    net.add(ActivationLayer(tanh, tanh_prime))

    # train
    net.use(mse, mse_prime)
    net.fit(x_train, y_train, epochs=1000, learning_rate=0.1)

    # test
    out = net.predict(x_train)
    print(out)
