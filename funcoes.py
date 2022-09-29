from collections import deque

class MinHeap:
    def __init__(self, objetivo, comparar):
        self.data = [None]
        self.size = 0
        self.comparador = comparar
        self.objetivo = objetivo

    def __len__(self): return self.size
    def __contains__(self, item): return item in self.data
    def __str__(self): return str(self.data)

    def _comparar(self, x, y):
        x = self.comparador(self.data[x], self.objetivo)
        y = self.comparador(self.data[y], self.objetivo)
        if x < y: return True
        else: return False

    def getpos(self, x):
        for i in range(self.size+1):
            if x == self.data[i]: return i
        return None

    def _cimaHeap(self, i):
        while i > 1 and self._comparar(i, int(i/2)):
            self._troca(i, int(i/2))
            i = int(i/2)

    def _baixoHeap(self, i):
        size = self.size
        while 2*i <= size:
            j = 2*i
            if j < size and self._comparar(j+1, j):
                j += 1
            if self._comparar(i, j):
                break
            self._troca(i, j)
            i = j

    def _troca(self, i, j):
        t = self.data[i]
        self.data[i] = self.data[j]
        self.data[j] = t

    def push(self, x):
        self.size += 1
        self.data.append(x)
        self._cimaHeap(self.size)

    def pop(self):
        if self.size < 1:
            return None
        t = self.data[1]
        self.data[1] = self.data[self.size]
        self.data[self.size] = t
        self.size -= 1
        self._baixoHeap(1)
        self.data.pop()
        return t

    def peek(self):
        if self.size < 1:
            return None
        return self.data[1]

# comparadores
def hamming(estado_inicial, estado_objetivo):
    inicial = estado_inicial.estado
    objetivo = estado_objetivo.estado
    depth = estado_inicial.profundidade
    soma = 0
    for x, y in zip(objetivo, inicial):
        if x != y and x != '0':
            soma += 1
    return soma + depth

def manhattan(estado_inicial, estado_objetivo):
    inicial = estado_inicial.estado
    objetivo = estado_objetivo.estado
    depth = estado_inicial.profundidade
    soma = 0
    for i in range(16):
        if objetivo[i] == '0':
            continue
        x1, y1 = (int(i / 4), i % 4)
        for j in range(16):
            if objetivo[i] == inicial[j]:
                x2, y2 = (int(j / 4), j % 4)
                soma += abs(x1 - x2) + abs(y1 - y2)
                break
    return soma + depth


# Implementação dos algoritmos de Busca

# Busca em largura --> Breadth-first search (bfs)
def bfs(estado_inicial, estado_objetivo):
    total_nos = 1
    fronteira = deque()
    fronteira.append(estado_inicial)

    while len(fronteira) > 0:
        state = fronteira.popleft()

        if estado_objetivo == state:
            return state.backtrack, total_nos
        for filho in state.moves():
            total_nos += 1
            fronteira.append(filho)
        del(state);
    return False, total_nos

# Busca em profundidade --> Depth-first search (dfs)
def dfs(estado_inicial, estado_objetivo, depth):
    total_nos = 1
    fronteira = list()
    visitados = set()
    fronteira.append(estado_inicial)

    while len(fronteira) > 0:
        estado = fronteira.pop()
        visitados.add(estado)

        if estado == estado_objetivo:
            return estado.backtrack, total_nos

        for filho in estado.jogadas():
            total_nos += 1
            if filho.profundidade <= depth:
                if filho not in visitados or filho not in fronteira:
                    fronteira.append(filho)
        del(estado)
    return False, total_nos

# Busca gulosa
def gulosa(estado_inicial, estado_objetivo, comparador):
    total_nos = 1
    estado = estado_inicial

    while estado != estado_objetivo:
        filhos = estado.jogadas()
        estado = filhos.pop()
        for x in filhos:
            total_nos += 1
            if comparador(x, estado_objetivo) < comparador(estado, estado_objetivo):
                estado = x
    return estado.backtrack, total_nos

# Busca A*
def a_estrela(estado_inicial, estado_objetivo, comparador):
    total_nos = 1
    fronteira = MinHeap(estado_objetivo, comparador)
    fronteira.push(estado_inicial)
    visitados = set()

    while len(fronteira) > 0:
        estado = fronteira.pop()
        visitados.add(estado)

        if estado_objetivo == estado:
            return estado.backtrack, total_nos

        for filho in estado.jogadas():
            total_nos += 1
            if filho not in fronteira and filho not in visitados:
                fronteira.push(filho)
            elif filho in fronteira:
                i = fronteira.getpos(filho)
                if fronteira.data[i].profundidade > filho.profundidade:
                    fronteira.data[i] = filho
                    fronteira._cimaHeap(i)
    return False, total_nos