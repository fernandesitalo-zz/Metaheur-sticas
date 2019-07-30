from random import random,randint
from math import pi,cos,exp
import numpy as np
np.random.seed(100)

class bat_algorithm():
  def __init__(self, D, tpop, niter, r0, Alfa, Lambda ,fmin, fmax, limInf_, limSup_, function):
    self.D = D          	# dimensao - quanidade de variaveis da equacao
    self.tpop = tpop        # tamanho da populacao
    self.niter = niter      # numero de iteracoes / geracoes
    self.Alfa = Alfa      	# parametro 1 - decaimento da amplitude ao encontrar uma amplitude menor
    self.Lambda = Lambda    # parametro 2
    self.fmin = fmin        # frequency min
    self.fmax = fmax        # frequency max
    self.li = limInf_       # limite inferior de busca
    self.ls = limSup_       # limite superior de busca
    self.Fun = function     # funcao para analise
    self.r0 = r0       		# r inicial

	######### - convenções 
    self.A = [0.95 for i in range(self.tpop)]     # amplitude - mesmo valor para todos morcegos
    self.r = [self.r0 for i in range(self.tpop)]  # taxa de emissao de pulso - mesmo valor para todos morcegos
	######### -
	
    self.limInf = [0 for i in range(self.D)]    # limite inferior para cada variavel  --- estabelecer limites diferentes para cada variavel? - talvez
    self.limSup = [0 for i in range(self.D)]    # limite superior para cada variavel

    self.f = [0.0] * self.tpop	# frequencia

    self.v = [[0.0 for i in range(self.D)] for j in range(self.tpop)] 	 # velocidade

    self.Sol = [[0.0 for i in range(self.D)] for j in range(self.tpop)]  # valores das variaveis dos morcegos existentes

    self.Fitness = [0.0] * self.tpop    # fitness
    self.melhor = [0] * self.D     		# configuracao da melhor solucao
    self.melhorFitness = 0.0         		# valor da melhor solucao

    self.Amedia = None					# media das amplitudes

  def melhorMorcego(self):# define melhor morcego 
    j = 0
    for i in range(self.tpop):
      if self.Fitness[i] < self.Fitness[j]:
        j = i
    for i in range(self.D):
      self.melhor[i] = self.Sol[j][i]
    self.melhorFitness = self.Fitness[j]

  def inicializacao(self):
    for i in range(self.D): # mesmos limites para cada variavel
      self.limInf[i] = self.li
      self.limSup[i] = self.ls
      
    for i in range(self.tpop):
      self.f[i] = 0
      for j in range(self.D):
        self.v[i][j] = 0.0	# velocidade inicial igual a zero para todos morcegos
        self.Sol[i][j] = self.limInf[j] + (self.limSup[j] - self.limInf[j]) * np.random.uniform(0,1) # atribui uma "frequencia aleatoria"
      self.Fitness[i] = self.Fun(self.D, self.Sol[i])
    self.melhorMorcego()


  def ajeitaLimites(self, val, d): # NORMALIZA O VALOR DE ACORDO COM OS PARAMENTROS PASSADOS (LIMITES DE BUSCA)
    if val < self.limInf[d]:
      val = self.limInf[d]
    if val > self.limSup[d]:
      val = self.limSup[d]
    return val

  def executa(self):
    # SOLUCOES ATUAIS
    S = [[0.0 for i in range(self.D)] for j in range(self.tpop)]
    self.inicializacao()
    
    # CRITERIO DE PARADA
    for t in range(self.niter):
      self.Amedia = np.mean(self.A) # obtem media do vetor A

      # PARA CADA MORCEGO
      for i in range(self.tpop):
        self.f[i] = self.fmin + (self.fmax - self.fmin) * np.random.uniform(0,1)    	# EQUACAO (1)
        for j in range(self.D): # para cada variavel dependente da funcao
          self.v[i][j] = self.v[i][j] + (self.Sol[i][j] - self.melhor[j]) * self.f[i] 	# EQUACAO (2)
          S[i][j] = self.Sol[i][j] + self.v[i][j]                   					# EQUACAO (3)
          S[i][j] = self.ajeitaLimites(S[i][j],j)

        # REALIZA BUSCA LOCAL
        if np.random.uniform(0,1) > self.r[i]:
          for j in range(self.D):
            S[i][j] = self.melhor[j] + np.random.uniform(-1.0,1.0) * self.Amedia # MUDEI
            S[i][j] = self.ajeitaLimites(S[i][j],j)

        # OBTEM O FITNESS DO MORCEGO NESTA ATUAL POSICAO
        temp_fitness = self.Fun(self.D, S[i])

        # ATUALIZAR OU NAO O MORCEGO ATUAL - estou procurando o minmimo, por isso pegar o menor fitness
        if (temp_fitness < self.Fitness[i]) and (np.random.uniform(0,1) < self.A[i]):
          for j in range(self.D):
            self.Sol[i][j] = S[i][j]
          self.Fitness[i] = temp_fitness						# atualizacao do fitness
          self.r[i] = self.r0 * ( 1 - exp(-self.Lambda * t) )	# atualizacao da taxa de emissão de pulso
          self.A[i] = self.A[i] * self.Alfa						# atualizacao da amplitude

        # ATUALIZAR O MELHOR MORCEGO GLOBAL
        if self.Fitness[i] < self.melhorFitness:
          for j in range(self.D):
            self.melhor[j] = S[i][j]
          self.melhorFitness = self.Fitness[i]



def funcaoTeste(d,x):
  return -cos(x[0])*cos(x[1])*exp(-(x[0]-pi)**2 -(x[1]-pi)**2)

if __name__ == '__main__':
  
  while (True) :
			#(D, tpop, niter, r0, Alfa, Lambda ,fmin, fmax, limInf_, limSup_, function):
    aux = bat_algorithm(2,1000,200, 0.3, 0.9999,0.001  , 0,10000 ,-100,100,funcaoTeste)
    aux.executa()
    print (aux.melhorFitness,aux.melhor)
