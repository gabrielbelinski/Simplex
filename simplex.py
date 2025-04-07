def le_arquivo():
    try:
        # Leitura do arquivo txt
        file = open("entrada.txt", "r")
        content = file.readlines()
        file.close()
    except FileNotFoundError:
        raise FileNotFoundError("Arquivo de entrada não encontrado!")
    
    return content

def salva_arquivo():
    pass

def tipo_problema():
    pass

def maximizar_funcao():
    pass

def minimizar_funcao():
    pass
    
def extrai_coeficientes():
    pass

def padroniza_variaveis_de_folga():
    pass

def gauss():
    pass

def simplex():
    pass

def main():
    problema = le_arquivo()

if __name__ == '__main__':
    main()