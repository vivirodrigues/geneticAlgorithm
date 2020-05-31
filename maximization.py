import random
import numpy as np

def fitness(a,b,c,d):
	
	fitness = (5*a) - (3*b*c) + c - (2*d)
	return fitness

def calc_fitness(populacao):
	
	len_pop = len(populacao)
	len_individuo = len(populacao[0])
	aptitude = []
	for i in range(len_pop):		
		a = populacao[i][0]	
		b = populacao[i][1]			
		c = populacao[i][2]			
		d = populacao[i][3]			
		fitness1 = fitness(a,b,c,d)
		aptitude.append(fitness1)
		
	return aptitude

def bestIndividual(aptitude,population):
	
	minimo = min(aptitude)	
	for i in range(len(aptitude)):		
		if aptitude[i] > minimo:			
			minimo = aptitude[i]			
			indice = i		
	return population[indice]

# decreases all aptitude values by the minimum value
def windowing(aptitude):
	
	novaLista = []
	minimo = min(aptitude)
	for i in range(len(aptitude)):
		valor = aptitude[i] - minimo
		novaLista.append(valor)
	return novaLista

# exponential transformation
def expTransformation(aptitude):

	novaLista = []

	for i in range(len(aptitude)):
		valor = aptitude[i] + 1
		valor1 = valor ** (1/2)		
		novaLista.append(valor1)	
	return novaLista

def roulette(aptitude,randomNumber,population):
	
	selected = []
	sumAptitude = 0

	# sum of all valued of aptitude
	for i in range(len(aptitude)):
		sumAptitude += aptitude[i]
	
	# create a list with the probability value about each individual to be selected
	probabilities = []
	
	for i in range(len(aptitude)):
		probability = aptitude[i]/sumAptitude
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
def linearNormFuction(aptitude):
	
	idSort = np.argsort(aptitude)	
	N = 20 # increment
	i=0

	for idValue in idSort:
		aptitude[i] = (idValue)* N + 1
		i=i+1	
	
	return aptitude

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

# select parents for crossover
def selectIndiv(aptitude,amount,population):
		
	quant = 0
	selecteds = []
	indivAlreadyStored = False # to verify if the individual has already been stored

	while quant != amount: # about quantity of individuals must be selected
	
		randomNumber = random.random()
		#print("Random number generated:", randomNumber)
		selected = roulette(aptitude,randomNumber,population) # select one individual by roulette		
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
def mutation(individual, points, type):
	
	if type == 1:
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

	elif type == 2:
		
		first = []
		#print("Individual before swap mutation:", individual)	
		newIndividual = []		

		for i in range(len(individual)):
			if i <= points[0]:
				first.append(individual[i])
			elif i == points[1]:
				for a in range(len(first)):
					newIndividual.append(first[a]) # add the genes at points <= first point 
				newIndividual.append(individual[i]) # add the gene at current point
			else:
				newIndividual.append(individual[i])
		
		#print("Individual after swap mutation:", newIndividual)

		return newIndividual		

def nextGeneration(aptitude, lastGen):

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
	bestIndiv = bestIndividual(aptitude,lastGen)
	#print("Best individual from last generation:", bestIndiv)
	generation.append(bestIndiv)

	return generation

###################################################################################################

if __name__ == '__main__':

	selecionados = []
	population = [[0,1,1,0], [1,1,0,0], [1,0,1,1], [0,0,0,1]]
	print("Initial population:", population)			
	
	limit = 50
	end = False
	generation = 1
	
	while end != True:

		aptitude = calc_fitness(population)
		linear = linearNormFuction(aptitude)
		#aptitudeWindow = windowing(aptitude)	
		#aptitudeExpTransf = expTransformation(aptitudeWindow)				
		population = nextGeneration(linear, population) 
		print("Generation",generation,":", population)
		
		for i in range(len(population)):
			if population[i] == population[0] and population[i] == population[1] and population[i] == population[2]:
				print("Convergence")
				end = True
							
		if generation == limit:
			print("Limit of generations reached")
			end = True		
					
		result = population[3]

		generation += 1

	print("Result: ", result)
		
	