// ==============================================================================
// JAVASCRIPT PRINCIPAL PARA O SIMULADOR ORBITAL
// ==============================================================================

// Constantes globais
const CONSTANTES = {
    G: 6.67430e-11,
    UA: 1.496e11,
    R_TERRA: 6.371e6,
    M_SOL: 1.989e30,
    M_TERRA: 5.972e24
};

// Tornar constantes globalmente disponíveis
const R_TERRA = CONSTANTES.R_TERRA;
const G = CONSTANTES.G;
const UA = CONSTANTES.UA;
const M_SOL = CONSTANTES.M_SOL;
const M_TERRA = CONSTANTES.M_TERRA;

// Estado global da aplicação
const AppState = {
    simulacoes: [],
    simulacaoAtiva: null,
    configuracao: null
};

// ==============================================================================
// FUNÇÕES UTILITÁRIAS
// ==============================================================================

/**
 * Formata números em notação científica
 */
function formatarNotacaoCientifica(numero, casasDecimais = 2) {
    if (numero === 0) return '0';
    if (Math.abs(numero) < 1e-6) return numero.toExponential(casasDecimais);
    if (Math.abs(numero) > 1e6) return numero.toExponential(casasDecimais);
    return numero.toFixed(casasDecimais);
}

/**
 * Formata distâncias em unidades apropriadas
 */
function formatarDistancia(metros) {
    if (metros < 1000) {
        return `${metros.toFixed(0)} m`;
    } else if (metros < 1000000) {
        return `${(metros / 1000).toFixed(2)} km`;
    } else if (metros < CONSTANTES.UA) {
        return `${(metros / 1000000).toFixed(2)} × 10⁶ m`;
    } else {
        return `${(metros / CONSTANTES.UA).toFixed(3)} UA`;
    }
}

/**
 * Formata velocidades em km/s
 */
function formatarVelocidade(metrosPorSegundo) {
    return `${(metrosPorSegundo / 1000).toFixed(2)} km/s`;
}

/**
 * Formata massas em unidades apropriadas
 */
function formatarMassa(kg) {
    if (kg < 1e6) {
        return `${(kg / 1000).toFixed(0)} kg`;
    } else if (kg < 1e9) {
        return `${(kg / 1e6).toFixed(1)} × 10⁶ kg`;
    } else if (kg < 1e12) {
        return `${(kg / 1e9).toFixed(1)} × 10⁹ kg`;
    } else {
        return `${(kg / 1e12).toFixed(1)} × 10¹² kg`;
    }
}

/**
 * Formata energia em unidades apropriadas
 */
function formatarEnergia(joules) {
    if (joules < 1e12) {
        return `${(joules / 1e9).toFixed(2)} × 10⁹ J`;
    } else if (joules < 1e15) {
        return `${(joules / 1e12).toFixed(2)} × 10¹² J`;
    } else {
        return `${(joules / 1e15).toFixed(2)} × 10¹⁵ J`;
    }
}

/**
 * Mostra um alerta na tela
 */
