import os
from operacoes_matrizes import *

def le_arquivo():
    try:
        with open('entrada.txt', "r") as file:
            content = file.readlines()
    except FileNotFoundError as e:
        os.system('cls')
        print(f"Arquivo de entrada não encontrado: {e}")
    except Exception as e:
        os.system('cls')
        print(f"Ocorreu um erro: {e}")    
    return content

def percorre_termo(termo):
    for i, char in enumerate(termo):
        if char.isalpha():
            indice = i
            break
    return indice

def verifica_fracoes(coef):
    if '/' in coef:
        num, den = coef.split('/') 
        num = float(num)
        den = float(den)
        return float(num/den)
    return coef

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
            indice = percorre_termo(termo)
            coeficiente = termo[:indice]
            variavel = termo[indice:]

            if 'x' in variavel:
                contador_variaveis +=1

            coeficiente = verifica_fracoes(coeficiente)

            if coeficiente == '':
                vetor_coeficientes_objetivo.append(1.0)
            elif coeficiente == '-':
                vetor_coeficientes_objetivo.append(-1.0)
            else:
                vetor_coeficientes_objetivo.append(float(coeficiente))
    except ValueError as e:
        print(f"Ha um problema com o arquivo de entrada: {e}")
    
    return vetor_coeficientes_objetivo, contador_variaveis

def ajusta_restricoes(arquivo, cont_variaveis):
    qtd_variaveis_folga = cont_variaveis
    restricoes = []
    
    for r in arquivo[1:]:
        r = r.strip().replace('-', '+-')
        restricoes.append(r)
        
    restricoes = [r.replace(" ", "") for r in restricoes]
    
    for i in range(len(restricoes)):
        if ">=" in restricoes[i]:
            qtd_variaveis_folga += 1
            tmp = restricoes[i].replace(">=", "-x{}=".format(qtd_variaveis_folga))
            restricoes[i] = tmp
        if "<=" in restricoes[i]:
            qtd_variaveis_folga += 1
            tmp = restricoes[i].replace("<=", "+x{}=".format(qtd_variaveis_folga))
            restricoes[i] = tmp
    
    restricoes = [r.replace('-', '+-') for r in restricoes]
    
    return restricoes, qtd_variaveis_folga

def separa_lados_restricoes(restricoes):
    lado_esq_restricao = []
    lado_dir_restricao = []
    
    for r in restricoes:
        e, d = r.split('=')
        lado_esq_restricao.append(e)
        lado_dir_restricao.append(d)
        
    return lado_esq_restricao, lado_dir_restricao

def ajusta_lado_direito_restricao(lado_dir_restricao):
    for i in range(len(lado_dir_restricao)):
        lado_dir_restricao[i] = verifica_fracoes(lado_dir_restricao[i])
    return lado_dir_restricao

def cria_matriz(tam_vetor, qtd_variaveis):
    return [[0.0 for _ in range(qtd_variaveis)] for _ in range(tam_vetor)]

def preenche_matriz_restricoes(lado_esq_restricao, qtd_variaveis):
    matriz_simplex= cria_matriz(len(lado_esq_restricao),qtd_variaveis)
    
    for i in range(len(lado_esq_restricao)):
       termos_aux = lado_esq_restricao[i].split('+')
       for termo_a in termos_aux:
        indice_a = percorre_termo(termo_a)
        coeficiente_res = termo_a[:indice_a]
        variavel_res = termo_a[indice_a:]
        indice_var = int(variavel_res[1:])
        coeficiente_res = verifica_fracoes(coeficiente_res)
        
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
    elif tipo_prob.startswith('max'):
        pass
    else:
        raise Exception("Nao foi possivel identificar o tipo da funcao, verifique o arquivo de entrada")
    
    return coef_obj

def main():
    entrada = le_arquivo()
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
    
if __name__ == '__main__':
    main()
