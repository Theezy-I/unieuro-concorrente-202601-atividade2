import time
import concurrent.futures

def calcular_soma_parcial(pedaco):
    """Função que cada processo vai executar para somar o seu pedaço"""
    return sum(pedaco)

def ler_arquivo(nome_arquivo):
    print(f"A ler o ficheiro {nome_arquivo} (isto pode demorar alguns segundos)...")
    with open(nome_arquivo, 'r') as f:
        # Lê todas as linhas e converte para número inteiro
        numeros = [int(linha) for linha in f]
    return numeros

def executar_teste(numeros):
    resultados_tempo = {}
    
    # --- 1. TESTE SERIAL (1 Processo) ---
    print("\n[+] A iniciar Teste Serial (1 Processo)...")
    inicio = time.time()
    soma_total = sum(numeros) # A função sum() nativa do Python faz o papel serial
    fim = time.time()
    
    tempo_serial = fim - inicio
    resultados_tempo[1] = tempo_serial
    print(f"Soma: {soma_total} | Tempo: {tempo_serial:.4f} segundos")

    # --- 2. TESTES PARALELOS (2, 4, 8, 12 Processos) ---
    processos_para_testar = [2, 4, 8, 12]
    tamanho_total = len(numeros)

    for p in processos_para_testar:
        print(f"\n[+] A iniciar Teste Paralelo ({p} Processos)...")
        
        # A dividir a lista gigante de números em 'p' pedaços iguais
        tamanho_pedaco = tamanho_total // p
        pedacos = []
        for i in range(p):
            inicio_idx = i * tamanho_pedaco
            # O último processo fica com o que sobrar no final da lista
            fim_idx = tamanho_total if i == p - 1 else inicio_idx + tamanho_pedaco
            pedacos.append(numeros[inicio_idx:fim_idx])

        # Começa a contar o tempo do paralelo
        inicio = time.time()
        
        # A magia do paralelismo acontece aqui
        with concurrent.futures.ProcessPoolExecutor(max_workers=p) as executor:
            resultados = executor.map(calcular_soma_parcial, pedacos)
            soma_total = sum(resultados)
            
        # Termina de contar o tempo
        fim = time.time()
        
        tempo_paralelo = fim - inicio
        resultados_tempo[p] = tempo_paralelo
        print(f"Soma: {soma_total} | Tempo: {tempo_paralelo:.4f} segundos")

    return resultados_tempo

if __name__ == '__main__':
    # A usar o ficheiro da fase de análise (10 milhões de linhas)
    # A soma tem de dar exatamente 5384!
    arquivo = 'numero2.txt' 
    
    numeros = ler_arquivo(arquivo)
    tempos = executar_teste(numeros)
    
    print("\n" + "="*50)
    print("RESUMO DOS TEMPOS PARA O SEU RELATÓRIO:")
    print("="*50)
    print("Threads/Processos | Tempo (s)")
    for p, t in tempos.items():
        print(f"{p:<17} | {t:.4f}")
    print("="*50)