function mostrarAlerta(mensagem, tipo = 'info', duracao = 5000) {
    const alertContainer = document.getElementById('alert-container');
    if (!alertContainer) return;
    
    const alertId = 'alert-' + Date.now();
    const alertHtml = `
        <div id="${alertId}" class="alert alert-${tipo} alert-dismissible fade show" role="alert">
            <i class="fas fa-${getIconeAlerta(tipo)} me-2"></i>
            ${mensagem}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    alertContainer.insertAdjacentHTML('beforeend', alertHtml);
    
    // Remover automaticamente após a duração especificada
    if (duracao > 0) {
        setTimeout(() => {
            const alert = document.getElementById(alertId);
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, duracao);
    }
}

/**
 * Retorna o ícone apropriado para o tipo de alerta
 */
function getIconeAlerta(tipo) {
    const icones = {
        'success': 'check-circle',
        'danger': 'exclamation-triangle',
        'warning': 'exclamation-circle',
        'info': 'info-circle'
    };
    return icones[tipo] || 'info-circle';
}

/**
 * Valida dados de entrada do formulário
 */
function validarDadosFormulario(dados) {
    const erros = [];
    
    if (!dados.cenario) {
        erros.push('Selecione um cenário de simulação');
    }
    
    if (!dados.tempo_total || dados.tempo_total <= 0) {
        erros.push('Tempo de simulação deve ser maior que zero');
    }
    
    if (dados.tempo_total > 100) {
        erros.push('Tempo de simulação muito longo (máximo 100 anos)');
    }
    
    if (dados.massa_asteroide && (dados.massa_asteroide <= 0 || dados.massa_asteroide > 1e20)) {
        erros.push('Massa do asteroide inválida');
    }
    
    if (dados.distancia_inicial && (dados.distancia_inicial <= 0 || dados.distancia_inicial > 1000)) {
        erros.push('Distância inicial inválida');
    }
    
    if (dados.velocidade_aproximacao && (dados.velocidade_aproximacao <= 0 || dados.velocidade_aproximacao > 100000)) {
        erros.push('Velocidade de aproximação inválida');
    }
    
    return erros;
}

/**
 * Atualiza o status da conexão
 */
function atualizarStatusConexao(status) {
    const statusElement = document.getElementById('status-conexao');
    if (statusElement) {
        statusElement.textContent = status;
        statusElement.className = status === 'Conectado' ? 'text-success' : 'text-danger';
    }
}

// ==============================================================================
// FUNÇÕES DE SIMULAÇÃO
// ==============================================================================

/**
 * Executa uma simulação
 */
async function executarSimulacao(dados) {
    try {
        // Validar dados
        const erros = validarDadosFormulario(dados);
        if (erros.length > 0) {
            mostrarAlerta(erros.join('<br>'), 'danger');
            return null;
        }
        
        // Mostrar loading
        mostrarModalLoading('Executando simulação...');
        
        // Fazer requisição
        const response = await fetch('/api/simular', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dados)
        });
        
        const resultado = await response.json();
        
        // Ocultar loading
        ocultarModalLoading();
        
        if (resultado.status === 'sucesso') {
            mostrarAlerta('Simulação executada com sucesso!', 'success');
            return resultado;
        } else {
            mostrarAlerta(`Erro na simulação: ${resultado.mensagem}`, 'danger');
            return null;
        }
        
    } catch (error) {
        ocultarModalLoading();
        mostrarAlerta(`Erro de comunicação: ${error.message}`, 'danger');
        return null;
    }
}

/**
 * Carrega lista de simulações
 */
async function carregarSimulacoes() {
    try {
        const response = await fetch('/api/lista_simulacoes');
        const data = await response.json();
        AppState.simulacoes = data.simulacoes;
        return data.simulacoes;
    } catch (error) {
        console.error('Erro ao carregar simulações:', error);
        mostrarAlerta('Erro ao carregar lista de simulações', 'danger');
        return [];
    }
}

/**
 * Carrega detalhes de uma simulação específica
 */
async function carregarDetalhesSimulacao(simId) {
    try {
        const response = await fetch(`/api/resultados/${simId}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erro ao carregar detalhes:', error);
        mostrarAlerta('Erro ao carregar detalhes da simulação', 'danger');
        return null;
    }
}

/**
 * Carrega gráfico de uma simulação
 */
async function carregarGrafico(simId) {
    try {
        const response = await fetch(`/api/grafico/${simId}`);
        const data = await response.json();
        return data.grafico;
    } catch (error) {
        console.error('Erro ao carregar gráfico:', error);
        return null;
    }
}

// ==============================================================================
// FUNÇÕES DE INTERFACE
// ==============================================================================

/**
 * Mostra modal de loading
 */
function mostrarModalLoading(mensagem = 'Processando...') {
    const modal = document.getElementById('loadingModal');
    if (modal) {
        const modalInstance = new bootstrap.Modal(modal);
        modalInstance.show();
        
        // Atualizar mensagem se especificada
        const mensagemElement = modal.querySelector('.modal-body p');
        if (mensagemElement) {
            mensagemElement.textContent = mensagem;
        }
    }
}

/**
 * Oculta modal de loading
 */
function ocultarModalLoading() {
    const modal = document.getElementById('loadingModal');
    if (modal) {
        const modalInstance = bootstrap.Modal.getInstance(modal);
        if (modalInstance) {
            modalInstance.hide();
        }
    }
}

/**
 * Atualiza barra de progresso
 */
function atualizarProgresso(percentual, texto = '') {
    const progressBar = document.getElementById('progress-bar');
    const statusText = document.getElementById('status-text');
    
    if (progressBar) {
        progressBar.style.width = `${percentual}%`;
        progressBar.setAttribute('aria-valuenow', percentual);
    }
    
    if (statusText && texto) {
        statusText.textContent = texto;
    }
}

