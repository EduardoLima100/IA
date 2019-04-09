#import time
#missionarioscanibais.py

Missionarios = 3
Canibais = 3
NODES = []

class Margem:
    def __init__(self,M,C):
        self.M = M
        self.C = C
    
    def compara_Margens(margem_A,margem_B):
        if margem_A.M == margem_B.M and margem_A.C == margem_B.C:
            return True
        else:
            return False
    
    def __str__(self):
        return str(self.M) + " missionários e " + str(self.C) + " canibais"

class Barco:
    def __init__(self,M,C):
        self.M = M
        self.C = C
    
    def atravessa(self,margem_A,margem_B):
        margem_A.M = margem_A.M - self.M
        margem_A.C = margem_A.C - self.C
        margem_B.M = margem_B.M + self.M
        margem_B.C = margem_B.C + self.C

class EstadoPai:
    def __init__(self,margem_E,margem_D):
        self.margem_E = margem_E
        self.margem_D = margem_D

class Estado:
    def __init__(self,margem_E,margem_D,rodada):
        self.i = 0
        self.estado_Pai = EstadoPai(Margem(0,0),Margem(0,0))
        self.margem_E = margem_E
        self.margem_D = margem_D
        self.rodada = rodada
        self.valido = self.teste_Estado()
        self.P = []
        self.is_Objetivo = self.teste_Objetivo()
        self.OPRS = []
        
    
    def teste_Estado(self):
        if((self.margem_E.C > self.margem_E.M and self.margem_E.M > 0) or (self.margem_D.C > self.margem_D.M and self.margem_D.M > 0)) :
            #print("Missionário Morre")
            return False
        elif((self.margem_E.C < 0) or (self.margem_E.M < 0) or (self.margem_D.C < 0) or (self.margem_D.M < 0)):
            #print("Não tem gente suficiente")
            return False
        else:
            if Estado.compara_Estados(self.estado_Pai,self):
                return False
            
            else:
                #print("Válido")
                return True
    
    def teste_Objetivo(self):
        if self.margem_E.C == Canibais and self.margem_E.M == Missionarios:
            return True
        else:
            return False
        
    def set_Possibs(self):
        OP = [[0,1],[1,0],[1,1],[0,2],[2,0]]
        
        i = 0
        for op in OP:
            #print(op)
            barco = Barco(op[0],op[1])
            
            margem_D = Margem(self.margem_D.M,self.margem_D.C)
            margem_E = Margem(self.margem_E.M,self.margem_E.C)
                        
            if self.rodada % 2 == 0:
                barco.atravessa(margem_D,margem_E)
                
            else:
            	barco.atravessa(margem_E,margem_D)
            
            new = Estado(margem_E,margem_D,self.rodada+1)
            
            if(new.valido):
                new.i = i
                new.estado_Pai = EstadoPai(self.margem_E,self.margem_D)
                for j in self.OPRS:
                    new.OPRS.append(j)
                new.OPRS.append(op)
                self.P.append(new)
                
                i = i + 1
    
    def compara_Estados(estado_A, estado_B):
        if Margem.compara_Margens(estado_A.margem_D,estado_B.margem_D) and Margem.compara_Margens(estado_A.margem_E,estado_B.margem_E):
            return True
        else:
            return False
    
    def __str__(self):
        return "Operadores:" + str(self.OPRS) + "\nMargem Esquerda: " + str(self.margem_E) + "\nMargem Direita: " + str(self.margem_D) + "\nRodada: " + str(self.rodada)

estado_Inicial = Estado(Margem(0,0),Margem(Missionarios,Canibais),0)
NODES.append(estado_Inicial)

cont = 0
while cont < len(NODES):
    if len(NODES)%1000 == 0:
        print("Testadas: ",len(NODES), " possibilidades")
    #print(NODES[cont])
    if NODES[cont].is_Objetivo:
        print("Objetivo encontrado\n", NODES[cont])
        cont = len(NODES) + 1
    else:
        NODES[cont].set_Possibs()
        #print("Possibilidades: ", len(NODES[cont].P))
        for p in NODES[cont].P:
            NODES.append(p)
    cont = cont + 1
    #time.sleep(0.01)
    



