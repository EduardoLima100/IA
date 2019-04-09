import time
#missionarioscanibais.py

Missionarios = 3
Canibais = 3

class Margem:
    def __init__(self,M,C):
        self.M = M
        self.C = C
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

class Estado:
    i = 0
    def __init__(self,margem_E,margem_D,rodada):
        self.margem_E = margem_E
        self.margem_D = margem_D
        self.rodada = rodada
        self.valido = self.teste_Estado()
        self.P = []
        self.is_Objetivo = self.teste_Objetivo()
        
    def teste_Estado(self):
        if((self.margem_E.C > self.margem_E.M and self.margem_E.M > 0) or (self.margem_D.C > self.margem_D.M and self.margem_D.M > 0)) :
            #print("Missionário Morre")
            return False
        elif((self.margem_E.C < 0) or (self.margem_E.M < 0) or (self.margem_D.C < 0) or (self.margem_D.M < 0)):
            #print("Não tem gente suficiente")
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
                self.P.append(new)
                i = i + 1
    
    def __str__(self):
        return "Opção:" + str(self.i) + "\nMargem Esquerda: " + str(self.margem_E) + "\nMargem Direita: " + str(self.margem_D) + "\nRodada: " + str(self.rodada)


def percorre(P):
    if P[0].is_Objetivo:
        print("Objetivo")
        return None
    else:
        P[0].set_Possibs()
        if len(P[0].P)>1:
            for p in P[0].P:
                print(p)
                P.append(p)
        P.remove(P[0])
        time.sleep(1)
        percorre(P)
            
            
    

estado_Inicial = Estado(Margem(0,0),Margem(Missionarios,Canibais),0)
P = [estado_Inicial]
percorre(P)




