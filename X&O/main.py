import numpy as np
from neural_network import Network
from layer import FCLayer, ActivationLayer


def loss(y_true, y_pred):
    return np.mean(np.power(y_true - y_pred, 2))


def loss_prime(y_true, y_pred):
    return 2 * (y_pred - y_true) / y_true.size


def activation(x):
    return np.tanh(x)


def activation_prime(x):
    return 1 - np.tanh(x) ** 2


if __name__ == '__main__':
    # training data
    in_train = np.array([[[0, 1, 0,
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
    out_train = np.array([[[0]],
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
    net.add_layer(FCLayer(9, 3))
    net.add_layer(ActivationLayer(activation, activation_prime))
    net.add_layer(FCLayer(3, 1))
    net.add_layer(ActivationLayer(activation, activation_prime))

    # train
    net.create_loss(loss, loss_prime)
    net.train_network(in_train, out_train, cycles=1000, learning_rate=0.1)

    # test
    out = net.get_output(test_cross)
    print(out)
