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
        self.energyVar = np.array(())
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
            self.energyVar = np.append(self.energyVar, [self.getTotalEnergy()])
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
                self.energyVar = np.append(self.energyVar, [self.getTotalEnergy()])



    def run(self, anim):
        if anim ==True:
            fig, ax = plt.subplots()
            self.im=plt.imshow(self.spins, cmap='winter', interpolation='nearest')
            anim = FuncAnimation(fig, self.change, init_func = self.init, frames = self.iterations, repeat = False, interval = 1, blit = True)
            plt.show()
        else:
            self.changeNoAnim()
        self.getAvrgMag()
        self.getAvrgEnergy()


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

    def kawasakiNoAnim(self):
        for i in range(self.iterations):
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
            self.testVar+=1
            if self.testVar%100 ==0 or (self.testVar>100 and self.testVar%10==0):
                self.magVar = np.append(self.magVar,[self.magnetization()])
                self.energyVar = np.append(self.energyVar, [self.getTotalEnergy()])


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
        self.testVar+=1
        if self.testVar%100 ==0 or (self.testVar>100 and self.testVar%10==0):
            self.magVar = np.append(self.magVar,[self.magnetization()])
            self.energyVar = np.append(self.energyVar, [self.getTotalEnergy()])
        self.im = plt.imshow(self.spins, cmap='winter', interpolation='nearest')
        return [self.im]

    def runK(self, anim):
        if anim==True:
            fig, ax = plt.subplots()
            self.im=plt.imshow(self.spins, cmap='winter', interpolation='nearest')
            anim = FuncAnimation(fig, self.kawasaki, init_func = self.init, frames = self.iterations, repeat = False, interval = 1, blit = True)
            plt.show()
        else:
            self.kawasakiNoAnim()
        self.getAvrgMag()
        self.getAvrgEnergy()

    def magnetization(self):
        return np.sum(self.spins)

    def getAvrgMag(self):
        self.averageMag = np.abs(float(np.sum(self.magVar))/float(len(self.magVar)))
        self.averageSquaremag = float(np.sum(self.magVar**2))/float(len(self.magVar))
        self.squareAverageMag = self.averageMag**2

    def getTotalEnergy(self):
        energy = 0
        for x in range(self.dimensions):
            for y in range(self.dimensions):
                energy += self.NNsum(self.spins[x,y],x,y)
        return energy

    def getAvrgEnergy(self):
        self.averageEnergy = np.abs(float(np.sum(self.energyVar))/float(len(self.energyVar)))
        self.averageSquareEnergy = float(np.sum(self.energyVar**2))/float(len(self.energyVar))
        self.squareAverageEnergy = self.averageEnergy**2
        self.heatCapacity = (1./float(self.dimensions*self.T**2))*(self.averageSquareEnergy-self.squareAverageEnergy)
        self.heatCapError = 0
        self.removedEnergyState = self.energyVar
        #print(self.heatCapacity)
        for i in range(len(self.energyVar)-1):
            self.removedEnergyState = np.delete(self.energyVar, i)
            self.removedSquareAverageEnergy = np.abs(float(np.sum(self.removedEnergyState))/float(len(self.removedEnergyState)))**2
            self.removedAverageSquareEnergy = float(np.sum(self.removedEnergyState**2))/float(len(self.removedEnergyState))
            self.removedHeatCapacity = (1./float(self.dimensions*self.T**2))*(self.removedAverageSquareEnergy-self.removedSquareAverageEnergy)
            #print(self.removedHeatCapacity)
            self.heatCapError += (self.removedHeatCapacity-self.heatCapacity)**2
        self.heatCapError = np.sqrt(self.heatCapError)



'''
A = Spin(50,1.1, 200)

A.run(False)
print(A.averageMag)
'''

