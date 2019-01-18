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

    def setInitialStates(self):
        for i in range(0,self.dimensions):
            for j in range(self.dimensions):
                if np.random.uniform(0,1)>=0.5:
                    self.spins[i,j] = 1
                else:
                    self.spins[i,j] = -1


    def NNsum(self,state, x,y):
        sum = 0
        sum+= state[x,y]*state[(x+1)%self.dimensions, y]
        sum+= state[x,y]*state[(x-1)%self.dimensions, y]
        sum+= state[x,y]*state[x,(y+1)%self.dimensions]
        sum+= state[x,y]*state[x, (y-1)%self.dimensions]
        return sum*-1



        '''
        if x == 0 and y == 0:
            sum += state[x,y]*state[x+1,y]
            sum += state[x,y]*state[x,y+1]
            sum += state[x,y]*state[-1,y]
            sum += state[x,y]*state[x,-1]
            return sum*-1
        elif x == self.dimensions-1 and y == self.dimensions-1:
            sum += state[x,y]*state[x-1,y]
            sum += state[x,y]*state[x,y-1]
            sum += state[x,y]*state[0,y]
            sum += state[x,y]*state[x,0]
            return sum*-1
        elif x == 0:
            sum += state[x,y]*state[x+1,y]
            sum += state[x,y]*state[x,y+1]
            sum += state[x,y]*state[x,y-1]
            sum += state[x,y]*state[-1,y]
            return sum*-1
        elif x == self.dimensions-1:
            sum += state[x,y]*state[x-1,y]
            sum += state[x,y]*state[x,y+1]
            sum += state[x,y]*state[x,y-1]
            sum += state[x,y]*state[0,y]
            return sum*-1
        elif y == 0:
            sum += state[x,y]*state[x+1,y]
            sum += state[x,y]*state[x,y+1]
            sum += state[x,y]*state[x-1,y]
            sum += state[x,y]*state[x,-1]
            return sum*-1
        elif y == self.dimensions-1:
            sum += state[x,y]*state[x-1,y]
            sum += state[x,y]*state[x+1,y]
            sum += state[x,y]*state[x,y-1]
            sum += state[x,y]*state[x,0]
            return sum*-1
        else:
            sum += state[x,y]*state[x+1,y]
            sum += state[x,y]*state[x-1,y]
            sum += state[x,y]*state[x,y+1]
            sum += state[x,y]*state[x,y-1]
            return sum*-1
            '''


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
            index = self.makeAlteredCopy()
            diff = self.NNsum(self.alteredCopy,index[0],index[1])-self.NNsum(self.spins,index[0],index[1])
            if diff<0:
                self.changeOriginal(index)
            else:
                p = np.exp((-1*diff)/self.T)
                if np.random.uniform(0,1)<p:
                    self.changeOriginal(index)
        self.im = plt.imshow(self.spins, cmap='winter', interpolation='nearest')
        return [self.im]


    def run(self):
        fig, ax = plt.subplots()

        self.im=plt.imshow(self.spins, cmap='winter', interpolation='nearest')
        anim = FuncAnimation(fig, self.change, init_func = self.init, frames = self.iterations, repeat = False, interval = 1, blit = True)
        plt.show()


    def init(self):
        return [self.im]

    def kawasaki(self, i):
        for j in range(self.dimensions*self.dimensions):
            index1 = np.random.randint(0,self.dimensions,2)
            index2 = np.random.randint(0,self.dimensions,2)
            beforeEnergy1 = self.NNsum(self.spins,index1[0],index1[1])
            beforeEnergy2 = self.NNsum(self.spins,index2[0],index2[1])
            



A = Spin(50,1, 100000)

A.run()

'''
print(A.spins)
plt.imshow(A.spins, cmap='winter', interpolation='nearest')
plt.show()
'''
