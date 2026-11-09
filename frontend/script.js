
const API_URL = "http://localhost:8000";

// Estatísticas
let total = 0;
let aprovados = 0;
let negados = 0;

// Elementos da página
const status = document.getElementById("status");
const statusDot = document.getElementById("status-dot");
const resultado = document.getElementById("resultado");
const listaEventos = document.getElementById("lista-eventos");

// Verificar conexão com a API
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

// Atualizar estatísticas
function atualizarEstatisticas(eventos) {
    total = eventos.length;
    aprovados = eventos.filter(evento => evento.autorizado).length;
    negados = total - aprovados;

    document.getElementById("total").textContent = total;
    document.getElementById("aprovados").textContent = aprovados;
    document.getElementById("negados").textContent = negados;
}

// Mostrar histórico
function atualizarHistorico(eventos) {
    listaEventos.innerHTML = "";

    if (eventos.length === 0) {
        listaEventos.innerHTML = `
            <div class="empty">
                <span>◷</span>
                <p>Nenhum evento registrado.</p>
                <small>Os testes aparecerão aqui.</small>
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
        situacao.className = evento.autorizado
            ? "event-status aprovado"
            : "event-status negado";

        situacao.textContent = evento.autorizado
            ? "APROVADO"
            : "NEGADO";

        item.append(informacoes, situacao);
        listaEventos.appendChild(item);
    });
}

// Buscar histórico no SQLite através da API
async function carregarEventos() {
    try {
        const resposta = await fetch(`${API_URL}/eventos`);

        if (!resposta.ok) {
            throw new Error("Não foi possível carregar o histórico");
        }

        const dados = await resposta.json();

        atualizarEstatisticas(dados.eventos);
        atualizarHistorico(dados.eventos);

    } catch (erro) {
        console.error("Erro ao carregar eventos:", erro);
    }
}

// Registrar evento de demonstração
async function registrarAcesso(autorizado) {
    const identificador = document
        .getElementById("identificador")
        .value.trim();

    if (!identificador) {
        resultado.textContent = "Digite um identificador fictício!";
        resultado.style.color = "#facc15";
        return;
    }

    resultado.textContent = "Enviando evento...";
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

        resultado.textContent = autorizado
            ? "✓ SIMULAÇÃO APROVADA!"
            : "✕ SIMULAÇÃO NEGADA!";

        resultado.style.color = autorizado
            ? "#26e69a"
            : "#ff5572";

        await carregarEventos();

        console.log("Evento enviado:", dados);

    } catch (erro) {
        resultado.textContent = "Erro: " + erro.message;
        resultado.style.color = "#ff5572";
    }
}

// Inicialização
verificarSistema();
carregarEventos();

// Atualizar informações periodicamente
setInterval(verificarSistema, 10000);
setInterval(carregarEventos, 10000);
