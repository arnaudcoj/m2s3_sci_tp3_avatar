from Agent import *
from Observer import *

class Hunter(Agent):
    """docstring for Hunter."""
    def __init__(self, environment, posX, posY, name):
        super(Hunter, self).__init__(environment, posX, posY, name)
        self.avatarFollower = AvatarFollower()
        self.color = "Red"
        self.tick = 0

    def decide(self):
        speedHunter = self.environment.data["speedHunter"]
        if (self.tick % speedHunter) == 0:
            targetX = self.posX
            targetY = self.posY
            matrix = self.avatarFollower.dijkstraMatrix

            if self.avatarFollower.dijkstraMatrix != None :
                for cell in self.environment.getMooreNeighbors(self.posX, self.posY):
                    x = cell[0]
                    y = cell[1]

                    if matrix[x][y] == 0:
                        raise NotImplementedError("end of the game, to be implemented")

                    if matrix[targetX][targetY] == None or (matrix[x][y] != None and matrix[x][y] < matrix[targetX][targetY]):
                        targetX = x
                        targetY = y

            self.pasX = targetX - self.posX
            self.pasY = targetY - self.posY

    def update(self):
        speedHunter = self.environment.data["speedHunter"]
        if (self.tick % speedHunter) == 0:
            self.move()
        self.tick += 1

class AvatarFollower(Observer):
    """docstring for AvatarFollower."""
    def __init__(self):
        super(AvatarFollower, self).__init__()
        self.dijkstraMatrix = None
        self.signalFunc = {"avatarUpdated":self.onAvatarUpdated}

    def onAvatarUpdated(self, avatar):
        self.dijkstraMatrix = avatar.dijkstraMatrix
