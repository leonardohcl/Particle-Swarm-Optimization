import numpy as np
import matplotlib.pyplot as plt
import math
from random import random
from functions import getBestNeighbor, plotPoints, f, getBestFitnessIndex

#Número de vezes que o algoritmo se repetirá
repetitions = 1
meanBestX = 0 #Melhor x médio
meanBestY = 0 #melhor y médio
meanBestF = 0 #Melhor f(x,y) médio
meanBestResultPoint = 0
showPlots = False #Mostrar gráficos da execução
printProgress = True #Mostrar progresso das iterações
printRepetitionProgress = False #Mostrar progresso das repetições
printExecutionResults = True #Mostrar resultados de cada execução
varyInertia = False #Variar inercia de acordo com as iterações

#limites pra x
maxX = 5
minX = -5
#limites para velocidade em x
vMaxX = 1
vMinX = -1
#limites pra y
maxY = 5
minY = -5
#limites para velocidade em y
vMaxY = 1
vMinY = -1
#---
maxIt = 1000 #número de iterações
n = 25 #num de particulas
ac1 = 2.05 #acelaracao 1 (comportamento cognitivo)
ac2 = 2.05 #acelaracao 2 (comportamento social)

repetitionProgress = 0
repStep = 0
for rep in range(repetitions):
        #Controle de execução
        repetitionProgress = float(rep) / repetitions
        if(repetitionProgress >= repStep and printRepetitionProgress):
                repStep = repStep + 0.1
                repetitionProgress = repetitionProgress * 100
                print(str(repetitionProgress)+'% - Repetições')
        #Inicia variáveis
        #lista da posição das particulas
        particle = np.zeros((n,2))
        #lista da melhor posição das particulas
        bestParticlePosition = np.zeros((n,2))
        #lista da melhor aptidão das particulas
        bestParticleFitness = np.zeros(n)
        #lista de velocidades das particulas
        velocity = np.zeros((n,2))
        #lista da aptidão das particulas
        fitness = np.zeros(n)
        #lista com a média da aptidão das particulas de cada iteração
        meanItFitness = []
        #lista com a melhor aptidão de cada iteração
        bestItFitness = []
        #lista com o melhor resultado até a dada iteração
        bestOfAllFitnessIt = []
        #indice da melhor aptidão da iteração
        itBestIndex = -1
        #melhor posição encontrada até a dada iteração
        bestOfAll = np.zeros(2)
        #fitness da melhor posição encontrada até a dada iteração
        bestOfAllFitness = float('Inf')
        #iteração em que a melhor posição foi encontrada 
        itOfBestOfAllFitness = 0
        #lista de iteraçõs que ocorreu melhora de aptidão
        listOfImprovements = []
        listOfImprovementsFitness = []
        #Inicia valores aleatóriamente
        for i in range(n):
                particle[i][0] = minX + (maxX - minX) * random()
                particle[i][1] = minY + (maxY - minY) * random()
                velocity[i][0] = vMinX + (vMaxX - vMinY) * random()
                velocity[i][1] = vMinY + (vMaxY - vMinY) * random()
                fitness[i] = f(particle[i][0],particle[i][1])
                bestParticlePosition[i][0] = particle[i][0]
                bestParticlePosition[i][1] = particle[i][1]
                bestParticleFitness[i] = fitness[i]
        itBestIndex = getBestFitnessIndex(fitness)
        bestOfAll[0] = particle[itBestIndex][0]        
        bestOfAll[1] = particle[itBestIndex][1]    
        bestOfAllFitness = fitness[itBestIndex]
        bestOfAllFitnessIt.append(bestOfAllFitness)    
        listOfImprovements.append(0)
        listOfImprovementsFitness.append(bestOfAllFitness)
        meanItFitness.append(sum(fitness)/n)
        bestItFitness.append(min(fitness))

        step = 0
        #Para o número máximo de iterações
        for it in range(maxIt):
                #Controle de execução
                prct = float(it) / maxIt
                if(prct >= step and printProgress):
                        step = step + 0.1
                        prct = prct * 100
                        print(str(prct)+'% - Iterações')
                #Atualiza o peso de inercia de acordo com a execução
                if(varyInertia):
                        w = 1 - prct
                else:
                        w = 1

                #Atualiza multiplicadores
                phi1 = [ac1 * random(), ac1 * random()]
                phi2 = [ac2 * random(), ac2 * random()]
                newFitness = np.zeros(n) 
                #Para cada particula
                for i in range(n):
                        #Encontra o minimo local
                        bestNeighbor = getBestNeighbor(i, fitness)
                        #Encontra nova velocidade
                        velocity[i][0] = w*velocity[i][0] + phi1[0] * (bestParticlePosition[i][0] - particle[i][0]) + phi2[0]*(particle[bestNeighbor][0] - particle[i][0])
                        velocity[i][1] = w*velocity[i][1] + phi1[1] * (bestParticlePosition[i][1] - particle[i][1]) + phi2[1]*(particle[bestNeighbor][1] - particle[i][1])
                        #Ajusta velocidade para estar entre o minimo/maximo
                        if(velocity[i][0] < vMinX):
                                velocity[i][0] = vMinX
                        elif(velocity[i][0] > vMaxX):
                                velocity[i][0] = vMaxX

                        if(velocity[i][1] < vMinY):
                                velocity[i][1] = vMinY
                        elif(velocity[i][1] > vMaxY):
                                velocity[i][1] = vMaxY
                        #Atualiza posição da particula
                        particle[i][0] = particle[i][0] + velocity[i][0]
                        particle[i][1] = particle[i][1] + velocity[i][1]
                        #Encontra a aptidão para a próxima iteração
                        newFitness[i] = f(particle[i][0],particle[i][1])
                        #Atualiza melhor solução conhecida se necessário
                        if(newFitness[i] < bestParticleFitness[i]):
                                bestParticleFitness[i] = newFitness[i]
                                bestParticlePosition[i][0] = particle[i][0]
                                bestParticlePosition[i][1] = particle[i][1]
                #Atualiza a lista de aptidões
                fitness = newFitness
                #Encontra a melhor aptidão da iteração
                itBestIndex = getBestFitnessIndex(fitness)
                #Incrementa a lista de média das iterações
                meanItFitness.append(sum(fitness)/n)
                #Incremente a lista de melhor aptidão de cada iteração
                bestItFitness.append(fitness[itBestIndex])
                #Atualiza a melhor aptidão encotrada se for o necessário 
                if(fitness[itBestIndex] < bestOfAllFitness):
                        itOfBestOfAllFitness = it+1
                        bestOfAllFitness = fitness[itBestIndex]
                        bestOfAll[0] = particle[itBestIndex][0]
                        bestOfAll[1] = particle[itBestIndex][1]
                        listOfImprovements.append(it+1)
                        listOfImprovementsFitness.append(bestOfAllFitness)
                #Incrementa a lista da melhor aptidão até agora
                bestOfAllFitnessIt.append(bestOfAllFitness)

        plotPoints(particle,it)

        if(printExecutionResults):
                print('Melhor resultado (it = '+str(itOfBestOfAllFitness)+'):')
                print('f('+str(bestOfAll[0])+','+str(bestOfAll[1])+') = '+str(bestOfAllFitness))
        if(showPlots):
                plt.plot(meanItFitness, 'r', label="Aptidão média")
                plt.plot(bestItFitness, 'b', label="Melhor aptidão desta iteração")
                plt.plot(bestOfAllFitnessIt, 'g', label="Melhor aptidão até agora")
                plt.plot(listOfImprovements,listOfImprovementsFitness, 'k.', label="Iteração com nova melhor aptidão")
                plt.legend()
                plt.show()
        meanBestX += bestOfAll[0]
        meanBestY += bestOfAll[1]
        meanBestResultPoint += itOfBestOfAllFitness
meanBestX = meanBestX/repetitions
meanBestY = meanBestY/repetitions
meanBestF = f(meanBestX,meanBestY)
meanBestResultPoint = math.ceil(meanBestResultPoint/repetitions)
print("------------------------")
print("Resultado médio de "+str(repetitions)+" execuções:")
print('f('+str(meanBestX)+','+str(meanBestY)+') = '+str(meanBestF))
print("Iteração média que atingiu o menor resultado: "+str(meanBestResultPoint))
                
