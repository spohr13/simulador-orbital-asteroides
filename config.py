# ==============================================================================
# ARQUIVO DE CONFIGURAÇÃO DO SIMULADOR ORBITAL v2.0
# ==============================================================================

"""
Configurações centralizadas para o simulador orbital.
Este arquivo permite personalizar facilmente os parâmetros do simulador.
"""

import numpy as np
from typing import Dict, Any, List, Tuple


# ==============================================================================
# CONFIGURAÇÕES DE SIMULAÇÃO
# ==============================================================================

class ConfigSimulacao:
    """Configurações gerais de simulação."""
    
    # Passos de tempo padrão (em segundos)
    DT_RAPIDO = 7200      # 2 horas - para simulações longas
    DT_PADRAO = 3600      # 1 hora - uso geral
    DT_PRECISO = 900      # 15 min - alta precisão
    DT_ULTRA_PRECISO = 300 # 5 min - máxima precisão
    
    # Tempos de simulação padrão (em anos)
    TEMPO_CURTO = 0.01    # 3.65 dias
    TEMPO_MEDIO = 0.1     # 36.5 dias
    TEMPO_LONGO = 1.0     # 1 ano
    TEMPO_MUITO_LONGO = 10.0  # 10 anos
    
    # Configurações de progresso
    MOSTRAR_PROGRESSO = True
    FREQUENCIA_PROGRESSO = 20  # A cada N% da simulação
    
    # Configurações de validação
    VERIFICAR_CONSERVACAO_FREQUENCIA = 100  # A cada N passos
    TOLERANCIA_ENERGIA = 1e-6
    TOLERANCIA_MOMENTO = 1e-6


# ==============================================================================
# CONFIGURAÇÕES DE CENÁRIOS
# ==============================================================================

class ConfigCenarios:
    """Configurações para cenários pré-definidos."""
    
    # Sistema Solar Básico
    SISTEMA_SOLAR_BASICO = {
        "dt": ConfigSimulacao.DT_PADRAO,
        "tempo": ConfigSimulacao.TEMPO_LONGO,
        "incluir_lua": True
    }
    
    # Cenário de Impacto
    IMPACTO_DIRETO = {
        "dt": ConfigSimulacao.DT_PRECISO,
        "tempo": ConfigSimulacao.TEMPO_CURTO,
        "massa_asteroide": 1e11,  # 100 milhões de toneladas
        "distancia_inicial": 20,  # raios terrestres
        "velocidade_aproximacao": 20000  # m/s
    }
    
    # Apophis
    APOPHIS = {
        "dt": ConfigSimulacao.DT_PADRAO,
        "tempo": ConfigSimulacao.TEMPO_MUITO_LONGO,
        "usar_parametros_reais": True
    }
    
    # Sistema Solar Completo
    SISTEMA_SOLAR_COMPLETO = {
        "dt": ConfigSimulacao.DT_RAPIDO,
        "tempo": ConfigSimulacao.TEMPO_LONGO,
        "incluir_planetas_externos": True
    }
    
    # Teste de Conservação
    TESTE_CONSERVACAO = {
        "dt": ConfigSimulacao.DT_PADRAO,
        "tempo": ConfigSimulacao.TEMPO_LONGO,
        "verificar_fisica": True
    }


# ==============================================================================
# CONFIGURAÇÕES DE VISUALIZAÇÃO
# ==============================================================================