/**
 * Cria gráfico de linha usando Chart.js
 */
function criarGraficoLinha(canvasId, dados, opcoes = {}) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    
    const config = {
        type: 'line',
        data: dados,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: opcoes.titulo || 'Gráfico'
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: opcoes.eixoX || 'Tempo'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: opcoes.eixoY || 'Valor'
                    }
                }
            },
            ...opcoes
        }
    };
    
    return new Chart(ctx, config);
}

/**
 * Cria gráfico de barras usando Chart.js
 */
function criarGraficoBarras(canvasId, dados, opcoes = {}) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    
    const config = {
        type: 'bar',
        data: dados,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: opcoes.titulo || 'Gráfico de Barras'
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: opcoes.eixoX || 'Categoria'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: opcoes.eixoY || 'Valor'
                    }
                }
            },
            ...opcoes
        }
    };
    
    return new Chart(ctx, config);
}

// ==============================================================================
// FUNÇÕES DE CONFIGURAÇÃO
// ==============================================================================

/**
 * Carrega configurações do servidor
 */
async function carregarConfiguracoes() {
    try {
        const response = await fetch('/api/configuracoes');
        const data = await response.json();
        AppState.configuracao = data;
        return data;
    } catch (error) {
        console.error('Erro ao carregar configurações:', error);
        return null;
    }
}

/**
 * Aplica configurações aos elementos da interface
 */
function aplicarConfiguracoes(config) {
    if (!config) return;
    
    // Aplicar configurações de cenários
    if (config.cenarios) {
        const cenarioSelect = document.getElementById('cenario');
        if (cenarioSelect) {
            // Limpar opções existentes
            cenarioSelect.innerHTML = '<option value="">Selecione um cenário...</option>';
            
            // Adicionar opções dos cenários
            Object.entries(config.cenarios).forEach(([key, cenario]) => {
                const option = document.createElement('option');
                option.value = key;
                option.textContent = cenario.nome;
                cenarioSelect.appendChild(option);
            });
        }
    }
}

// ==============================================================================
// FUNÇÕES DE INICIALIZAÇÃO
// ==============================================================================

/**
 * Inicializa a aplicação
 */
async function inicializarApp() {
    try {
        // Atualizar status de conexão
        atualizarStatusConexao('Conectado');
        
        // Carregar configurações
        const config = await carregarConfiguracoes();
        if (config) {
            aplicarConfiguracoes(config);
        }
        
        // Configurar event listeners globais
        configurarEventListeners();
        
        console.log('Aplicação inicializada com sucesso');
        
    } catch (error) {
        console.error('Erro ao inicializar aplicação:', error);
        atualizarStatusConexao('Erro');
        mostrarAlerta('Erro ao inicializar aplicação', 'danger');
    }
}

/**
 * Configura event listeners globais
 */
function configurarEventListeners() {
    // Listener para mudanças de conectividade
    window.addEventListener('online', () => {
        atualizarStatusConexao('Conectado');
        mostrarAlerta('Conexão restaurada', 'success');
    });
    
    window.addEventListener('offline', () => {
        atualizarStatusConexao('Desconectado');
        mostrarAlerta('Conexão perdida', 'warning');
    });
    
    // Listener para erros globais
    window.addEventListener('error', (event) => {
        console.error('Erro global:', event.error);
        mostrarAlerta('Ocorreu um erro inesperado', 'danger');
    });
    
    // Listener para promises rejeitadas
    window.addEventListener('unhandledrejection', (event) => {
        console.error('Promise rejeitada:', event.reason);
        mostrarAlerta('Erro de processamento', 'danger');
    });
}

// ==============================================================================
// INICIALIZAÇÃO AUTOMÁTICA
// ==============================================================================

// Inicializar quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', inicializarApp);

// Exportar funções para uso global
window.SimuladorOrbital = {
    executarSimulacao,
    carregarSimulacoes,
    carregarDetalhesSimulacao,
    carregarGrafico,
    mostrarAlerta,
    formatarDistancia,
    formatarVelocidade,
    formatarMassa,
    formatarEnergia,
    criarGraficoLinha,
    criarGraficoBarras,
    CONSTANTES
};
