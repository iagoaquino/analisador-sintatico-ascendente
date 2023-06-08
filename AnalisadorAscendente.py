from tabulate import tabulate
from classes.automato import Automato
from classes.token import Token
alfabeto = "ifthenab"
class AnalisadorAscendente:
    def __init__(self,automato):
        self.tabelaNumero = []
        self.tabelaAcao = []
        self.tabelaTransicao = []
        self.automato = automato
        self.entrada = ""
        self.token = Token("NULL","NULL")
        for i in range(9):
            linha = []
            for j in range(5):
                linha.append("[][]")
            self.tabelaNumero.append(linha)

        for i in range(9):
            linha = []
            for j in range(5):
                linha.append("[][]")
            self.tabelaAcao.append(linha)
        
        for i in range(9):
            linha = []
            for j in range(3):
                linha.append("[][]")
            self.tabelaTransicao.append(linha)
            
    def set_entrada(self,entrada):
        self.entrada = entrada
    
    def formarTabelas(self):
        self.tabelaAcao[0][0] = "shift"
        self.tabelaAcao[0][3] = "shift"
        self.tabelaAcao[1][4] = "aceite"
        self.tabelaAcao[2][2] = "shift"
        self.tabelaAcao[3][4] = "reduct"
        self.tabelaAcao[4][4] = "reduct"
        self.tabelaAcao[5][1] = "shift"
        self.tabelaAcao[6][1] = "reduct"
        self.tabelaAcao[7][3] = "shift"
        self.tabelaAcao[8][4] = "reduct"
        self.tabelaNumero[0][0] = 2
        self.tabelaNumero[0][3] = 4
        self.tabelaNumero[1][4] = 0
        self.tabelaNumero[2][2] = 6
        self.tabelaNumero[3][4] = 2
        self.tabelaNumero[4][4] = 4
        self.tabelaNumero[5][1] = 7
        self.tabelaNumero[6][1] = 3
        self.tabelaNumero[7][3] = 4 
        self.tabelaNumero[8][4] = 1
        self.tabelaTransicao[0][1] = 3
        self.tabelaTransicao[0][2] = 1
        self.tabelaTransicao[2][0] = 5
        self.tabelaTransicao[7][1] = 8
        print(tabulate(self.tabelaAcao))
        print(tabulate(self.tabelaNumero))
        print(tabulate(self.tabelaTransicao))

def criarAutomato(quantidade_estados,alfabeto):
    automato = Automato(alfabeto,quantidade_estados)
    # criando a transição do token 'if'

    automato.adicionar_transicao(0,"i",1)
    automato.adicionar_transicao(1,"f",2)
    # criando a transição do token 'then'

    automato.adicionar_transicao(0,"t",3)
    automato.adicionar_transicao(3,"h",4)
    automato.adicionar_transicao(4,"e",5)
    automato.adicionar_transicao(5,"n",6)

    # criando a transição do token a
    automato.adicionar_transicao(0,"a",7)

    # criando a transição do tokenb b
    automato.adicionar_transicao(0,"b",8)

    #definindo os estados de aceitação
    automato.definir_aceitacao(2)
    automato.definir_aceitacao(6)
    automato.definir_aceitacao(7)
    automato.definir_aceitacao(8)

    return automato
# a função retorna criar_automato um automato que é passada para o construtor da classe
analisador1 = AnalisadorAscendente(criarAutomato(9,alfabeto))
analisador1.formarTabelas()