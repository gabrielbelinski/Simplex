import sys
import os
from operacoes_matrizes import *
def le_arquivo():
    try:
        # Leitura do arquivo txt
        with open(sys.argv[1], "r") as file:
            content = file.readlines()
    except IndexError:
        os.system('cls')
        raise IndexError("Por favor digite o nome do arquivo ao executar o Simplex!")
    except FileNotFoundError:
        os.system('cls')
        raise FileNotFoundError("Arquivo de entrada não encontrado!")
    return content

def extrai_coeficientes_fc_objetivo(arquivo):
    try:
        termos_fc_objetivo = []
        vetor_coeficientes_objetivo = []
        contador_variaveis = 0
        _, fc_objetivo = arquivo[0].split('=')
        fc_objetivo = fc_objetivo.strip()
        if '-' in fc_objetivo:
            fc_objetivo = fc_objetivo.replace('-', '+-')
        termos_fc_objetivo = [t.replace(' ', '') for t in fc_objetivo.split('+')]
        for termo in termos_fc_objetivo:
            if termo == '':
                continue
            for i, char in enumerate(termo):
                if char.isalpha():
                    idx = i
                    contador_variaveis += 1
                    break
            coeficiente = termo[:idx]

            if '/' in coeficiente:
                num, den = coeficiente.split('/') 
                num = float(num)
                den = float(den)
                coeficiente = float(num/den)

            if coeficiente == '':
                vetor_coeficientes_objetivo.append(1.0)
            elif coeficiente == '-':
                vetor_coeficientes_objetivo.append(-1.0)
            else:
                vetor_coeficientes_objetivo.append(float(coeficiente))
    except:
        raise ValueError("Ha um problema com o arquivo de entrada!")
    
    return vetor_coeficientes_objetivo, contador_variaveis

def ajusta_restricoes(arquivo, cont_variaveis):
    qtd_variaveis_folga = cont_variaveis
    restricoes = [r.strip().replace('-', '+-') for r in arquivo[1:]]
    restricoes = [r.replace(" ", "") for r in restricoes]
    for i in range(len(restricoes)):
        if ">=" in restricoes[i]:
            qtd_variaveis_folga += 1
            newstring = restricoes[i].replace(">=", "-x{}=".format(qtd_variaveis_folga))
            restricoes[i] = newstring
        if "<=" in restricoes[i]:
            qtd_variaveis_folga += 1
            newstring = restricoes[i].replace("<=", "+x{}=".format(qtd_variaveis_folga))
            restricoes[i] = newstring
    restricoes = [r.replace('-', '+-') for r in restricoes]
    return restricoes, qtd_variaveis_folga

def separa_lados_restricoes(restricoes):
    lado_esquerdo_restricao = []
    lado_direito_restricao = []
    for r in restricoes:
        e, d = r.split('=')
        lado_esquerdo_restricao.append(e)
        lado_direito_restricao.append(d)
    return lado_esquerdo_restricao, lado_direito_restricao

def ajusta_lado_direito_restricao(lado_direito_restricao):
    for i in range(len(lado_direito_restricao)):
        if '/' in lado_direito_restricao[i]:
            num, den = lado_direito_restricao[i].split('/') 
            num = float(num)
            den = float(den)
            lado_direito_restricao[i] = float(num/den)
    return lado_direito_restricao


def cria_matriz(tam_vetor, qtd_variaveis):
    return [[0.0 for _ in range(qtd_variaveis)] for _ in range(tam_vetor)]

def preenche_matriz_restricoes(lado_esquerdo_restricao, qtd_variaveis):
    matriz_simplex= cria_matriz(len(lado_esquerdo_restricao),qtd_variaveis)
    for i in range(len(lado_esquerdo_restricao)):
       #lado_esquerdo_restricao[i] = lado_esquerdo_restricao[i].replace('-','+-')
       termos_aux = lado_esquerdo_restricao[i].split('+')
       for termo_a in termos_aux:
        termo_a = termo_a.strip()
        if termo_a == '':
            continue
        for i_a, char_a in enumerate(termo_a):
            if char_a.isalpha():
                idx_a = i_a
                break
        coeficiente_res = termo_a[:idx_a]
        variavel_res = termo_a[idx_a:]
        indice_var = int(variavel_res[1:])

        if '/' in coeficiente_res:
            num, den = coeficiente_res.split('/') 
            num = float(num)
            den = float(den)
            coeficiente_res = float(num/den)
        
        if coeficiente_res == '':
            matriz_simplex[i][indice_var-1] = 1.0
        elif coeficiente_res == '-':
            matriz_simplex[i][indice_var-1] = -1.0
        else:
            matriz_simplex[i][indice_var-1] = float(coeficiente_res)

    return matriz_simplex

def tipo_problema(entrada, coef_obj):
    tipo_prob, _ = entrada[0].split('=')
    tipo_prob = tipo_prob.lower()
    if tipo_prob.startswith('min'):
        for i in range(len(coef_obj)):
            coef_obj[i] = coef_obj[i] * (-1.0)
    return coef_obj

    
def main():
    entrada = le_arquivo()
    try:
        coef_obj, qtd_variaveis = extrai_coeficientes_fc_objetivo(entrada)
        coef_obj = tipo_problema(entrada, coef_obj)
        restricoes, qtd_variaveis = ajusta_restricoes(entrada, qtd_variaveis)
        coef_obj[len(coef_obj)+1:] = [0]*(qtd_variaveis - len(coef_obj))
        esq_rst, dir_rst = separa_lados_restricoes(restricoes)
        dir_rst = ajusta_lado_direito_restricao(dir_rst)
        matriz = preenche_matriz_restricoes(esq_rst, qtd_variaveis)
        print(coef_obj)
        print(matriz)
        print(dir_rst)
    except:
        raise Exception("Nao foi possivel executar o Simplex")
if __name__ == '__main__':
    main()
