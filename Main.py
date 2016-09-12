import json
import sys
import random

from Environment import *
from SMA import *
from Agent import *
from View import *

class Main(object):
    """docstring for Main"""
    def __init__(self, nbParticles=None):
        super(Main, self).__init__()
        self.delay = data["delay"]
        if nbParticles != None:
            data["nbParticles"] = nbParticles
        self.createEnvironment()
        agentlist = []
        self.populate(agentlist)
        self.createSMA(agentlist)
        self.createWindow()
        self.createView()

    def createEnvironment(self):
        gridSizeX = data["gridSizeX"]
        gridSizeY = data["gridSizeY"]
        torus = data["torus"]

        self.environment = Environment(gridSizeX, gridSizeY, torus)

    def populate(self, agentlist):
        #Fetch data
        seed = data["seed"]
        nbParticles = data["nbParticles"]

        #Check if there is a given seed
        if seed == 0 or seed == "0" :
            #if not, create a random seed
            seed = random.randint(0, sys.maxsize)

        #Initialize the random engine with the seed
        random.seed(seed)

        #Fetch the free cells from the environment
        freeCells = self.environment.getFreeCells()

        #Check if there are enough cells for each particle
        if len(freeCells) < nbParticles :
            print("Error ! There are more particles than free cells !")
            return

        #Shuffle the list
        random.shuffle(freeCells)

        #Pop a free cell from the list then create and place an agent in this cell
        for i in range(nbParticles):
            position = freeCells.pop()
            self.createAgent(agentlist, position[0], position[1], i)

    def createAgent(self, agentlist, x, y, name):
        agent = Agent(self.environment, x, y, name, data["torus"], data["trace"])
        agentlist.append(agent)
        self.environment.setInCell(x, y, agent)

    def createSMA(self, agentlist):
        scheduling = data["scheduling"]
        nbTicks = data["nbTicks"]
        trace = data["trace"]

        self.SMA = SMA(self.environment, agentlist, scheduling, nbTicks, trace)

    def createWindow(self):
        self.window = Tk()
        self.window.title("S.M.A")
        self.canvas = Canvas(self.window, width = data["canvasSizeX"] + 1, height = data["canvasSizeY"] + 1, background = 'white', bd=0, highlightthickness=0, relief='ridge')
        self.canvas.pack()

    def createView(self):
        boxSize = data["boxSize"]

        if boxSize == 0 :
            boxSize = min(data["canvasSizeX"], data["canvasSizeY"]) / max(data["gridSizeY"], data["gridSizeX"])

        self.view = View(self.window, self.canvas, data["gridSizeX"], data["gridSizeY"], boxSize, data["grid"], data["refresh"])
        self.SMA.addObserver(self.view)

    def run(self):
        self.SMA.emitSignal("modelCreated")
        self.window.after(self.delay, self.update)
        self.window.mainloop()

    def update(self):
        if self.SMA.hasFinished() and data["autoquit"]:
            self.SMA.emitSignal("destroy")
        else:
            self.SMA.run()
            self.view.updateParticles()
            self.window.after(self.delay, self.update)

def loadPropertiesFromJSON(fileName):
    global data
    dataFile = open(fileName, 'r')
    try:
        data = json.loads(dataFile.read())
    finally:
        dataFile.close()

def main():
    loadPropertiesFromJSON("properties.json")
    if data["profile"]:
        profile()
    else:
        run()

def profile():
    nbParticles = data["nbParticles"]
    for i in range(1, nbParticles):
        startTime = time.clock()
        main = Main(nbParticles=i)
        main.run()
        endTime = time.clock()
        executionTime = endTime - startTime
        print("%5f seconds for %d particles" % (executionTime, i))

def run():
    main = Main()
    main.run()

if __name__ == '__main__':
    main()
