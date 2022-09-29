import copy
class Tabuleiro:
    # Método de inicialização
    def __init__(self, arg, pai=None, depth=0): 
        self.estado = arg
        self._findx()
        self.volta = pai
        self.filhos = []
        self.profundidade = depth

    def __copy__(self):
        return Tabuleiro(self.estado)
    def __hash__(self):
        return hash(''.join(self.estado))
    
    # Exibe a representação do tabuleiro
    def __str__(self):
        text = """┌──┬──┬──┬──┐
                  │{}│{}│{}│{}│
                  ├──┼──┼──┼──┤
                  │{}│{}│{}│{}│
                  ├──┼──┼──┼──┤
                  │{}│{}│{}│{}│
                  ├──┼──┼──┼──┤
                  │{}│{}│{}│{}│
                  └──┴──┴──┴──┘""" \
            .format(self.estado[0].rjust(2, '0'), self.estado[1].rjust(2, '0'), self.estado[2].rjust(2, '0'),
                    self.estado[3].rjust(2, '0'),
                    self.estado[4].rjust(2, '0'), self.estado[5].rjust(2, '0'), self.estado[6].rjust(2, '0'),
                    self.estado[7].rjust(2, '0'),
                    self.estado[8].rjust(2, '0'), self.estado[9].rjust(2, '0'), self.estado[10].rjust(2, '0'),
                    self.estado[11].rjust(2, '0'),
                    self.estado[12].rjust(2, '0'), self.estado[13].rjust(2, '0'), self.estado[14].rjust(2, '0'),
                    self.estado[15].rjust(2, '0')).replace("00", "  ")
        return text
    # Retorna uma sequencia de sequencia de objetos
    def __repr__(self): return str(self.estado)
    def __eq__(self, other): return self.estado == other
    def _findx(self):
        i = 0
        while self.estado[i] != '0':
            i += 1
        self.x, self.y = (int(i / 4), i % 4)

    def cap_soluc(self):
        soma = 0
        for i in range(0, 16):
            for j in range(i + 1, 16):
                if self.estado[i] > self.estado[j] and self.estado[i] != '0' and self.estado[j] != '0':
                    soma += 1
        for i in range(0, 16):
            if self.estado[i] == '0':
                a = int(i / 4) % 2 == 0
                b = not (soma % 2 == 0)
                self.solvable = (a == b)
                return self.solvable

    def getX(self): return self.x, self.y

    # Movimentos
    def _cima(self):
        jogada = copy.deepcopy(self.estado)
        rota = copy.deepcopy(self.volta)
        if rota is None: rota = ['Cima']
        else: rota.append('Cima')
        if self.x != 0:
            jogada[self.x * 4 + self.y] = jogada[(self.x - 1) * 4 + self.y]
            jogada[(self.x - 1) * 4 + self.y] = '0'
            tCima = Tabuleiro(jogada, pai=rota, depth=self.profundidade + 1)
            self.filhos.append(tCima)

    def _baixo(self):
        jogada = copy.deepcopy(self.estado)
        rota = copy.deepcopy(self.volta)
        if rota is None: rota = ['Baixo']
        else: rota.append('Baixo')
        if self.x != 3:
            jogada[self.x * 4 + self.y] = jogada[(self.x + 1) * 4 + self.y]
            jogada[(self.x + 1) * 4 + self.y] = '0'
            tBaixo = Tabuleiro(jogada, pai=rota, depth=self.profundidade + 1)
            self.filhos.append(tBaixo)
    
    def _direita(self):
        jogada = copy.deepcopy(self.estado)
        rota = copy.deepcopy(self.volta)
        if rota is None: rota = ['Direita']
        else: rota.append('Direita')
        if self.y != 3:
            jogada[self.x * 4 + self.y] = jogada[self.x * 4 + self.y + 1]
            jogada[self.x * 4 + self.y + 1] = '0'
            tDireita = Tabuleiro(jogada, pai=rota, depth=self.profundidade + 1)
            self.filhos.append(tDireita)

    def _esquerda(self):
        jogada = copy.deepcopy(self.estado)
        rota = copy.deepcopy(self.volta)
        if rota is None: rota = ['Esquerda']
        else: rota.append('Esquerda')
        if self.y != 0:
            jogada[self.x * 4 + self.y] = jogada[self.x * 4 + self.y - 1]
            jogada[self.x * 4 + self.y - 1] = '0'
            tEsquerda = Tabuleiro(jogada, pai=rota, depth=self.profundidade + 1)
            self.filhos.append(tEsquerda)

    def jogadas(self):
        if self.profundidade > 1: ultimo = self.volta[self.profundidade-1]
        else: ultimo = "0"
        if ultimo != "Direita": self._esquerda()
        if ultimo != "Esquerda": self._direita()
        if ultimo != "Baixo": self._cima()
        if ultimo != "Cima": self._baixo()
        return self.filhos