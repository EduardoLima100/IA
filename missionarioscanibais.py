import time
""" 
Solução para o problema da travessia de missionários e canibais de uma
margem para a outra do rio.
Este programa propõe uma solução para o problema utilizando a estratégia
de busca em árvore por largura.
    
Aluno: Eduardo Machado de Lima
Matrícula: 201620605
"""

"""
Parâmetros do Problema:
    Missionarios (int): Número de missionários a serem atravessados
    Canibais (int): Número de canibais a serem atravessados
    n_Barco (int): Número máximo de pessoas no barco
    OP (List): Lista com os possíveis operadores para a solução
"""

Missionarios =  3
Canibais = 3
n_Barco = 2

OP = []

for i in range(n_Barco+1):
    for j in range(n_Barco+1):
        if i+j!=0 and i+j<=n_Barco and not(j > i and i > 0):
            OP.append([i,j])

print("Possíveis barcos:",OP)

"""
NODES (List): Lista para a fila de nós da árvore gerada
T_NODES (List): Lista com todos os estados já testados
"""
NODES = []
T_NODES = []

class Margem:
    """
    Classe Margem:
        Define atributos e métodos de uma margem
    
    Atributos:
        M (int): Número de missionários na margem
        C (int): Número de canibais na margem
    """
    def __init__(self,M,C):
        self.M = M
        self.C = C
    
    def compara_Margens(margem_A,margem_B):
        """
        Método que compara os números de missionários e canibais de duas margens
        
        Argumentos:
            margem_A (Margem): Margem A a ser comparada com margem B
            margem_B (Margem): Margem B a ser comparada com margem A
        
        Retornos:
            True: Se as margens tiverem os mesmos numeros de missionários e canibais entre elas
            False: Se as margens tiverem números diferentes de missionários e canibais estre elas
        """
        if margem_A.M == margem_B.M and margem_A.C == margem_B.C:
            return True
        else:
            return False
    
    def __str__(self):
        """
        Método para definir uma representação da classe como uma string (str)
        """
        return str(self.M) + " missionários e " + str(self.C) + " canibais"

class Barco:
    """
    Classe Barco:
        Define atributos e métodos de um barco no problema proposto
    
    Atributos:
        M (int): Número de missionários no barco
        C (int): Número de canibais no barco
    """
    def __init__(self,M,C):
        self.M = M
        self.C = C
    
    def atravessa(self,margem_A,margem_B):
        """
        Metodo para remover os missionários e canibais de uma margem e 
        adicioná-los à outra
        Calcula novas margens após aplicação do operador
        
        Argumentos:
            margem_A (Margem): Ponteiro da margem de embarque
            margem_B (Margem): Ponteiro da margem de desembarque
        
        """
        margem_A.M = margem_A.M - self.M
        margem_A.C = margem_A.C - self.C
        margem_B.M = margem_B.M + self.M
        margem_B.C = margem_B.C + self.C

