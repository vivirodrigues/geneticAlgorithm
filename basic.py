import random

def fitness(a,b,c,d):
	
	fitness = (5*a) - (3*b*c) + c - (2*d)
	return fitness

def calc_fitness(populacao):
	
	len_pop = len(populacao)
	len_individuo = len(populacao[0])
	aptidao = []
	for i in range(len_pop):		
		a = populacao[i][0]	
		b = populacao[i][1]			
		c = populacao[i][2]			
		d = populacao[i][3]			
		fitness1 = fitness(a,b,c,d)
		aptidao.append(fitness1)		
	return aptidao

def melhorIndiv(aptidao):
	
	minimo = min(aptidao)	
	for i in range(len(aptidao)):		
		if aptidao[i] > minimo:			
			minimo = aptidao[i]			
			indice = i		
	return indice

# diminui todos os valores de aptidao pelo valor minimo
def windowing(aptidao):
	
	novaLista = []
	minimo = min(aptidao)
	for i in range(len(aptidao)):
		valor = aptidao[i] - minimo
		novaLista.append(valor)
	return novaLista

# organiza lista com os melhores individuos
def selecionaMelhor(populacao,maximo,aptidao,selecionados):
	
	lastGen = [] # last generation
	novaAptidao = [] # nova lista de aptidao, excluindo os que ja foram selecionados

	for i in range(len(populacao)):
		if i != maximo:	# esse indice pode ser calculado com a funcao melhorIndiv. Ex: indiceDoMelhor = melhorIndiv(aptidao)
			novaAptidao.append(aptidao[i])
			lastGen.append(populacao[i])
		else:			
			selecionados.append(populacao[i]) # eh importante inicializar a lista selecionados antes de entrar na funcao			
	return lastGen,novaAptidao,selecionados


def roulette(aptidao,randomico,selecionados):
	
	somaAptidao = 0
	for i in range(len(aptidao)):
		somaAptidao += aptidao[i]
	
	# cria uma lista com o valor da probabilidade para cada individuo
	probabilidades = []
	anterior = 0.0
	for i in range(len(aptidao)):
		probabilidade = aptidao[i]/somaAptidao
		probabilidades.append(probabilidade)	
	
	# ordena em ordem crescente
	probabilidades.sort()	

	# verifica em que intervalo o valor randomico esta
	soma_probabilidades = 0
	for a in range(len(probabilidades)):
		soma_probabilidades += probabilidades[a]		
		if float(randomico) < soma_probabilidades:
			selecionados.append(populacao[a])
			return selecionados
	


###################################################################################################

if __name__ == '__main__':

	populacao = [[0,1,1,0], [1,1,0,0], [1,0,1,1], [0,0,0,1]]
	selecionados = []

	aptidao = calc_fitness(populacao)
	novaAptidao = windowing(aptidao)
	randomico = random.random()	
	print("Valor randomico gerado:", randomico)
	selecionados = roulette(novaAptidao,randomico,selecionados)
	print("Individuo selecionado:",selecionados)


