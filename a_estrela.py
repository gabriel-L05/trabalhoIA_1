class No:
    def __init__(self, nome, is_obstaculo=False):
        self.nome = nome
        self.is_obstaculo = is_obstaculo
        self.pai = None
        self.g = 0  # Custo real do início até aqui
        self.h = 0  # Estimativa (heurística) até o destino
        self.f = 0  # Custo total: F = G + H

def reconstruir_caminho(no_atual):
    """Rastreia os nós pais de volta para montar o trajeto do início ao fim."""
    caminho = []
    while no_atual is not None:
        caminho.append(no_atual.nome)
        no_atual = no_atual.pai
    return caminho[::-1]

def busca_a_estrela(inicio, destino, vizinhos_func, heuristica_func):
    lista_aberta = [inicio]   # Nós a explorar
    lista_fechada = []        # Nós já visitados

    while lista_aberta:
        # Pega o nó mais promissor (menor F)
        atual = min(lista_aberta, key=lambda no: no.f)
        lista_aberta.remove(atual)
        lista_fechada.append(atual)

        # Destino encontrado
        if atual == destino:
            return reconstruir_caminho(atual)

        # Avalia cada vizinho adjacente
        for vizinho, custo_mov in vizinhos_func(atual):
            if vizinho.is_obstaculo or vizinho in lista_fechada:
                continue

            novo_g = atual.g + custo_mov

            # Novo nó descoberto
            if vizinho not in lista_aberta:
                vizinho.pai = atual
                vizinho.g = novo_g
                vizinho.h = heuristica_func(vizinho, destino)
                vizinho.f = vizinho.g + vizinho.h
                lista_aberta.append(vizinho)
            
            # Caminho melhor encontrado para nó já conhecido
            elif novo_g < vizinho.g:
                vizinho.pai = atual
                vizinho.g = novo_g
                vizinho.f = vizinho.g + vizinho.h

    return None  # Sem caminho viável

if __name__ == "__main__":
    # Exemplo prático: Navegação em Grid 2D (5x5) com Obstáculos
    linhas, colunas = 5, 5
    grid = {}
    
    # Obstáculos representados como coordenadas (x, y)
    obstaculos = {(1, 1), (1, 2), (2, 2), (3, 2)}
    
    for r in range(linhas):
        for c in range(colunas):
            is_obs = (r, c) in obstaculos
            grid[(r, c)] = No(f"({r},{c})", is_obstaculo=is_obs)

    # Heurística: Distância de Manhattan até o destino
    def heuristica(no_a, no_b):
        coord_a = eval(no_a.nome)
        coord_b = eval(no_b.nome)
        return abs(coord_a[0] - coord_b[0]) + abs(coord_a[1] - coord_b[1])

    # Função de vizinhos (cima, baixo, esquerda, direita)
    def obter_vizinhos(no):
        r, c = eval(no.nome)
        movimentos = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        vizinhos = []
        for mr, mc in movimentos:
            if 0 <= mr < linhas and 0 <= mc < colunas:
                vizinhos.append((grid[(mr, mc)], 1)) # Custo de movimentação unitário = 1
        return vizinhos

    inicio = grid[(0, 0)]
    destino = grid[(4, 4)]

    print("=== Executando Busca A* (A-Star) em Grid 5x5 ===")
    print(f"Início: {inicio.nome} | Destino: {destino.nome}")
    print(f"Obstáculos: {list(obstaculos)}")

    caminho = busca_a_estrela(inicio, destino, obter_vizinhos, heuristica)
    print(f"\nCaminho encontrado ({len(caminho)} passos):")
    print(" -> ".join(caminho))

    print("\n--- Visualização do Grid ---")
    for r in range(linhas):
        linha_str = ""
        for c in range(colunas):
            no_nome = f"({r},{c})"
            if (r, c) == eval(inicio.nome):
                linha_str += " [I] "
            elif (r, c) == eval(destino.nome):
                linha_str += " [D] "
            elif (r, c) in obstaculos:
                linha_str += " [X] "
            elif no_nome in caminho:
                linha_str += "  *  "
            else:
                linha_str += "  .  "
        print(linha_str)
    print("----------------------------\nLegenda: [I] Início, [D] Destino, [X] Obstáculo, * Caminho, . Livre")