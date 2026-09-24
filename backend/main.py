import mapa

inicio = (input("Escolha o ponto de início: ")).upper()
fim = (input("Escolha o ponto de fim: ")).upper()
opcao = mapa.escolher_distancia()
caminho_u, caminho_d = mapa.buscar_caminho(inicio, fim, opcao)
mapa.imprimir_caminho(caminho_u, caminho_d)