class ConfigVisualizacao:
    """Configurações para visualização e gráficos."""
    
    # Tamanhos de figura
    FIGURA_PADRAO = (12, 8)
    FIGURA_GRANDE = (15, 10)
    FIGURA_PEQUENA = (8, 6)
    
    # Configurações de plotagem
    LINHA_ESPESSURA = 2
    PONTO_TAMANHO = 8
    TRANSPARENCIA = 0.7
    
    # Cores personalizadas
    CORES_PERSONALIZADAS = {
        "sol": "#FFD700",      # Dourado
        "terra": "#4169E1",    # Azul real
        "lua": "#C0C0C0",      # Prata
        "asteroide": "#DC143C", # Vermelho escuro
        "jupiter": "#FF8C00",   # Laranja escuro
        "marte": "#CD5C5C",     # Vermelho indiano
        "venus": "#FFD700",     # Dourado
        "mercurio": "#8B4513"   # Marrom
    }
    
    # Configurações de animação
    FPS_PADRAO = 30
    DURACAO_MAXIMA = 60  # segundos
    
    # Configurações de salvamento
    DPI_ALTA = 300
    DPI_PADRAO = 150
    FORMATO_PADRAO = "png"
    COMPRESSAR_IMAGENS = True


# ==============================================================================
# CONFIGURAÇÕES DE ANÁLISE
# ==============================================================================

class ConfigAnalise:
    """Configurações para análise de resultados."""
    
    # Precisões de formatação
    PRECISAO_DISTANCIA = 2      # casas decimais para distâncias (km)
    PRECISAO_VELOCIDADE = 2     # casas decimais para velocidades (km/s)
    PRECISAO_ENERGIA = 2        # casas decimais para energias (J)
    PRECISAO_TEMPO = 4          # casas decimais para tempos (anos)
    PRECISAO_MASSA = 1          # casas decimais para massas (Mt)
    
    # Limites para classificação
    LIMITE_APROXIMACAO_PERIGOSA = 10  # raios terrestres
    LIMITE_APROXIMACAO_CRITICA = 2    # raios terrestres
    LIMITE_APROXIMACAO_MUITO_PROXIMA = 5  # raios terrestres
    
    # Limites para classificação de impacto
    LIMITES_ENERGIA_IMPACTO = {
        "muito_pequeno": 0.01,    # megatons TNT
        "pequeno": 0.1,
        "medio": 1.0,
        "grande": 10.0,
        "muito_grande": 100.0,
        "catastrofico": 1000.0
    }
    
    # Configurações de relatório
    INCLUIR_GRAFICOS = True
    INCLUIR_ANALISE_DETALHADA = True
    INCLUIR_VALIDACAO_FISICA = True
    INCLUIR_COMPARACOES = True


# ==============================================================================
# CONFIGURAÇÕES DE ARQUIVOS
# ==============================================================================

class ConfigArquivos:
    """Configurações para salvamento e carregamento."""
    
    # Diretórios padrão
    DIR_RESULTADOS = "resultados"
    DIR_GRAFICOS = "graficos"
    DIR_DADOS = "dados"
    DIR_RELATORIOS = "relatorios"
    
    # Configurações de nomeação
    PREFIXO_SIMULACAO = "simulacao"
    PREFIXO_GRAFICO = "grafico"
    PREFIXO_RELATORIO = "relatorio"
    
    # Formatos suportados
    FORMATOS_SAIDA = ["txt", "json", "csv", "xml"]
    FORMATOS_GRAFICOS = ["png", "jpg", "pdf", "svg"]
    
    # Configurações de backup
    CRIAR_BACKUP = True
    MANTER_HISTORICO = True
    LIMITE_HISTORICO = 100  # número de simulações antigas


# ==============================================================================
# CONFIGURAÇÕES DE PERFORMANCE
# ==============================================================================

class ConfigPerformance:
    """Configurações para otimização de performance."""
    
    # Limites de simulação
    MAX_PASSOS_SIMULACAO = 1000000
    MAX_TEMPO_SIMULACAO = 365.25 * 24 * 3600 * 100  # 100 anos em segundos
    
    # Configurações de memória
    LIMITE_HISTORICO_POSICOES = 10000  # máximo de pontos salvos por corpo
    COMPRIMIR_DADOS = True
    
    # Configurações de paralelização
    USAR_MULTIPROCESSING = False  # para futuras implementações
    NUM_THREADS = 1
    
    # Configurações de cache
    CACHE_CALCULOS = True
    LIMITE_CACHE = 1000


