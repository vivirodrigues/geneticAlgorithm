import random
import numpy as np
import copy

def calc_aptitude(a,b,c,d):
	
	aptitude = (5*a) - (3*b*c) + c - (2*d)
	return aptitude

def calc_fitness(population):
	
	len_pop = len(population)
	len_individuo = len(population[0])
	fitness = []
	for i in range(len_pop):		
		a = population[i][0]	
		b = population[i][1]			
		c = population[i][2]			
		d = population[i][3]			
		aptitude1 = calc_aptitude(a,b,c,d)
		fitness.append(aptitude1)
		
	return fitness

def bestIndividual(fitness,population):
	
	minimo = fitness[0]
	indice = 0

	for i in range(len(fitness)):		
		if fitness[i] > minimo:			
			minimo = fitness[i]			
			indice = i		
	return population[indice]

# decreases all aptitude values by the minimum value
def windowing(fitness):
        
    newList = []
    min1 = min(fitness)
    for i in range(len(fitness)):
        value = fitness[i] - min1
        newList.append(value)
    return newList

# exponential transformation
def expTransformation(fitness):

    newList = []

    for i in range(len(fitness)):
        value = fitness[i] + 1
        value1 = value ** (1/2)
        newList.append(value1)
    return newList

def roulette(fitness,randomNumber,population):
	
	selected = []
	sumAptitude = 0

	# sum of all valued of fitness
	for i in range(len(fitness)):
		sumAptitude += fitness[i]
	
	# create a list with the probability value about each individual to be selected
	probabilities = []
	
	for i in range(len(fitness)):
		probability = fitness[i]/sumAptitude
		probabilities.append(probability)	
		
	# sort in ascending order
	probabilities.sort()	

	# verify the interval of random number
	sum_probabilities = 0
	for a in range(len(probabilities)):
		sum_probabilities += probabilities[a]		
		if float(randomNumber) < sum_probabilities:						
			return population[a]

# linear normalization
def linearNormFuction(fitness):
	
	idSort = np.argsort(fitness)	
	N = 20 # increment
	i=0

	for idValue in idSort:
		fitness[i] = (idValue)* N + 1
		i=i+1	
	
	return fitness

def recombinationCrossover(parents,points):
	
	child1 = []
	child2 = []
	father1 = parents[0]
	father2 = parents[1]

	if len(points) == 1:
		for i in range(len(father1)):
			if i <= points:
				child1.append(father1[i])			
			else:			
				child2.append(father1[i])
		
		for i in range(len(father2)):
			if i <= points:
				child2.append(father2[i])
			else:
				child1.append(father2[i])
	
	elif len(points) == 2:

		for i in range(len(father1)):
			if i <= points[0]:
				child1.append(father1[i])								
				child2.append(father2[i])
			elif i <= points[1]:
				child1.append(father2[i])								
				child2.append(father1[i])
			else:
				child1.append(father1[i])								
				child2.append(father2[i])

	return child1,child2


def selectIndiv(fitness,amount,population):
		
	quant = 0
	selecteds = []
	indivAlreadyStored = False # to verify if the individual has already been stored

	while quant != amount: # about quantity of individuals must be selected
	
		randomNumber = random.random()
		#print("Random number generated:", randomNumber)
		selected = roulette(fitness,randomNumber,population) # select one individual by roulette		
		if len(selecteds) > 0:
			for j in range(len(selecteds)):					
				if selecteds[j] == selected: # if the individual selected has already been stored
					indivAlreadyStored = True					
				else:
					indivAlreadyStored = False
			if indivAlreadyStored == False:
				selecteds.append(selected)			
		else:
			selecteds.append(selected)
		quant = len(selecteds)		

	if len(selecteds) > 1:
		return selecteds
	elif len(selecteds) == 1: # if it is just one individual, it is not returned inside other list
		return selecteds[0]

# 1 : swap mutation
# 2 : seq swap
def mutation(individual, points, typ):
	
	if typ == 1:
		#print("Individual before swap mutation:", individual)	
		newIndividual = []
		value1 = individual[points[0]]
		value2 = individual[points[1]]

		for i in range(len(individual)):
			if i == points[0]:
				newIndividual.append(value2)
			elif i == points[1]:
				newIndividual.append(value1)
			else:
				newIndividual.append(individual[i])
		
		#print("Individual after swap mutation:", newIndividual)

		return newIndividual

	elif typ == 2:
		
		#print("Individual before swap mutation:", individual)
		points.sort()		
		newIndividual = []		
		a1 = []
		a2 = []
		a3 = []

		for i in range(len(individual)):
			if i <= points[0]:
				a1.append(individual[i])
			elif i < points[1]:
				a2.append(individual[i])
			else:
				a3.append(individual[i])
			
		newIndividual = a3 + a2 + a1
		#print("Individual after swap mutation:", newIndividual)

		return newIndividual

def nextGeneration(aptitude, lastGen):

	before = copy.deepcopy(lastGen)
	points = []
	generation = []
	length = len(aptitude)
	points.append(random.randrange(0, length, 1))
	points.append(random.randrange(0, length, 1))
	
	# crossover
	amountParents = 2
	selecteds = selectIndiv(aptitude,amountParents,lastGen)
	#print("Selected individuals for crossover:",selecteds)
	children = recombinationCrossover(selecteds,points)
	#print("Children:", children)
	generation.append(children[0])
	generation.append(children[1])

	# mutation
	amountIndividuals = 1
	typeMutation = 1 # sequencial swap
	selected = selectIndiv(aptitude,amountIndividuals,lastGen)
	#print("Selected individual(s) for mutation:", selected)
	mutated = mutation(selected, points, typeMutation)	
	generation.append(mutated)
	
	# best individual
	bestIndiv = bestIndividual(aptitude,before)
	#print("Best individual from last generation:", bestIndiv)
	generation.append(bestIndiv)

	return generation

###################################################################################################

if __name__ == '__main__':

	selecionados = []
	population = [[0,1,1,0], [1,1,0,0], [1,0,1,1], [0,0,0,1]]
	#print("Initial population:", population)			
	
	limit = 2000
	end = False
	generation = 1
	
	while end != True:

		fitnessValues = calc_fitness(population) # fitness vector
		#linear = linearNormFuction(fitnessValues)
		aptitudeWindow = windowing(fitnessValues)	
		aptitudeExpTransf = expTransformation(aptitudeWindow)				
		population = nextGeneration(aptitudeExpTransf, population) 
		#print("Generation",generation,":", population)
		
		if population[0] == population[1] and population[1] == population[2] and population[2] == population[3]:
			print("Convergence in generation", generation)
			end = True
							
		if generation == limit:
			print("Limit of generations reached")
			end = True		
					
		result = population[3]

		generation += 1

	print("Result: ", result)
		
	