class Simulations(object):

    def __init__(self, iterations, dimensions, temperatures, anim, kawasaki = False):
        self.kawasaki = kawasaki
        self.anim = anim
        self.iterations = iterations
        self.dimensions = dimensions
        self.temperatures = temperatures
        self.runs = len(temperatures)
        self.states=np.zeros(self.runs, dtype = object)
        self.magnetizations = np.array(())
        self.susceptebilities = np.array(())
        self.energies = np.array(())
        self.heatCap = np.array(())
        self.heatCapErrors = np.array(())
        for i in range(self.runs):
            self.states[i]=Spin(self.dimensions,self.temperatures[i],self.iterations)
        self.start()
        self.analyzeMag()
        self.analyzeSus()
        self.analyzeEnergy()
        self.analyzeHeatCap()


    def start(self):
        if self.kawasaki == False:
            for i in range(self.runs):
                self.states[i].run(self.anim)
                print('ok')
        else:
            for i in range(self.runs):
                self.states[i].runK(self.anim)
                print('ok')

    def analyzeMag(self):
        for state in self.states:
            self.magnetizations = np.append(self.magnetizations, [state.averageMag])

        plt.plot(self.temperatures, self.magnetizations)
        plt.title('Magnetization')
        plt.show()

    def analyzeSus(self):
        for i in range(self.runs):
            self.susceptebilities = np.append(self.susceptebilities, [(1./float(self.dimensions*self.states[i].T))*(self.states[i].averageSquaremag-self.states[i].squareAverageMag)])

        plt.plot(self.temperatures, self.susceptebilities)
        plt.title('Susceptebility')
        plt.show()

    def analyzeEnergy(self):
        for state in self.states:
            self.energies = np.append(self.energies, [state.averageEnergy])

        plt.plot(self.temperatures, self.energies)
        plt.title('Total Energy')
        plt.show()

    def analyzeHeatCap(self):
        for i in range(self.runs):
            self.heatCap = np.append(self.heatCap, [(1./float(self.dimensions*self.states[i].T**2))*(self.states[i].averageSquareEnergy-self.states[i].squareAverageEnergy)])
            self.heatCapErrors = np.append(self.heatCapErrors, [self.states[i].heatCapError])
        plt.plot(self.temperatures, self.heatCap)
        #plt.scatter(self.temperatures, self.heatCap)
        plt.title('Heat Capacity')
        plt.errorbar(self.temperatures, self.heatCap, yerr = self.heatCapErrors, fmt='o')
        plt.show()

#B = Simulations(300, 50, np.arange(0.1,4.1,0.5), False)



class Interface(object):

    def __init__(self):
        self.more = int(raw_input("do you want to run one(0) or multiple simulations(1)?"))
        if self.more == 0:
            self.dim = int(raw_input('dimensions?'))
            self.tem = float(raw_input('temperature?'))
            self.it = int(raw_input('iterations?'))
            self.an = int(raw_input('animate(yes(1), no(0))'))
            self.type = int(raw_input('Sim Type?(glauber(0), kawasaki(1))'))
            A = Spin(self.dim,self.tem,self.it)
            if self.an==0:
                A.run(self.an)
            else:
                A.runK(self.an)
        else:
            self.dim = int(raw_input('dimensions?'))
            self.temS = float(raw_input('temperature(start)?'))
            self.temP = float(raw_input('temperature(stop)?'))
            self.temI = float(raw_input('temperature(interval)?'))
            self.tem = np.arange(self.temS,self.temP,self.temI)
            self.it = int(raw_input('iterations?'))
            self.an = int(raw_input('animate(yes(1), no(0))'))
            self.type = int(raw_input('Sim Type?(glauber(0), kawasaki(1))'))
            print('------Starting simulations-------')
            B = Simulations(self.it,self.dim,self.tem,self.an)
            if self.an==0:
                B.run(self.an)
            else:
                B.runK(self.an)


C = Interface()
'''
print(A.spins)
plt.imshow(A.spins, cmap='winter', interpolation='nearest')
plt.show()
'''