# ==============================================================================
# CONFIGURAÇÕES DE DEBUGGING
# ==============================================================================

class ConfigDebug:
    """Configurações para debugging e desenvolvimento."""
    
    # Níveis de log
    LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
    SALVAR_LOGS = True
    DIR_LOGS = "logs"
    
    # Configurações de debug
    DEBUG_MODO = False
    VERIFICAR_INPUTS = True
    VALIDAR_SISTEMAS = True
    
    # Configurações de teste
    EXECUTAR_TESTES_AUTOMATICOS = False
    GERAR_DADOS_TESTE = False


# ==============================================================================
# CONFIGURAÇÕES PADRÃO
# ==============================================================================

class ConfigPadrao:
    """Configurações padrão do simulador."""
    
    # Configurações gerais
    SIMULACAO = ConfigSimulacao()
    CENARIOS = ConfigCenarios()
    VISUALIZACAO = ConfigVisualizacao()
    ANALISE = ConfigAnalise()
    ARQUIVOS = ConfigArquivos()
    PERFORMANCE = ConfigPerformance()
    DEBUG = ConfigDebug()
    
    # Versão
    VERSAO = "2.0"
    NOME = "Simulador Orbital de Asteroides"
    AUTOR = "Assistente IA"
    DATA = "2025"
    
    # Configurações de compatibilidade
    COMPATIBILIDADE_V1 = True
    MIGRAR_DADOS_V1 = True


# ==============================================================================
# FUNÇÕES DE CONFIGURAÇÃO
# ==============================================================================

def obter_config_padrao() -> Dict[str, Any]:
    """Retorna a configuração padrão como dicionário."""
    return {
        "simulacao": {
            "dt_padrao": ConfigSimulacao.DT_PADRAO,
            "tempo_padrao": ConfigSimulacao.TEMPO_MEDIO,
            "mostrar_progresso": ConfigSimulacao.MOSTRAR_PROGRESSO,
            "tolerancia_energia": ConfigSimulacao.TOLERANCIA_ENERGIA
        },
        "visualizacao": {
            "figura_tamanho": ConfigVisualizacao.FIGURA_PADRAO,
            "linha_espessura": ConfigVisualizacao.LINHA_ESPESSURA,
            "fps_animacao": ConfigVisualizacao.FPS_PADRAO
        },
        "analise": {
            "precisao_distancia": ConfigAnalise.PRECISAO_DISTANCIA,
            "limite_aproximacao_perigosa": ConfigAnalise.LIMITE_APROXIMACAO_PERIGOSA,
            "incluir_graficos": ConfigAnalise.INCLUIR_GRAFICOS
        },
        "arquivos": {
            "dir_resultados": ConfigArquivos.DIR_RESULTADOS,
            "formatos_saida": ConfigArquivos.FORMATOS_SAIDA,
            "criar_backup": ConfigArquivos.CRIAR_BACKUP
        }
    }


def carregar_config_arquivo(caminho: str) -> Dict[str, Any]:
    """Carrega configuração de um arquivo JSON."""
    import json
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Arquivo de configuração não encontrado: {caminho}")
        return obter_config_padrao()
    except json.JSONDecodeError:
        print(f"Erro ao decodificar arquivo de configuração: {caminho}")
        return obter_config_padrao()


def salvar_config_arquivo(config: Dict[str, Any], caminho: str):
    """Salva configuração em um arquivo JSON."""
    import json
    import os
    
    # Criar diretório se não existir
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    
    try:
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"Configuração salva em: {caminho}")
    except Exception as e:
        print(f"Erro ao salvar configuração: {e}")


