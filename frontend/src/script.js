// Front-end "burro": não tem nenhuma lógica de busca de caminho aqui.
// Os pontos do mapa e o algoritmo de busca vêm todos da API Flask
// (/api/pontos e /api/buscar-caminho), que por sua vez chama as funções
// originais do mapa.py.

const CELL = 78,
  PAD = 40;

let pontos = {}; // preenchido a partir de /api/pontos
let LETRAS = [];

function coord(letra) {
  const [row, col] = pontos[letra].ponto;
  return { x: PAD + col * CELL, y: PAD + row * CELL };
}

function desenharMapa(resultado) {
  const svg = document.getElementById("svgMapa");
  svg.innerHTML = "";

  // marcadores de seta (recriados a cada desenho, já que o innerHTML é limpo acima)
  const defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
  defs.innerHTML = `
    <marker id="arrow-edge" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" class="arrowhead-edge"></path>
    </marker>
    <marker id="arrow-path" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" class="arrowhead-path"></path>
    </marker>
    <marker id="arrow-discard" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" class="arrowhead-discard"></path>
    </marker>
  `;
  svg.appendChild(defs);

  const NODE_R = 13,
    GAP = 4; // espaço entre a ponta da seta e o círculo do destino

  const ordemUsado = resultado
    ? resultado.caminho.map((item) => item.ponto)
    : [];
  const usados = new Set(ordemUsado);
  const pathSet = new Set();
  for (let i = 0; i < ordemUsado.length - 1; i++) {
    pathSet.add(ordemUsado[i] + ">" + ordemUsado[i + 1]);
  }

  // pontos que o algoritmo chegou a olhar, mas descartou durante a busca
  const discardSet = new Set();
  if (resultado) {
    for (const item of resultado.descartes) {
      for (const d of item.descartados) {
        discardSet.add(item.ponto + ">" + d);
      }
    }
  }

  // arestas (o grafo é direcionado: a seta mostra de onde pra onde dá pra ir)
  for (const letra of LETRAS) {
    const c1 = coord(letra);
    for (const v of pontos[letra].vizinhos) {
      if (!pontos[v]) continue;
      const c2 = coord(v);
      const isPath = pathSet.has(letra + ">" + v);
      const isDiscard = !isPath && discardSet.has(letra + ">" + v);

      // encurta o fim da linha pra a seta não ficar escondida atrás do círculo do destino
      const dx = c2.x - c1.x,
        dy = c2.y - c1.y;
      const dist = Math.hypot(dx, dy) || 1;
      const endX = c2.x - (dx / dist) * (NODE_R + GAP);
      const endY = c2.y - (dy / dist) * (NODE_R + GAP);

      let cls = "edge";
      let marker = "url(#arrow-edge)";
      if (isPath) {
        cls += " path";
        marker = "url(#arrow-path)";
      } else if (isDiscard) {
        cls += " discard";
        marker = "url(#arrow-discard)";
      }

      const line = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "line",
      );
      line.setAttribute("x1", c1.x);
      line.setAttribute("y1", c1.y);
      line.setAttribute("x2", endX);
      line.setAttribute("y2", endY);
      line.setAttribute("class", cls);
      line.setAttribute("marker-end", marker);
      svg.appendChild(line);
    }
  }

  // pontos
  for (const letra of LETRAS) {
    const c = coord(letra);
    const isUsed = usados.has(letra);
    const isStart = ordemUsado[0] === letra;
    const isEnd =
      ordemUsado.length && ordemUsado[ordemUsado.length - 1] === letra;

    const circle = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "circle",
    );
    circle.setAttribute("cx", c.x);
    circle.setAttribute("cy", c.y);
    circle.setAttribute("r", 13);
    let cls = "pt-circle" + (isUsed ? " used" : "");
    if (isStart) cls += " start";
    if (isEnd) cls += " end";
    circle.setAttribute("class", cls);
    svg.appendChild(circle);

    const label = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "text",
    );
    label.setAttribute("x", c.x);
    label.setAttribute("y", c.y + 4);
    label.setAttribute("text-anchor", "middle");
    label.setAttribute("class", "pt-label" + (isUsed ? " used-label" : ""));
    label.textContent = letra;
    svg.appendChild(label);
  }
}

