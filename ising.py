import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Spin(object):

    def __init__(self, dimensions, T, iterations):
        self.iterations = iterations
        self.dimensions = dimensions
        self.T = T
        self.spins = np.zeros((self.dimensions,self.dimensions))
        self.setInitialStates()
        self.alteredCopy = np.zeros((self.dimensions,self.dimensions))
        self.magVar = np.array(())
        self.testVar = 0

    def setInitialStates(self):
        for i in range(0,self.dimensions):
            for j in range(self.dimensions):
                if np.random.uniform(0,1)>=0.5:
                    self.spins[i,j] = 1
                else:
                    self.spins[i,j] = -1


    def NNsum(self, pos, x,y):
        sum = 0
        sum+= pos*self.spins[(x+1)%self.dimensions, y]
        sum+= pos*self.spins[(x-1)%self.dimensions, y]
        sum+= pos*self.spins[x,(y+1)%self.dimensions]
        sum+= pos*self.spins[x, (y-1)%self.dimensions]
        return sum*-1



    def makeAlteredCopy(self):
        for i in range(0,self.dimensions):
            for j in range(self.dimensions):
                    self.alteredCopy[i,j] = self.spins[i,j]
        index = np.random.randint(0,self.dimensions,2)
        self.alteredCopy[index[0],index[1]] = self.alteredCopy[index[0],index[1]]*-1
        return index

    def changeOriginal(self, index):
        self.spins[index[0],index[1]] = self.spins[index[0],index[1]]*-1


    def change(self, i):
        for i in range(self.dimensions*self.dimensions):
            index = np.random.randint(0,self.dimensions,2)
            diff = self.NNsum(-1*self.spins[index[0],index[1]],index[0],index[1])-self.NNsum(self.spins[index[0],index[1]],index[0],index[1])
            if diff<0:
                self.changeOriginal(index)
            else:
                p = np.exp((-1*diff)/self.T)
                if np.random.uniform(0,1)<p:
                    self.changeOriginal(index)
        self.testVar+=1
        if self.testVar%100 ==0 or (self.testVar>100 and self.testVar%10==0):
            self.magVar = np.append(self.magVar,[self.magnetization()])
        self.im = plt.imshow(self.spins, cmap='winter', interpolation='nearest')
        return [self.im]

    def changeNoAnim(self):
        for j in range(self.iterations):
            for i in range(self.dimensions*self.dimensions):
                index = np.random.randint(0,self.dimensions,2)
                diff = self.NNsum(-1*self.spins[index[0],index[1]],index[0],index[1])-self.NNsum(self.spins[index[0],index[1]],index[0],index[1])
                if diff<0:
                    self.changeOriginal(index)
                else:
                    p = np.exp((-1*diff)/self.T)
                    if np.random.uniform(0,1)<p:
                        self.changeOriginal(index)
            self.testVar+=1
            if self.testVar%100 ==0 or (self.testVar>100 and self.testVar%10==0):
                self.magVar = np.append(self.magVar,[self.magnetization()])



    def run(self, anim):
        if anim ==True:
            fig, ax = plt.subplots()
            self.im=plt.imshow(self.spins, cmap='winter', interpolation='nearest')
            anim = FuncAnimation(fig, self.change, init_func = self.init, frames = self.iterations, repeat = False, interval = 1, blit = True)
            plt.show()
        else:
            self.changeNoAnim()
        self.getAvrgMag()


    def init(self):
        return [self.im]

    def kawasakiTest(self, index1, index2):
        if abs(index1[0]-index2[0])>1 or abs(index1[1]-index2[1])>1:
            diff1 = self.NNsum(-1*self.spins[index1[0],index1[1]],index1[0],index1[1])-self.NNsum(self.spins[index1[0],index1[1]],index1[0],index1[1])
            diff2 = self.NNsum(-1*self.spins[index2[0],index2[1]],index2[0],index2[1])-self.NNsum(self.spins[index2[0],index2[1]],index2[0],index2[1])
            diff = diff1+diff2
        elif np.array_equal(index1,index2)==True:
            diff = self.NNsum(-1*self.spins[index1[0],index1[1]],index1[0],index1[1])-self.NNsum(self.spins[index1[0],index1[1]],index1[0],index1[1])
        else:
            self.changeOriginal(index2)
            diff1 = self.NNsum(-1*self.spins[index1[0],index1[1]],index1[0],index1[1])-self.NNsum(self.spins[index1[0],index1[1]],index1[0],index1[1])
            self.changeOriginal(index2)
            self.changeOriginal(index1)
            diff2 = self.NNsum(-1*self.spins[index2[0],index2[1]],index2[0],index2[1])-self.NNsum(self.spins[index2[0],index2[1]],index2[0],index2[1])
            self.changeOriginal(index1)
            diff = diff1+diff2
        return diff

    def kawasaki(self, i):
        for j in range(self.dimensions*self.dimensions):
            index1 = np.random.randint(0,self.dimensions,2)
            index2 = np.random.randint(0,self.dimensions,2)
            diff = self.kawasakiTest(index1,index2)
            if diff<0:
                self.changeOriginal(index1)
                self.changeOriginal(index2)
            else:
                p = np.exp((-1*diff)/self.T)
                if np.random.uniform(0,1)<p:
                    self.changeOriginal(index1)
                    self.changeOriginal(index2)
        self.im = plt.imshow(self.spins, cmap='winter', interpolation='nearest')
        return [self.im]

    def runK(self):
        fig, ax = plt.subplots()

        self.im=plt.imshow(self.spins, cmap='winter', interpolation='nearest')
        anim = FuncAnimation(fig, self.kawasaki, init_func = self.init, frames = self.iterations, repeat = False, interval = 1, blit = True)
        plt.show()

    def magnetization(self):
        return np.sum(self.spins)

    def getAvrgMag(self):
        self.averageMag = np.abs(float(np.sum(self.magVar))/float(len(self.magVar)))
'''
A = Spin(50,1.1, 200)

A.run(False)
print(A.averageMag)
'''

class Simulations(object):

    def __init__(self, iterations, dimensions, temperatures, anim):
        self.anim = anim
        self.iterations = iterations
        self.dimensions = dimensions
        self.temperatures = temperatures
        self.runs = len(temperatures)
        self.states=np.zeros(self.runs, dtype = object)
        self.magnetizations = np.array(())
        for i in range(self.runs):
            self.states[i]=Spin(self.dimensions,self.temperatures[i],self.iterations)
        self.start()
        self.analyze()


    def start(self):
        for i in range(self.runs):
            self.states[i].run(self.anim)
            print('ok')

    def analyze(self):
        for state in self.states:
            self.magnetizations = np.append(self.magnetizations, [state.averageMag])

        plt.plot(self.temperatures, self.magnetizations)
        plt.show()

B = Simulations(200, 50, np.arange(0.1,8.1,1), False)

'''
print(A.spins)
plt.imshow(A.spins, cmap='winter', interpolation='nearest')
plt.show()
'''
