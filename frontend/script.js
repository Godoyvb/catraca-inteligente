
const API_URL = "http://localhost:8000";

const status = document.getElementById("status");
const statusDot = document.getElementById("status-dot");
const resultado = document.getElementById("resultado");
const listaEventos = document.getElementById("lista-eventos");
const filtroEventos = document.getElementById("filtro-eventos");

const fotoCamera = document.getElementById("fotoCamera");
const cameraPlaceholder = document.getElementById("cameraPlaceholder");
const statusCamera = document.getElementById("statusCamera");
const btnCapturar = document.getElementById("btnCapturar");

let todosEventos = [];

async function verificarSistema() {
    try {
        const resposta = await fetch(`${API_URL}/status`);

        if (!resposta.ok) {
            throw new Error("API indisponível");
        }

        status.textContent = "API conectada";
        status.style.color = "#26e69a";
        statusDot.style.background = "#26e69a";
        statusDot.style.boxShadow = "0 0 12px #26e69a";

    } catch (erro) {
        status.textContent = "API desconectada";
        status.style.color = "#ff5572";
        statusDot.style.background = "#ff5572";
        statusDot.style.boxShadow = "0 0 12px #ff5572";
    }
}

async function verificarArduino() {
    const arduinoDot = document.getElementById("arduino-dot");
    const arduinoLabel = document.getElementById("arduino-label");

    try {
        const resposta = await fetch(`${API_URL}/arduino/status`);

        if (!resposta.ok) {
            throw new Error("Arduino indisponível");
        }

        const dados = await resposta.json();
        const conectado = dados.arduino === "conectado";

        arduinoLabel.textContent = conectado ? "Conectado" : "Desconectado";
        arduinoDot.style.background = conectado ? "#26e69a" : "#ff5572";

        return conectado;

    } catch (erro) {
        arduinoLabel.textContent = "Desconectado";
        arduinoDot.style.background = "#ff5572";
        return false;
    }
}

// Capturar foto pela Raspberry Pi
async function capturarFoto() {
    btnCapturar.disabled = true;
    btnCapturar.textContent = "Capturando...";
    statusCamera.textContent = "Aguarde a captura da câmera...";

    try {
        const resposta = await fetch(`${API_URL}/camera/capturar`, {
            method: "POST"
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            throw new Error(dados.detail || "Erro ao capturar foto");
        }

        fotoCamera.src = `${API_URL}${dados.url}?t=${Date.now()}`;
        fotoCamera.hidden = false;
        cameraPlaceholder.style.display = "none";

        statusCamera.textContent = "Foto capturada: " + dados.arquivo;

    } catch (erro) {
        statusCamera.textContent = "Erro: " + erro.message;
    } finally {
        btnCapturar.disabled = false;
        btnCapturar.textContent = "📸 Tirar foto";
    }
}

function atualizarEstatisticas(eventos) {
    const total = eventos.length;

    const aprovados = eventos.filter(
        evento => Boolean(evento.autorizado)
    ).length;

    document.getElementById("total").textContent = total;
    document.getElementById("aprovados").textContent = aprovados;
    document.getElementById("negados").textContent = total - aprovados;
}

function atualizarHistorico(eventos) {
    listaEventos.innerHTML = "";

    if (eventos.length === 0) {
        listaEventos.innerHTML = `
            <div class="empty">
                <span>◷</span>
                <p>Nenhum evento encontrado.</p>
                <small>Experimente outro filtro.</small>
            </div>
        `;
        return;
    }

    eventos.forEach(evento => {
        const item = document.createElement("div");
        item.className = "event-item";

        const identificador = document.createElement("strong");
        identificador.textContent = evento.identificador_demo;

        const horario = document.createElement("small");
        horario.textContent = new Date(evento.data_hora)
            .toLocaleString("pt-BR");

        const informacoes = document.createElement("div");
        informacoes.append(identificador, horario);

        const situacao = document.createElement("span");
        const autorizado = Boolean(evento.autorizado);

        situacao.className = autorizado
            ? "event-status aprovado"
            : "event-status negado";

        situacao.textContent = autorizado ? "APROVADO" : "NEGADO";

        item.append(informacoes, situacao);
        listaEventos.appendChild(item);
    });
}

function aplicarFiltro() {
    const filtro = filtroEventos.value;

    let eventosFiltrados = todosEventos;

    if (filtro === "aprovados") {
        eventosFiltrados = todosEventos.filter(
            evento => Boolean(evento.autorizado)
        );
    } else if (filtro === "negados") {
        eventosFiltrados = todosEventos.filter(
            evento => !Boolean(evento.autorizado)
        );
    }

    atualizarHistorico(eventosFiltrados);
}

async function carregarEventos() {
    try {
        const resposta = await fetch(`${API_URL}/eventos`);

        if (!resposta.ok) {
            throw new Error("Não foi possível carregar o histórico");
        }

        const dados = await resposta.json();

        todosEventos = dados.eventos;

        atualizarEstatisticas(todosEventos);
        aplicarFiltro();

    } catch (erro) {
        console.error("Erro ao carregar eventos:", erro);
    }
}

function atualizarEstadoCatraca(autorizado) {
    const estado = document.getElementById("estado-catraca");
    const descricao = document.getElementById("descricao-catraca");

    if (!estado || !descricao) return;

    if (autorizado) {
        estado.textContent = "LIBERADO";
        descricao.textContent = "Acesso autorizado na demonstração.";
        estado.className = "gate-approved";
    } else {
        estado.textContent = "NEGADO";
        descricao.textContent = "Acesso negado na demonstração.";
        estado.className = "gate-denied";
    }
}

async function registrarAcesso(autorizado) {
    const identificador = document
        .getElementById("identificador")
        .value.trim();

    if (!identificador) {
        resultado.textContent = "Digite um identificador fictício!";
        resultado.style.color = "#facc15";
        return;
    }

    resultado.textContent = "Processando autorização...";
    resultado.style.color = "#20d9f5";

    try {
        const resposta = await fetch(`${API_URL}/acesso`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                identificador_demo: identificador,
                autorizado: autorizado
            })
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            throw new Error(dados.detail || "Erro ao enviar evento");
        }

        atualizarEstadoCatraca(autorizado);

        if (dados.catraca === "abertura_simulada") {
            resultado.textContent =
                "✓ ACESSO AUTORIZADO — ABERTURA SIMULADA!";
            resultado.style.color = "#26e69a";

        } else if (dados.catraca === "acesso_negado_sem_movimento") {
            resultado.textContent =
                "✕ ACESSO NEGADO — SEM MOVIMENTO!";
            resultado.style.color = "#ff5572";
        }

        await carregarEventos();

        console.log("Resposta da API:", dados);

    } catch (erro) {
        resultado.textContent = "Erro: " + erro.message;
        resultado.style.color = "#ff5572";
    }
}

filtroEventos.addEventListener("change", aplicarFiltro);

verificarSistema();
verificarArduino();
carregarEventos();

setInterval(verificarSistema, 10000);
setInterval(verificarArduino, 10000);
setInterval(carregarEventos, 10000);