class Estado:
    """
    Classe Estado:
        Define atributos e métodos necessários para descrever um dos possíveis
        estados e para encontrar as possibilidades que ele é capaz de gerar
    
    Atributos de inicialização:
        margem_E (Margem): Margem esquerda do estado
        margem_D (Margem): Margem direita do estado
        rodada (int): Camada da árvore que esse estado se encontra
    
    Atributos:
        valido (bool): Indica se o estado é válido de acordo com o problema proposto
        is_Objetivo (bool): Indica se o estado é o objetivo a ser atingido pela solução do problema proposto
        P (List): Lista que guardará os nós filhos gerados pelo estado
        OPRS (List): Lista dos operadores que geraram o estado a partir do estado inicial
    """
    def __init__(self,margem_E,margem_D,rodada):
        self.margem_E = margem_E
        self.margem_D = margem_D
        self.rodada = rodada

        self.valido = self.teste_Estado()
        self.is_Objetivo = self.teste_Objetivo()
        self.P = []
        self.OPRS = []
        
    
    def teste_Estado(self):
        """
        Método para informar se o estado é válido de acordo com o problema proposto
        
        Retornos:
            False:
                Se missionários ficarem em menor número em alguma margem do estado
                Se não houver missionários ou canibais suficientes na margem de embarque para que o operador seja aplicado
            True:
                Se o estado estiver de acordo com todas as regras do problema proposto
        """
        if((self.margem_E.C > self.margem_E.M and self.margem_E.M > 0) or (self.margem_D.C > self.margem_D.M and self.margem_D.M > 0)) :
            return False
        elif((self.margem_E.C < 0) or (self.margem_E.M < 0) or (self.margem_D.C < 0) or (self.margem_D.M < 0)):
            return False
        else:
            return True
    
    def teste_Objetivo(self):
        """
        Método para informar se o estado é o objetivo a ser atingido pela solução do problema proposto
        
        Retornos:
            True: Se todos os missionários e canibais do problema estiverem na margem esquerda
            False: Se todos os missionários e canibais do problema ainda não estiverem na margem esquerda
        """
        if self.margem_E.C == Canibais and self.margem_E.M == Missionarios:
            return True
        else:
            return False
        
    def set_Possibs(self):
        """
        Método adiciona todas as possibilidades válidas, geradas pelos operadores do 
        problema, à lista P 
        """
        for op in OP:
            barco = Barco(op[0],op[1])
            
            margem_D = Margem(self.margem_D.M,self.margem_D.C)
            margem_E = Margem(self.margem_E.M,self.margem_E.C)
                        
            if self.rodada % 2 == 0:
                barco.atravessa(margem_D,margem_E)
                
            else:
            	barco.atravessa(margem_E,margem_D)
            
            new = Estado(margem_E,margem_D,self.rodada+1)
            
            if(new.valido):
                for j in self.OPRS:
                    new.OPRS.append(j)
                new.OPRS.append(op)
                self.P.append(new)
    
    def compara_Estados(estado_A, estado_B):
        """
        Método que compara as margens de dois estados
        
        Argumentos:
            estado_A (Estado): Estado A a ser comparado com estado B
            estado_B (Estado): Estado B a ser comparado com estado A
        
        Retornos:
            True: Se os estados tiverem as mesmas margens entre eles
            False: Se os estados tiverem margens diferentes entre eles
        """
        if Margem.compara_Margens(estado_A.margem_D,estado_B.margem_D) and Margem.compara_Margens(estado_A.margem_E,estado_B.margem_E):
            return True
        else:
            return False
    
    def __str__(self):
        """
        Método para definir uma representação da classe como uma string (str)
        """
        return "Operadores:" + str(self.OPRS) + "\nMargem Esquerda: " + str(self.margem_E) + "\nMargem Direita: " + str(self.margem_D) + "\nRodada: " + str(self.rodada)

def main():
    """
    Cria estado inicial, adiciona-o à fila de nós e inicia a varredura 
    a procura do estado inicial, enquanto adiciona novos estados na fila
    para também serem testados
    """
    estado_Inicial = Estado(Margem(0,0),Margem(Missionarios,Canibais),0)
    NODES.append(estado_Inicial)
    
    rod_Ant = 0
    cont = 0
    loop = True
    while loop: #cont <= len(NODES): #Enquanto não chegar no fim da fila
        if len(NODES)>0:
            if NODES[0].is_Objetivo: #Se o nó sendo testado for o objetivo do problema proposto
                """
                Imprime a declaração de sucesso, o estado encontrado, a quantidade 
                de nós testados e finaliza a fila de nós
                """
                print("Objetivo encontrado!")
                print(NODES[0])
                print("Na tentativa:",cont)
                loop = False#cont = len(NODES) + 1
                                
            else:   #Se ainda não for o objetivo
                #Adiciona os nós filhos à fila de nós
                
                NODES[0].set_Possibs()
                
                for p in NODES[0].P:
                    f = 0
                    for n in T_NODES:
                        if Estado.compara_Estados(NODES[0],n) and NODES[0].rodada%2 == n.rodada%2 and NODES[0].rodada>n.rodada:
                            f = 1
                    if f == 0:    
                        NODES.append(p)
                    
            if NODES[0].rodada > rod_Ant:
                rod_Ant = NODES[0].rodada
                print(time.strftime("\n[%H:%M:%S]"))
                print(NODES[0].rodada)
                print("Testadas:",cont, "possibilidades")
                print(len(NODES)-len(NODES[0].P), "possibilidades a serem testadas\n")
            
            T_NODES.append(NODES[0])
            #print(NODES[0])
            NODES.remove(NODES[0])
            cont = cont + 1
        else:
            print("Todas as possibilidades foram testadas\nSolução não existe")
            loop = False
                        
        
    NODES.clear()
if __name__ == "__main__":
    main()
    print("\nMissionários:",Missionarios)
    print("Canibais:",Canibais)
    print("Max no barco:",n_Barco)
    print("Possíveis barcos:",OP)
        



