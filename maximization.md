## Maximization

The individual is represented as a binary vector, where each value represents X1, X2, X3 and X4, respectively.
[0,1,1,0]
The initial population was exhibit as a list, where each item is an individual.


```python
population = [[0,1,1,0], [1,1,0,0], [1,0,1,1], [0,0,0,1]]
```

The code was developed in Python, without AI modules. The only module used was:


```python
import random
import copy
```

The aptitude of each individual is calculated by the function below.


```python
def calc_aptitude(a,b,c,d):
    
    aptitude = (5*a) - (3*b*c) + c - (2*d) # f = 5X1 - 3 X2 X3 + X3 - 2 X4.    
    return aptitude
```

The fitness function returns a vector with the aptitude value of each individual of population. The function bellow uses this idea to identify the fitness value.


```python
def calc_fitness(pop):

    len_pop = len(pop)    
    fitness = []
    a = 0
    b = 0
    c = 0
    d = 0
    
    for i in range(len_pop):
        
        a = pop[i][0]
        b = pop[i][1]
        c = pop[i][2]
        d = pop[i][3]
        aptitude1 = calc_aptitude(a,b,c,d)
        fitness.append(aptitude1)
    
    return fitness
```

The functions below implement the windowing and exponential transformation methods in the firness vector.


```python
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
```

To select individuals, the roulette method is used, described below.


```python
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
            #print(population[a])
            return population[a]
```

The function below selects individuals using the roulette method. The number of individuals to be selected is described in the amount variable.


```python
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

The mutation is performed using the function below, where typ variable represents the type of mutation (1: swap, and 2: sequential swap)


```python
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
            
        first = []
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

        return newIndividual
```

The best individual of the current generation is identified by the highest fitness value:


```python
def bestIndividual(fitness,population):

    minimo = min(fitness)
    for i in range(len(fitness)):
        if fitness[i] > minimo:
            minimo = fitness[i]
            indice = i
    return population[indice]
```

The next generation is created out of elitism, where two individuals from the previous generation crossover, one mutates and the best individual remains alive.


```python
def nextGeneration(aptitude, lastGen):

    points = []
    generation = []
    length = len(aptitude)
    points.append(random.randrange(0, length, 1))
    points.append(random.randrange(0, length, 1))
    before = copy.deepcopy(lastGen)

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
    typeMutation = 1 # swap
    selected = selectIndiv(aptitude,amountIndividuals,lastGen)
    #print("Selected individual(s) for mutation:", selected)
    mutated = mutation(selected, points, typeMutation)
    generation.append(mutated)
    
    # best individual
    bestIndiv = bestIndividual(aptitude,before)
    #print("Best individual from last generation:", bestIndiv)
    generation.append(bestIndiv)
    return generation
```


```python
if __name__ == '__main__':

    selecionados = []
    population = [[0,1,1,0], [1,1,0,0], [1,0,1,1], [0,0,0,1]]
    print("Initial population:", population)

    limit = 200
    end = False
    generation = 1

    while end != True:

        fitnessValues = calc_fitness(population) # fitness vector
        aptitudeWindow = windowing(fitnessValues)
        aptitudeExpTransf = expTransformation(aptitudeWindow)
        population = nextGeneration(aptitudeExpTransf, population)         
        
        if population[3] == [1, 0, 1, 0]:
            print("Convergence in generation", generation)
            end = True
                            
        if generation == limit:
            print("Limit of generations reached")
            end = True

        result = population[3]

        generation += 1

    print("Result: ", result)
```

    Initial population: [[0, 1, 1, 0], [1, 1, 0, 0], [1, 0, 1, 1], [0, 0, 0, 1]]
    Convergence in generation 3
    Result:  [1, 0, 1, 0]

