import math

#representação do mapa como uma matriz
mapa = [
    ['A', 'B', 0, 0, 'C', 'D', 0, 'E'],
    [0, 0, 0, 0, 0, 0, 0, 0],
    ['F', 'G', 0, 0, 'H', 0, 0, 'I'],
    [0, 'J', 0, 'K', 'L', 'M', 0, 'N'],
    [0, 0, 0, 0, 'O', 0, 0, 'P'],
    ['Q','R', 0, 'S', 'T', 0, 0, 'U']
]

#dicionário com os pontos do mapa e seus vizinhos, sendo os vizinhos o pontos 
#"enxergados" a partir do ponto atual e que podem ser alcançados partindo deste.
#ex: existe um caminho do ponto H para o ponto C, por isso H está na lista de vizinhos de C,
#mas não existe um caminho do ponto C para o ponto H, então C não está na lista de vizinhos de H.
pontos = {
    'A': {'ponto': (0, 0), 'vizinhos': [mapa[0][1], mapa[2][0]]},
    'B': {'ponto': (0, 1), 'vizinhos': [mapa[0][0], mapa[0][4], mapa[2][1]]},
    'C': {'ponto': (0, 4), 'vizinhos': [mapa[0][1], mapa[0][5]]},
    'D': {'ponto': (0, 5), 'vizinhos': [mapa[0][4], mapa[0][7], mapa[3][5]]},
    'E': {'ponto': (0, 7), 'vizinhos': [mapa[0][5], mapa[2][7]]},
    'F': {'ponto': (2, 0), 'vizinhos': [mapa[0][0], mapa[2][1], mapa[5][0]]},
    'G': {'ponto': (2, 1), 'vizinhos': [mapa[2][0], mapa[2][4], mapa[3][1]]},
    'H': {'ponto': (2, 4), 'vizinhos': [mapa[0][4], mapa[2][1]]},
    'I': {'ponto': (2, 7), 'vizinhos': [mapa[3][7]]},
    'J': {'ponto': (3, 1), 'vizinhos': [mapa[5][1]]},
    'K': {'ponto': (3, 3), 'vizinhos': [mapa[3][1], mapa[5][3]]},
    'L': {'ponto': (3, 4), 'vizinhos': [mapa[2][4], mapa[3][3]]},
    'M': {'ponto': (3, 5), 'vizinhos': [mapa[0][5], mapa[3][4]]},
    'N': {'ponto': (3, 7), 'vizinhos': [mapa[3][5], mapa[4][7]]},
    'O': {'ponto': (4, 4), 'vizinhos': [mapa[3][4]]},
    'P': {'ponto': (4, 7), 'vizinhos': [mapa[4][4], mapa[5][7]]},
    'Q': {'ponto': (5, 0), 'vizinhos': [mapa[2][0], mapa[5][1]]},
    'R': {'ponto': (5, 1), 'vizinhos': [mapa[5][3]]},
    'S': {'ponto': (5, 3), 'vizinhos': [mapa[3][3], mapa[5][4]]},
    'T': {'ponto': (5, 4), 'vizinhos': [mapa[4][4], mapa[5][7]]},
    'U': {'ponto': (5, 7), 'vizinhos': [mapa[5][4]]}
}

#função que retorna os vizinhos de um ponto
def get_vizinhos(ponto):
    if ponto in pontos:
        return pontos[ponto]['vizinhos']
    else:
        return []

#função que calcula a distância entre dois pontos usando a distância euclidiana.
def distancia_euclidiana(ponto1, ponto2):
    x1, y1 = pontos[ponto1]['ponto']
    x2, y2 = pontos[ponto2]['ponto']
    return math.sqrt(((x2 - x1) ** 2 + (y2 - y1) ** 2))

#função que calcula a distância entre dois pontos usando a distância de manhattan.
def distancia_manhattan(ponto1, ponto2):
    x1, y1 = pontos[ponto1]['ponto']
    x2, y2 = pontos[ponto2]['ponto']
    return abs(x2 - x1) + abs(y2 - y1)

