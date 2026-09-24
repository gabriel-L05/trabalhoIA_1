import random

def criar_individuo(n):
    # Índice = Coluna, Valor = Linha da Rainha
    return [random.randint(0, n - 1) for _ in range(n)]

def fitness(individuo):
    # Calcula pares de rainhas sem conflito (nota máx para N=8 é 28)
    n = len(individuo)
    conflitos = 0
    for i in range(n):
        for j in range(i + 1, n):
            if individuo[i] == individuo[j] or abs(individuo[i] - individuo[j]) == abs(i - j):
                conflitos += 1
    
    max_pares = (n * (n - 1)) // 2
    return max_pares - conflitos

def selecao_torneio(populacao, k=3):
    # Seleciona o melhor entre K competidores aleatórios
    competidores = random.sample(populacao, k)
    return max(competidores, key=fitness)

def crossover(pai1, pai2):
    # Cruzamento de 1 ponto de corte
    ponto = random.randint(1, len(pai1) - 1)
    filho1 = pai1[:ponto] + pai2[ponto:]
    filho2 = pai2[:ponto] + pai1[ponto:]
    return filho1, filho2

def mutacao(individuo, taxa_mutacao=0.1):
    # Altera aleatoriamente a linha de uma rainha com base na taxa
    return [random.randint(0, len(individuo) - 1) if random.random() < taxa_mutacao else gene for gene in individuo]

def algoritmo_genetico(n=8, tam_populacao=100, max_geracoes=1000, taxa_mutacao=0.1):
    max_fitness = (n * (n - 1)) // 2
    populacao = [criar_individuo(n) for _ in range(tam_populacao)]
    
    print(f"=== Iniciando Algoritmo Genético para {n}-Rainhas ===")
    print(f"Aptidão máxima (objetivo): {max_fitness} pares seguros\n")
    
    for geracao in range(1, max_geracoes + 1):
        melhor_ind = max(populacao, key=fitness)
        melhor_fit = fitness(melhor_ind)
        
        if geracao % 50 == 0 or melhor_fit == max_fitness:
            print(f"Geração {geracao:4d} | Melhor Fitness: {melhor_fit}/{max_fitness} | Indivíduo: {melhor_ind}")
        
        # Critério de parada: solução ótima encontrada
        if melhor_fit == max_fitness:
            print(f"\n Solução perfeita encontrada na geração {geracao}!")
            return melhor_ind
        
        # Elitismo: mantém o melhor indivíduo na próxima geração
        nova_populacao = [melhor_ind]
        
        # Gera novos indivíduos através de seleção, cruzamento e mutação
        while len(nova_populacao) < tam_populacao:
            pai1 = selecao_torneio(populacao)
            pai2 = selecao_torneio(populacao)
            filho1, filho2 = crossover(pai1, pai2)
            
            nova_populacao.append(mutacao(filho1, taxa_mutacao))
            if len(nova_populacao) < tam_populacao:
                nova_populacao.append(mutacao(filho2, taxa_mutacao))
                
        populacao = nova_populacao
        
    print("\n⚠️ Número máximo de gerações atingido.")
    return max(populacao, key=fitness)

def imprimir_tabuleiro(solucao):
    n = len(solucao)
    print("\n--- Tabuleiro ---")
    for lin in range(n):
        linha_str = ""
        for col in range(n):
            if solucao[col] == lin:
                linha_str += " Q "
            else:
                linha_str += " . "
        print(linha_str)
    print("-----------------\n")

if __name__ == "__main__":
    random.seed(42)  # Para reprodutibilidade
    solucao = algoritmo_genetico(n=8, tam_populacao=100, max_geracoes=500, taxa_mutacao=0.15)
    print(f"Resultado final: {solucao}")
    imprimir_tabuleiro(solucao)
