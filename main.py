import numpy as np
from neural_network import Network
from layer import FCLayer, ActivationLayer


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
    x_train = np.array([[[0, 1, 0,
                          1, 0, 1,
                          0, 1, 0]],
                        [[1, 0, 1,
                          0, 1, 0,
                          1, 0, 1]],
                        [[0, 1, 0,
                          1, 0, 1,
                          0, 1, 0]],
                        [[1, 0, 1,
                          0, 1, 0,
                          1, 0, 1]]])
    y_train = np.array([[[0]],
                        [[1]],
                        [[0]],
                        [[1]]])

    test_cross = np.array([[[0, 1, 0,
                             1, 0, 1,
                             0, 1, 0],
                            [1, 0, 1,
                             0, 1, 0,
                             1, 0, 1]]])
    # network
    net = Network()
    net.add(FCLayer(9, 3))
    net.add(ActivationLayer(tanh, tanh_prime))
    net.add(FCLayer(3, 1))
    net.add(ActivationLayer(tanh, tanh_prime))

    # train
    net.use(mse, mse_prime)
    net.fit(x_train, y_train, epochs=1000, learning_rate=0.1)

    # test
    out = net.predict(test_cross)
    print(out)
