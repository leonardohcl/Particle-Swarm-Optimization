import matplotlib.pyplot as plt
import numpy as np

def f(x,y):
        return ((1-x)**2) + 100*((y - x**2)**2)

def getBestNeighbor(i, fitness):
        right = i + 1
        left = i - 1
        if(right >= len(fitness)):
                right = 0
        elif(left < 0):
                left = len(fitness) - 1
        
        if(fitness[right] < fitness[left]):
                if(fitness[right] < fitness[i]):
                        return right
                else:
                        return i
        else:
                if(fitness[left]<fitness[i]):
                        return left
                else:
                        return i

def plotPoints(particles,it):
        plt.axis([-5,5,-5,5]) 
        plt.title('it='+str(it), loc='left')
        x = []
        y = []
        plt.contourf(xImage,yImage,zImage,200,cmap='jet', alpha=0.5)
        plt.colorbar()
        for i in range(len(particles)):
                x.append(particles[i][0])
                y.append(particles[i][1])
        plt.plot(x,y,'ko')
        plt.show()

def getSpacialContours(start, end, step):
        size = end - start
        n = int(size / step) + 1
        x = np.zeros(n)
        y = np.zeros(n)
        z = np.zeros((n,n))
        for i in range(n):
                x[i] = start + step*i
                for j in range(n):
                        y[j] = start + step*j
                        z[i][j] = f(x[i],y[j])
        
        return [x,y,z]

def getBestFitnessIndex(fitness):
        return fitness.tolist().index(min(fitness))

[xImage, yImage, zImage] = getSpacialContours(-5,5,0.1)