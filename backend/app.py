from flask import Flask, jsonify, request, send_from_directory
import os
import mapa

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
# o Flask, por padrão, reordena as chaves de um dict em ordem alfabética
# ao gerar o JSON - isso quebrava a ordem do caminho encontrado (que não é
# alfabética, é a ordem em que o algoritmo passou pelos pontos). Além de
# desligar isso aqui, o endpoint de busca manda o caminho como lista.
app.json.sort_keys = False


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# devolve os pontos do mapa (coordenadas + vizinhos) pra o front desenhar o grafo,
# assim os dados ficam só num lugar (mapa.py) em vez de duplicados no JS
@app.route("/api/pontos")
def api_pontos():
    dados = {
        letra: {"ponto": info["ponto"], "vizinhos": info["vizinhos"]}
        for letra, info in mapa.pontos.items()
    }
    return jsonify(dados)


@app.route("/api/buscar-caminho", methods=["POST"])
def api_buscar_caminho():
    body = request.get_json(silent=True) or {}
    inicio = str(body.get("inicio", "")).upper()
    fim = str(body.get("fim", "")).upper()
    opcao = body.get("opcao")

    if inicio not in mapa.pontos or fim not in mapa.pontos:
        return jsonify({"erro": "Ponto de início ou fim inválido."}), 400

    if opcao not in (1, 2, 3):
        return jsonify({"erro": "Tipo de distância inválido."}), 400

    if inicio == fim:
        return jsonify({"erro": "O ponto de início não pode ser igual ao ponto de fim."}), 400

    resultado = mapa.buscar_caminho(inicio, fim, opcao)

    if resultado is None:
        return jsonify({"erro": "Não foi possível encontrar um caminho entre esses pontos."}), 404

    caminho_usado, caminho_descartado = resultado

    # manda o caminho como LISTA (não como dict): dict em JSON não garante
    # ordem entre implementações/proxies, e a ordem aqui importa - é a
    # sequência real de pontos percorridos pelo algoritmo.
    caminho = [
        {"ponto": ponto, "distancia": dist}
        for ponto, dist in caminho_usado.items()
    ]
    descartes = [
        {"ponto": ponto, "descartados": vizinhos}
        for ponto, vizinhos in caminho_descartado.items()
    ]

    return jsonify({
        "caminho": caminho,
        "descartes": descartes,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
