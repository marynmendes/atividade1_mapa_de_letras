import mapa

inicio = (input("Escolha o ponto de início: ")).upper()
fim = (input("Escolha o ponto de fim: ")).upper()
caminho_u, caminho_d = mapa.buscar_caminho(inicio, fim)
mapa.imprimir_caminho(caminho_u, caminho_d)