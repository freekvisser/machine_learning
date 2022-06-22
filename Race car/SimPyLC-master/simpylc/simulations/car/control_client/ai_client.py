import time as tm
import sys as ss
import os
import socket as sc
import numpy as np
ss.path += [os.path.abspath(relPath) for relPath in ('..',)]

import socket_wrapper as sw
import parameters as pm

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