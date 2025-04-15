def inversa(matriz_simplex):
    n = len(matriz_simplex)
    mt_aumentada = [[0.0 for _ in range(n*2)] for _ in range((n))]

    for i in range(n):
        for j in range(n):
            mt_aumentada[i][j] = matriz_simplex[i][j]
        for j in range(n, n*2):
            mt_aumentada[i][j] = 1 if j == i+n else 0

    for k in range(n):
        if mt_aumentada[k][k] == 0:
            encontrou = False
            for i in range(k+1, n):
                if mt_aumentada[i][k] != 0:
                    mt_aumentada[k], mt_aumentada[i] = mt_aumentada[i], mt_aumentada[k]
                    encontrou = True
                    break
            assert encontrou is not False, "Nao é possivel inverter a matriz, pois ela nao é singular"

        pivo = mt_aumentada[k][k]
        for j in range(k, n*2):
            mt_aumentada[k][j] /= pivo
        
        for i in range(n):
            if i != k:
                fator = mt_aumentada[i][k]
                for j in range(k, n*2):
                    mt_aumentada[i][j] -= fator * mt_aumentada[k][j]

    mt_inversa = [[0.0 for _ in range(n)] for _ in range((n))]
    for i in range(n):
        for j in range(n):
            mt_inversa[i][j] = mt_aumentada[i][j+n]
    
    return mt_inversa
            
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