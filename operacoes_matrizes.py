def inversa(matriz_simplex):
    pass

def determinante(matriz_simplex):
    n = len(matriz_simplex)
    if n == 1:
        return matriz_simplex[0][0]
    if n == 2:
        return matriz_simplex[0][0] * matriz_simplex[1][1] - matriz_simplex[1][0]
    
    det_total = 0
    for j in range(n):
        elemento = matriz_simplex[0][j]
        menor = [linha[:j] + linha[j+1:] for linha in matriz_simplex[1:]]
        cofator = -1**(0+j) * determinante(menor)
        det_total += elemento * cofator

    return det_total

def multiplicacao(matriz_a, matriz_b):
    l_a = len(matriz_a)
    c_a = len(matriz_a[0])
    l_b = len(matriz_b)
    c_b = len(matriz_b[0])

    assert c_a == l_b, "Numero de colunas de A deve ser igual ao numero de linhas de B"
    resultado = [[0.0 for _ in range(l_a)] for _ in range(c_b)]

    for i in range(l_a):
        for j in range(c_b):
            for k in range(c_a):
                resultado[i][j] += matriz_a[i][k] * matriz_b[k][j]
    
    return resultado

    