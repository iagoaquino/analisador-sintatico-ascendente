from tabulate import tabulate
from classes.automato import Automato
from classes.token import Token
from classes.arvore import *

alfabeto = "ifthenab "
class AnalisadorAscendente:
    def __init__(self,automato):
        self.tabelaNumero = []
        self.tabelaAcao = []
        self.tabelaTransicao = []
        self.automato = automato
        self.entrada = ""
        self.posicao = 0
        self.pilhaEstado = []
        self.pilhaNo = []
        self.pilhaAcao = []
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

    def set_token(self,token):
        self.token = token

    def buscar_transicao_coluna(self,entrada):
        if entrada == "E":
            return 0
        elif entrada == "C":
            return 1
        elif entrada == "S":
            return 2
        return 404
    
    def fazer_transicao(self,entrada):
        linha = self.pilhaEstado[-1]
        coluna = self.buscar_transicao_coluna(entrada)
        self.pilhaEstado.append(self.tabelaTransicao[linha][coluna])
        
    def reduct1(self):
        no_pai = No("S")
        for i in range(4):
            no_pai.filhos.append(self.pilhaNo[-1])
            self.pilhaNo.pop()
            self.pilhaEstado.pop()
        
        no_pai.filhos.reverse()
        self.pilhaNo.append(no_pai)
        self.fazer_transicao("S")
    
    def reduct2(self):
        no_pai = No("S")
        no_pai.filhos.append(self.pilhaNo[-1])
        self.pilhaNo.pop()
        self.pilhaEstado.pop()
        self.pilhaNo.append(no_pai)
        self.fazer_transicao("S")

    def reduct3(self):
        no_pai = No("E")
        no_pai.filhos.append(self.pilhaNo[-1])
        self.pilhaNo.pop()
        self.pilhaEstado.pop()
        self.pilhaNo.append(no_pai)
        self.fazer_transicao("E")
    
    def reduct4(self):
        no_pai = No("C")
        no_pai.filhos.append(self.pilhaNo[-1])
        self.pilhaNo.pop()
        self.pilhaEstado.pop()
        self.pilhaNo.append(no_pai)
        self.fazer_transicao("C")

    def formar_token(self,estado_atual,valor_token):
        token = Token("NULL","NULL")
        if estado_atual == 2:
            token.tipo = "if"
            token.valor = "if"
        if estado_atual == 6:
            token.tipo = "then"
            token.valor = "then"
        if estado_atual == 7:
            token.tipo = "a"
            token.valor = "a"
        if estado_atual == 8:
            token.tipo = "b"
            token.valor = "b"
        return token
    
    def get_next_token(self):
        if self.posicao == len(self.entrada):
            token = Token("$","$")
            self.set_token(token)
        else:
            atual_position = self.posicao
            estado_atual = 0
            valor_token = ""
            while atual_position != len(self.entrada):
                validador = 0
                if self.entrada[atual_position] != " ":
                    valor_token = valor_token+self.entrada[atual_position]
                estado_atual,validador = self.automato.fazer_transicao(estado_atual,self.entrada[atual_position])
                if self.automato.checar_aceitacao(estado_atual) == 1:
                    self.set_token(self.formar_token(estado_atual,valor_token))
                    estado_atual = 0
                    self.posicao = atual_position+1
                    break
                if validador == 0:
                    return 0
                atual_position += 1

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

    def buscarSimbolo(self,texto):
        if texto == "if":
            return 0
        elif texto == "then":
            return 1
        elif texto == "a":
            return 2
        elif texto == "b":
            return 3
        elif texto == "$":
            return 4 
        return 404
    
    def fazerAnalise(self):
        self.pilhaEstado.append(0)
        self.get_next_token()
        while 1:
            row_table = []
            linha = self.pilhaEstado[-1]
            coluna = self.buscarSimbolo(self.token.valor)
            acao = self.tabelaAcao[linha][coluna]
            numero = self.tabelaNumero[linha][coluna]
            row_table.append(self.pilhaEstado)
            row_table.append(self.token.valor+self.entrada[self.posicao:len(self.entrada)])
            row_table.append(acao+str(numero))
            nos = []
            for no in self.pilhaNo: 
                nos.append(no.valor)
            row_table.append(nos)
            print(tabulate(row_table))
            if acao == "aceite":
                break
            if acao == "shift":
                self.pilhaEstado.append(numero)
                no = No(self.token.valor)
                self.pilhaNo.append(no)
                self.get_next_token()
            if acao == "reduct":
                if numero == 1:
                    self.reduct1()
                elif numero == 2:
                    self.reduct2()
                elif numero == 3:
                    self.reduct3()
                elif numero == 4:
                    self.reduct4()

            
            
        print(self.token.valor)


def criarAutomato(quantidade_estados,alfabeto):
    automato = Automato(alfabeto,quantidade_estados)
    #tratamento do " "
    automato.adicionar_transicao(0," ",0)

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
analisador1.set_entrada("if a then b")
analisador1.fazerAnalise()