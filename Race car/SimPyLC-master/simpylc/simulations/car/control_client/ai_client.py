import time as tm
import sys as ss
import os
import socket as sc
import numpy as np
ss.path += [os.path.abspath(relPath) for relPath in ('..',)]

import socket_wrapper as sw
import parameters as pm

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

class AiClient:
    def __init__(self):
        self.steeringAngle = 0

        with open(pm.sampleFileName, 'w') as self.sampleFile:
            with sc.socket(*sw.socketType) as self.clientSocket:
                self.clientSocket.connect(sw.address)
                self.socketWrapper = sw.SocketWrapper(self.clientSocket)
                self.halfApertureAngle = False

                while True:
                    self.input()
                    self.lidarSweep()
                    self.output()
                    tm.sleep(0.02)

    def input(self):
        sensors = self.socketWrapper.recv()

        if not self.halfApertureAngle:
            self.halfApertureAngle = sensors['halfApertureAngle']
            self.sectorAngle = 2 * self.halfApertureAngle / pm.lidarInputDim
            self.halfMiddleApertureAngle = sensors['halfMiddleApertureAngle']

        if 'lidarDistances' in sensors:
            self.lidarDistances = sensors['lidarDistances']

    def lidarSweep(self):
        nearestObstacleDistance = pm.finity
        nearestObstacleAngle = 0

        nextObstacleDistance = pm.finity
        nextObstacleAngle = 0

        for lidarAngle in range(-self.halfApertureAngle, self.halfApertureAngle):
            lidarDistance = self.lidarDistances[lidarAngle]

            if lidarDistance < nearestObstacleDistance:
                nextObstacleDistance = nearestObstacleDistance
                nextObstacleAngle = nearestObstacleAngle

                nearestObstacleDistance = lidarDistance
                nearestObstacleAngle = lidarAngle

            elif lidarDistance < nextObstacleDistance:
                nextObstacleDistance = lidarDistance
                nextObstacleAngle = lidarAngle

        targetObstacleDistance = (nearestObstacleDistance + nextObstacleDistance) / 2
        print(targetObstacleDistance)

        self.steeringAngle = (nearestObstacleAngle + nextObstacleAngle) / 2
        self.targetVelocity = pm.getTargetVelocity(self.steeringAngle)

    def output(self):
        actuators = {
            'steeringAngle': self.steeringAngle,
            'targetVelocity': self.targetVelocity
        }

        self.socketWrapper.send(actuators)

if __name__ == '__main__':
    AiClient()

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