const selInicio = document.getElementById("inicio");
const selFim = document.getElementById("fim");
const selDist = document.getElementById("tipoDist");
const btn = document.getElementById("btnBuscar");
const errMsg = document.getElementById("errMsg");
const statusLine = document.getElementById("statusLine");
const resultCard = document.getElementById("resultCard");
const discardCard = document.getElementById("discardCard");

async function carregarPontos() {
  try {
    const resp = await fetch("/api/pontos");
    if (!resp.ok) throw new Error("Falha ao carregar o mapa");
    pontos = await resp.json();
    LETRAS = Object.keys(pontos);

    for (const letra of LETRAS) {
      const o1 = document.createElement("option");
      o1.value = letra;
      o1.textContent = letra;
      selInicio.appendChild(o1);
      const o2 = document.createElement("option");
      o2.value = letra;
      o2.textContent = letra;
      selFim.appendChild(o2);
    }
    selInicio.value = LETRAS[0];
    selFim.value = LETRAS[LETRAS.length - 1];

    desenharMapa(null);
    statusLine.textContent =
      'Selecione início, fim e o tipo de distância, depois clique em "Buscar caminho".';
  } catch (e) {
    statusLine.textContent =
      "Não foi possível carregar o mapa. Verifique se o backend (app.py) está rodando.";
  }
}

btn.addEventListener("click", async () => {
  errMsg.hidden = true;
  const inicio = selInicio.value,
    fim = selFim.value,
    opcao = Number(selDist.value);

  if (inicio === fim) {
    errMsg.textContent =
      "O ponto de início não pode ser igual ao ponto de fim.";
    errMsg.hidden = false;
    return;
  }

  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span>Buscando...';
  resultCard.hidden = true;
  discardCard.hidden = true;

  try {
    const resp = await fetch("/api/buscar-caminho", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ inicio, fim, opcao }),
    });
    const dados = await resp.json();

    if (!resp.ok) {
      errMsg.textContent = dados.erro || "Não foi possível buscar o caminho.";
      errMsg.hidden = false;
      desenharMapa(null);
      return;
    }

    desenharMapa(dados);

    const nomesDist = { 1: "Euclidiana", 2: "Manhattan", 3: "Chebyshev" };
    statusLine.textContent = `Caminho de ${inicio} até ${fim} usando distância ${nomesDist[opcao]}.`;

    const tbody = document.querySelector("#tabelaCaminho tbody");
    tbody.innerHTML = "";
    dados.caminho.forEach((item, i) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td>${i + 1}</td><td>${item.ponto}</td><td>${Number(item.distancia).toFixed(2)}</td>`;
      tbody.appendChild(tr);
    });
    resultCard.hidden = false;

    const discardList = document.getElementById("discardList");
    discardList.innerHTML = "";
    let algumDescarte = false;
    for (const item of dados.descartes) {
      if (item.descartados && item.descartados.length) {
        algumDescarte = true;
        const div = document.createElement("div");
        div.className = "discard-item";
        div.innerHTML = `<span class="pt">${item.ponto}</span> descartou: ${item.descartados.join(", ")}`;
        discardList.appendChild(div);
      }
    }
    if (!algumDescarte) {
      discardList.innerHTML =
        '<div class="empty-state">Nenhum ponto foi descartado nessa busca.</div>';
    }
    discardCard.hidden = false;
  } catch (e) {
    errMsg.textContent = "Erro de conexão com o backend.";
    errMsg.hidden = false;
  } finally {
    btn.disabled = false;
    btn.textContent = "Buscar caminho";
  }
});

carregarPontos();
