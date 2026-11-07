
const API_URL = "http://localhost:8000";

// Estatísticas da sessão
let total = 0;
let aprovados = 0;
let negados = 0;

// Histórico de eventos
const eventos = [];

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
function atualizarEstatisticas() {
    document.getElementById("total").textContent = total;
    document.getElementById("aprovados").textContent = aprovados;
    document.getElementById("negados").textContent = negados;
}

// Mostrar histórico
function atualizarHistorico() {
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

    eventos.slice().reverse().forEach(evento => {
        const item = document.createElement("div");
        item.className = "event-item";

        const identificador = document.createElement("strong");
        identificador.textContent = evento.identificador;

        const horario = document.createElement("small");
        horario.textContent = evento.horario;

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

        total++;

        if (autorizado) {
            aprovados++;
            resultado.textContent = "✓ SIMULAÇÃO APROVADA!";
            resultado.style.color = "#26e69a";
        } else {
            negados++;
            resultado.textContent = "✕ SIMULAÇÃO NEGADA!";
            resultado.style.color = "#ff5572";
        }

        const horario = new Date().toLocaleTimeString("pt-BR");

        eventos.push({
            identificador: identificador,
            autorizado: autorizado,
            horario: horario
        });

        atualizarEstatisticas();
        atualizarHistorico();

        console.log("Evento enviado:", dados);

    } catch (erro) {
        resultado.textContent = "Erro: " + erro.message;
        resultado.style.color = "#ff5572";
    }
}

// Verificar conexão ao abrir a página
verificarSistema();

// Atualizar conexão periodicamente
setInterval(verificarSistema, 10000);
