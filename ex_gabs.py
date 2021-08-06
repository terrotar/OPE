from collections import deque


class Fila:
    def __init__(self):
        self.itens = deque()

    def insere(self, e):
        self.itens.append(e)

    def remove(self):
        return self.itens.popleft()

    def __len__(self):
        return len(self.itens)

    def proximo(self):
        prox = self.itens.popleft()
        self.itens.appendleft(prox)
        return prox


class Pilha:
    def __init__(self):
        self.itens = []
        self.tamanho = 0

    def insere(self, e):
        self.itens.append(e)
        self.tamanho += 1

    def remove(self):
        self.tamanho -= 1
        return self.itens.pop()

    def topo(self):
        return self.itens[-1]

    def __len__(self):
        return self.tamanho


f1 = Fila()

f1.insere(1)
f1.insere(9)
f1.insere(0)
f1.insere(3)
f1.insere(2)
f1.insere(4)
f1.insere(6)


p1 = Pilha()

p1.insere(1)
p1.insere(9)
p1.insere(0)
p1.insere(3)
p1.insere(2)
p1.insere(4)
p1.insere(6)


def desafio_final(fila, pilha):
    # retornar maior par da Fila
    maior_par_fila = -1
    for i in range(len(f1)):
        if (i % 2 == 0) and (i > maior_par_fila):
            maior_par_fila = i
    # menor impar da Pilha
    menor_impar_pilha = 99
    for i in range(len(p1)):
        if (i % 2 != 0) and (i < menor_impar_pilha):
            menor_impar_pilha = i
    return (maior_par_fila + menor_impar_pilha)


print(desafio_final(f1, p1))
