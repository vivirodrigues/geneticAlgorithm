import random
import numpy as np
import copy

def fitnessPopulation(population):
	
	len_pop = len(population)
	len_individuo = len(population[0])
	fitness = []
	
	for i in range(len_pop):
		
		matrix = transfMatrix(population[i])		
		colisionVector = colision(population[i], matrix)		
		aptitude = notColision(colisionVector)				
		fitness.append(aptitude)
		
	return fitness

def notColision(colision):
		
	notColi = []
	sumColision = 0

	for i in range(len(colision)):
		sumColision += colision[i] # decreases from queens that collided		
	
	notCol = 28 - sumColision	
	
	return notCol

def colision(vector, matrix):
	
	colision = []	

	for i in range(len(vector)):
		
		a = vector[i] # line of point
		b = i # column of point
		
		# line
		colisionHorizontally = horizontal(a,b,matrix)						
		# diagonal
		colisionDiagonally = diagonal(a,b,matrix)
		total = colisionHorizontally + colisionDiagonally	
		colision.append(total)
		#print(colision[i])
		total = 0
					
	return colision

def horizontal(a,b,matrix):	

	colision = 0

	for lin in range(len(matrix)):			
			if lin == a:				
				for col in range(len(matrix[0])):
					if col > b and matrix[lin][col] == 1:				
						colision += 1
	return colision

def diagonal(a,b,matrix):	
	
	# point a,b
	colision = 0		
	len_lin = len(matrix)
	len_col = len(matrix[0])	

	lin = a
	col = b

	while lin < len_lin and col < len_col:
				
		if matrix[lin][col]==1 and lin > a:
			colision += 1
			#print("colision in", lin, col)
				
		lin += 1
		col += 1
		if col == 8:
			col = 0
			break

	lin = a
	col = b

	while lin >= 0 and col >= 0:
		#print("lin",lin)
		#print("col",col)		
		if matrix[lin][col]==1 and lin < a:
			colision += 1
			#print("colision in", lin, col)
				
		lin -= 1
		col += 1
		
		if col == 8:
			col = 0
			break

	return colision
	
# vector of positions
def transfMatrix(vector):
		
	length = len(vector)
	matrix = createMatrix(length,length,0)	

	for col in range(len(vector)):
		var = vector[col]
		
		for lin in range(len(matrix)):
			list1 = matrix[lin]
			
			if lin == var:				
				matrix[lin][col] = 1

	return matrix

def imprime_matriz(M):  
  	for linha in M:
  		print("".join([str(i) for i in linha]))

def createMatrix(numLinhas, numColunas, valor):
	matriz = [] # lista vazia
	for i in range(numLinhas):
		linha = []
		for j in range(numColunas):
			linha.append(valor)
		matriz.append(linha)
	return matriz

def bestIndividual(aptitude,population):
		
	var = min(aptitude)
	indice = 0

	for i in range(len(aptitude)):		
		if aptitude[i] > var:			
			var = aptitude[i]						
			indice = i
	
	#print("Best individual:", aptitude[indice])
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

def roulette(fitness,randomNumber,population):
	
	selected = []
	sumFitness = 0

	# sum of all valued of fitness
	for i in range(len(fitness)):
		sumFitness += fitness[i]
	
	# create a list with the probability value about each individual to be selected
	probabilities = []
	
	for i in range(len(fitness)):
		probability = fitness[i]/sumFitness
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

def mutation(vector, min, max):
	
	allele = random.randrange(min, max+1, 1)
	locus = random.randrange(0, len(vector), 1)
	vector[locus] = allele
	
	return vector	

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
	children = recombinationCrossover(selecteds,points)	
	generation.append(children[0])
	generation.append(children[1])

	# mutation
	amountIndividuals = 1	
	selected = selectIndiv(aptitude,amountIndividuals,lastGen)
	mutated = mutation(selected,0,7)	
	generation.append(mutated)		
	
	# best individual	
	bestIndiv = bestIndividual(aptitude,before)	
	generation.append(bestIndiv)	

	return generation

###################################################################################################

if __name__ == '__main__':

	selecionados = []
	population = [[6,1,0,4,3,0,4,0],[6,1,6,4,3,0,4,3],[1,1,0,4,3,0,4,0],[6,1,6,4,3,0,4,6]]
	#print("Initial population:", population)			
	
	limit = 10000
	end = False
	generation = 0
	
	while end != True:

		aptitude = fitnessPopulation(population)
		#linear = linearNormFuction(aptitude)
		#aptitudeWindow = windowing(aptitude)	
		#aptitudeExpTransf = expTransformation(aptitude)				
		population = nextGeneration(aptitude, population) 		
		
		if population[0] == population[1] and population[1] == population[2] and population[2] == population[3]:
			print("Convergence")
			end = True

		if 	aptitude[3]==28:
			print("You got it")
			print("Generation",generation)
			end = True

		if generation > limit:
			print("Limit of generations reached")
			end = True		
					
		result = population[3]

		generation += 1

	print("Result: ", result, "Aptitude:", aptitude[3])