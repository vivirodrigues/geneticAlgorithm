## 8-queens puzzle

An individual is represented by a chromosome, and each gene is the respective position of the queen in the specific column:


```python
[6,1,0,4,3,0,4,0]
```




    [6, 1, 0, 4, 3, 0, 4, 0]



The initial population was exhibit as a list, where each item is an individual.


```python
population = [[6,1,0,4,3,0,4,0],[6,1,6,4,3,0,4,3],[1,1,0,4,3,0,4,0],[6,1,6,4,3,0,4,6]]
```

The code was developed in Python, without AI modules. The modules used were:


```python
import random
import copy
```

An individual must be represented by a binary matrix. The positions of the queens are demonstrated as "1", and the empty positions are represented by "0". The function below makes the conversion of positions vector to binary matrix:


```python
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

def createMatrix(numLinhas, numColunas, valor):
    matriz = [] # lista vazia
    for i in range(numLinhas):
        linha = []
        for j in range(numColunas):
            linha.append(valor)
        matriz.append(linha)
    return matriz
```

So, the matrix of individual [6,1,0,4,3,0,4,0] can be represented as:

```python
00100101
01000000
00000000
00001000
00010010
00000000
10000000
00000000
```

The fitness function is the number of queens that are not attacking each other. To calculate that, first, we can verify how many queens are attacking each other. The collision function do that:


```python
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
```


```python
def horizontal(a,b,matrix):	

    colision = 0

    for lin in range(len(matrix)):
        if lin == a:
            for col in range(len(matrix[0])):
                if col > b and matrix[lin][col] == 1:
                    colision += 1
    return colision
```


```python
def diagonal(a,b,matrix):

    colision = 0
    len_lin = len(matrix)
    len_col = len(matrix[0])

    lin = a
    col = b

    while lin < len_lin and col < len_col:

        if matrix[lin][col]==1 and lin > a:
            colision += 1

        lin += 1
        col += 1
        if col == 8:
            col = 0
            break

    lin = a
    col = b

    while lin >= 0 and col >= 0:

        if matrix[lin][col]==1 and lin < a:
            colision += 1

        lin -= 1
        col += 1

        if col == 8:
            col = 0
            break

    return colision

```

With information on the number of queens that are attacking, it is possible to know how many are not colliding. Considering 8 queens, the largest possible number of non-collisions is 28, because: 7 + 6 + 5 + 4 + 3 + 2 + 1 = 28


```python
def notColision(colision):

    notColi = []
    sumColision = 0

    for i in range(len(colision)):
        sumColision += colision[i] # decreases from queens that collided

    notCol = 28 - sumColision

    return notCol
```

Then, to calculate the fitness function of the population, we must use the aptitude of each individual. The function bellow uses the idea of collisions to identify the fitness value.


```python
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
```

To select individuals, the roulette method is used, described below.


```python
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
```

The function below selects individuals using the roulette method. The number of individuals to be selected is described in the amount variable.


```python
def selectIndiv(fitness,amount,population):

    quant = 0
    selecteds = []
    indivAlreadyStored = False # to verify if the individual has already been stored

    while quant != amount: # amount of individuals must be selected

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
```

The recombination (crossover) of individuals is performed using the function below. The "points" variable represents the cut-off point of the chromosome.


```python
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
```

The mutation is performed generatively, using the function below:


```python
def mutation(vector, min, max):

    allele = random.randrange(min, max+1, 1)
    locus = random.randrange(0, len(vector), 1)
    vector[locus] = allele

    return vector
```

The best individual of the current generation is identified by the highest fitness value:


```python
def bestIndividual(fitness,population):
            
    var = min(fitness)
    indice = 0

    for i in range(len(fitness)):
        if fitness[i] > var:
            var = fitness[i]
            indice = i

    return population[indice]
```

The next generation is created out of elitism, where two individuals from the previous generation crossover, one mutates and the best individual remains alive.


```python
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

```

The function vectorsFitness save best and worst fitness values, and average of fitness.


```python
def vectorsFitness(bestIndividuals,worstIndividuals,sumIndividuals,fitness):

    best = fitness[0]
    worst = fitness[0]
    sum1 = 0
    average = 0

    for i in range(len(fitness)):
            
        sum1 += fitness[i]

        if fitness[i] > best:
            best = fitness[i]

        if fitness[i] < worst:
            worst = fitness[i]

    average = sum1 / 4 # 4: number of individuals (generation)

    bestIndividuals.append(best)
    worstIndividuals.append(worst)
    averageIndividuals.append(average)

    return bestIndividuals,worstIndividuals,averageIndividuals
```


```python
if __name__ == '__main__':

    selecionados = []
    population = [[6,1,0,4,3,0,4,0],[6,1,6,4,3,0,4,3],[1,1,0,4,3,0,4,0],[6,1,6,4,3,0,4,6]]
    bestIndividuals = [] # best fitness of individuals (each generation)
    worstIndividuals = [] # worst fitness of individuals (each generation)
    averageIndividuals = [] # fitness average (each generation)

    limit = 10000
    end = False
    generation = 1

    while end != True:

        fitness = fitnessPopulation(population)        
        population = nextGeneration(fitness, population)
        bestIndividuals,worstIndividuals,averageIndividuals = vectorsFitness(bestIndividuals,worstIndividuals,averageIndividuals,fitness)

        if population[0] == population[1] and population[1] == population[2] and population[2] == population[3]:
            print("Convergence")
            end = True

        if 	fitness[3]==28:
            print("You got it")
            print("Generation",generation)
            end = True

        if generation > limit:
            print("Limit of generations reached")
            end = True
                    
        result = population[3]

        generation += 1

    print("Result: ", result, "Fitness:", fitness[3])
```

    You got it
    Generation 3900
    Result:  [4, 1, 7, 0, 3, 6, 2, 5] Fitness: 28