def criar_config_personalizada(**kwargs) -> Dict[str, Any]:
    """Cria uma configuração personalizada baseada nos parâmetros fornecidos."""
    config = obter_config_padrao()
    
    # Atualizar com parâmetros fornecidos
    for chave, valor in kwargs.items():
        if chave in config:
            config[chave].update(valor)
        else:
            config[chave] = valor
    
    return config


def validar_config(config: Dict[str, Any]) -> List[str]:
    """Valida uma configuração e retorna lista de avisos."""
    avisos = []
    
    # Validar configurações de simulação
    if "simulacao" in config:
        sim = config["simulacao"]
        if "dt_padrao" in sim and sim["dt_padrao"] <= 0:
            avisos.append("Passo de tempo deve ser positivo")
        if "tempo_padrao" in sim and sim["tempo_padrao"] <= 0:
            avisos.append("Tempo de simulação deve ser positivo")
    
    # Validar configurações de visualização
    if "visualizacao" in config:
        vis = config["visualizacao"]
        if "figura_tamanho" in vis:
            tamanho = vis["figura_tamanho"]
            if len(tamanho) != 2 or any(x <= 0 for x in tamanho):
                avisos.append("Tamanho da figura deve ser (largura, altura) com valores positivos")
    
    return avisos


# ==============================================================================
# CONFIGURAÇÕES ESPECÍFICAS POR CENÁRIO
# ==============================================================================

def obter_config_cenario(nome_cenario: str) -> Dict[str, Any]:
    """Retorna configuração específica para um cenário."""
    configs_cenarios = {
        "sistema_solar_basico": {
            "dt": ConfigSimulacao.DT_PADRAO,
            "tempo": ConfigSimulacao.TEMPO_LONGO,
            "visualizacao": {"incluir_orbita_terra": True}
        },
        "impacto_direto": {
            "dt": ConfigSimulacao.DT_PRECISO,
            "tempo": ConfigSimulacao.TEMPO_CURTO,
            "analise": {"focar_impacto": True}
        },
        "apophis": {
            "dt": ConfigSimulacao.DT_PADRAO,
            "tempo": ConfigSimulacao.TEMPO_MUITO_LONGO,
            "analise": {"usar_parametros_reais": True}
        },
        "teste_conservacao": {
            "dt": ConfigSimulacao.DT_PADRAO,
            "tempo": ConfigSimulacao.TEMPO_LONGO,
            "debug": {"verificar_fisica": True}
        }
    }
    
    return configs_cenarios.get(nome_cenario, obter_config_padrao())


def aplicar_config_sistema(sistema, config: Dict[str, Any]):
    """Aplica configurações a um sistema gravitacional."""
    if "simulacao" in config:
        sim_config = config["simulacao"]
        if "dt" in sim_config:
            sistema.dt = sim_config["dt"]
        if "tolerancia_energia" in sim_config:
            sistema.tolerancia_energia = sim_config["tolerancia_energia"]


# ==============================================================================
# EXEMPLO DE USO
# ==============================================================================

if __name__ == "__main__":
    # Exemplo de uso das configurações
    print("Configurações do Simulador Orbital v2.0")
    print("="*50)
    
    # Obter configuração padrão
    config = obter_config_padrao()
    print("Configuração padrão carregada")
    
    # Validar configuração
    avisos = validar_config(config)
    if avisos:
        print("Avisos encontrados:")
        for aviso in avisos:
            print(f"  - {aviso}")
    else:
        print("Configuração válida!")
    
    # Salvar configuração
    salvar_config_arquivo(config, "config_personalizada.json")
    
    # Criar configuração personalizada
    config_personalizada = criar_config_personalizada(
        simulacao={"dt_padrao": 1800, "tempo_padrao": 0.5},
        visualizacao={"figura_tamanho": (15, 10)}
    )
    
    print("Configuração personalizada criada")
    print(f"DT personalizado: {config_personalizada['simulacao']['dt_padrao']}s")
    print(f"Tamanho da figura: {config_personalizada['visualizacao']['figura_tamanho']}")