#função que calcula a distância entre dois pontos usando a distância de chebyshev.
def distancia_chebyshev(ponto1, ponto2):
    x1, y1 = pontos[ponto1]['ponto']
    x2, y2 = pontos[ponto2]['ponto']
    return max(abs(x2 - x1), abs(y2 - y1))

def escolher_distancia():
    print("Escolha o tipo de distância a ser utilizada:")
    print("1 - Distância Euclidiana")
    print("2 - Distância de Manhattan")
    print("3 - Distância de Chebyshev")
    opcao = int(input("Opção: "))
    return opcao

def distancia(ponto1, ponto2, opcao):
    if opcao == 1:
        return distancia_euclidiana(ponto1, ponto2)
    elif opcao == 2:
        return distancia_manhattan(ponto1, ponto2)
    elif opcao == 3:
        return distancia_chebyshev(ponto1, ponto2)

#função para encontrar o caminho entre dois pontos
def buscar_caminho(ponto_inicial, ponto_final):
    caminho_usado = {}    
    caminho_descartado = {}
    distancia_final =  0.0
    ponto_atual = ponto_inicial
    opcao = escolher_distancia()
    descartados_atual = {}

    if ponto_inicial == ponto_final:
        return None

    while ponto_atual != ponto_final:
        caminho_usado[ponto_atual] = distancia_final
        caminho_descartado[ponto_atual] = []
        descartados_atual[ponto_atual] = []
        vizinhos = get_vizinhos(ponto_atual)
        valor_distancia = 0.0
        novo_ponto = None

        #escolhe o vizinho que tem a menor distância até o ponto final, sendo que esse vizinho não pode 
        #estar no caminho já percorrido e nem já ter sido descartado pelo ponto atual, e se for o ponto final, ele é escolhido imediatamente
        for vizinho in vizinhos:
            if vizinho == ponto_final:
                novo_ponto = vizinho
                break
            if vizinho in caminho_usado or vizinho in descartados_atual:
                continue
            dist_vizfin = distancia(vizinho, ponto_final, opcao)
            dist_vizatual = distancia(ponto_atual, vizinho, opcao)
            dist_momento = dist_vizfin + dist_vizatual
            if dist_momento < valor_distancia or valor_distancia == 0.0:
                valor_distancia = dist_momento
                novo_ponto = vizinho

        #caso não haja vizinhos disponíveis para o ponto atual, ele é removido do caminho
        #e um novo caminho a partir do ponto anterior ao atual é calculado
        if novo_ponto is None:
            del caminho_usado[ponto_atual]
            ponto_anterior = list(caminho_usado.keys())[-1]
            descartados_atual[ponto_atual].append(ponto_atual)
            distancia_final -= distancia(ponto_anterior, ponto_atual, opcao)
            ponto_atual = ponto_anterior
            continue

        #adiciona os vizinhos descartados ao dicionário de caminhos descartados
        for vizinho in vizinhos:
            if vizinho != novo_ponto and vizinho != ponto_final and vizinho not in caminho_usado:
                caminho_descartado[ponto_atual].append(vizinho)

        #registra a distancia real percorrida do ponto atual até o novo ponto e atualiza a distancia total percorrida
        distancia_final += distancia(ponto_atual, novo_ponto, opcao)
        #atualiza o ponto atual para o novo ponto escolhido
        ponto_atual = novo_ponto

    #finaliza o caminho escolhido com o ponto final e registra a distancia total percorrida
    caminho_usado[ponto_final] = distancia_final
    #retorna os dicinários de caminhos usados e descartados
    return caminho_usado, caminho_descartado

def imprimir_caminho(caminho_usado, caminho_descartado):
    pontos_usados_formatados = [f"{ponto}({distancia:.0f})" for ponto, distancia in caminho_usado.items()]
    print("Caminho usado:")
    print(" -> ".join(pontos_usados_formatados))
    print()
    for ponto, vizinhos in caminho_descartado.items():
        if vizinhos:
            print(f"{ponto} descartou: {', '.join(vizinhos)}")
    