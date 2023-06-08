class No:
    def __init__(self,valor):
        self.filhos = []
        self.valor = valor
class Arvore:
    def __init__(self):
        self.tamanho = 0
    def definir_raiz(self,no):
        if self.tamanho == 0:
            self.raiz = no
    def mostrar_arvore(self,no):
        if type(no) is not str:
            nome = "pai:"+no.valor+",filhos("
            for filho in no.filhos:
                if type(filho) == str:
                    nome = nome +" "+filho
                else:
                    nome = nome +" "+filho.valor+" "
            print(nome +")")
            for filho in no.filhos:
                self.mostrar_arvore(filho)




        
