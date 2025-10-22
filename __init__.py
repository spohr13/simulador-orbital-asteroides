# ==============================================================================
# SIMULADOR ORBITAL DE ASTEROIDES v2.0 - MÓDULO PRINCIPAL
# ==============================================================================

"""
Simulador Orbital de Asteroides v2.0

Uma ferramenta modular e extensível para simulação de dinâmica orbital,
detecção de colisões e análise de risco de impacto de asteroides.

Módulos principais:
- constants: Constantes físicas e configurações
- celestial_body: Classe CorpoCeleste
- simulation_result: Classe ResultadoSimulacao  
- gravitational_system: Classe SistemaGravitacional
- scenarios: Cenários pré-configurados
- utils: Funções utilitárias
- main: Ponto de entrada principal
- config: Configurações do sistema
"""

# Importar constantes
from constants import *

# Importar classes principais
from celestial_body import CorpoCeleste
from simulation_result import ResultadoSimulacao
from gravitational_system import SistemaGravitacional

# Importar cenários
from scenarios import *

# Importar utilitários
from utils import *

# Importar configurações
from config import *

# Importar funções principais
from main import (
    demonstrar_deteccao_melhorada,
    exemplo_completo_colisao,
    teste_deteccao_colisao,
    executar_cenario_interativo
)

# Versão do simulador
__version__ = "2.0"
__author__ = "Assistente IA"
__date__ = "2025"

# Informações do módulo
__name__ = "simulador_orbital"
__description__ = "Simulador Orbital de Asteroides v2.0 - Modular e Extensível"

# Lista de módulos disponíveis
MODULOS_DISPONIVEIS = [
    "constants",
    "celestial_body", 
    "simulation_result",
    "gravitational_system",
    "scenarios",
    "utils",
    "main",
    "config"
]

# Lista de classes principais
CLASSES_PRINCIPAIS = [
    "CorpoCeleste",
    "ResultadoSimulacao", 
    "SistemaGravitacional"
]

# Lista de funções principais
FUNCOES_PRINCIPAIS = [
    "demonstrar_deteccao_melhorada",
    "exemplo_completo_colisao",
    "teste_deteccao_colisao",
    "executar_cenario_interativo"
]

# Lista de cenários disponíveis
CENARIOS_DISPONIVEIS = [
    "sistema_solar_basico",
    "impacto_direto", 
    "apophis",
    "sistema_solar_completo",
    "asteroide_personalizado",
    "teste_conservacao",
    "multi_asteroides"
]


def obter_informacoes():
    """Retorna informações sobre o simulador."""
    return {
        "nome": __name__,
        "versao": __version__,
        "autor": __author__,
        "data": __date__,
        "descricao": __description__,
        "modulos": MODULOS_DISPONIVEIS,
        "classes": CLASSES_PRINCIPAIS,
        "funcoes": FUNCOES_PRINCIPAIS,
        "cenarios": CENARIOS_DISPONIVEIS
    }


def verificar_instalacao():
    """Verifica se todos os módulos estão instalados corretamente."""
    import sys
    modulos_ok = []
    modulos_erro = []
    
    for modulo in MODULOS_DISPONIVEIS:
        try:
            __import__(modulo)
            modulos_ok.append(modulo)
        except ImportError as e:
            modulos_erro.append((modulo, str(e)))
    
    return {
        "ok": modulos_ok,
        "erro": modulos_erro,
        "total": len(MODULOS_DISPONIVEIS),
        "instalado": len(modulos_ok)
    }


def exemplo_rapido():
    """Executa um exemplo rápido do simulador."""
    print("Simulador Orbital de Asteroides v2.0 - Exemplo Rápido")
    print("="*60)
    
    # Criar sistema básico
    sistema = criar_sistema_solar_basico()
    print(f"Sistema criado: {sistema.nome}")
    print(f"Corpos: {len(sistema.corpos)}")
    
    # Simular
    print("Executando simulação...")
    resultado = sistema.simular(0.01 * ANOS_EM_SEGUNDOS, progresso=True)
    
    # Mostrar resultados
    print(f"\nResultados:")
    print(f"  Estado: {resultado.estado_final}")
    print(f"  Física válida: {resultado.fisica_valida()}")
    print(f"  Tempo simulado: {resultado.tempo_simulacao/ANOS_EM_SEGUNDOS:.4f} anos")
    
    return sistema, resultado


# Função de inicialização
def inicializar():
    """Inicializa o simulador e verifica dependências."""
    print("Inicializando Simulador Orbital v2.0...")
    
    # Verificar instalação
    status = verificar_instalacao()
    
    if status["erro"]:
        print("Avisos de instalação:")
        for modulo, erro in status["erro"]:
            print(f"  - {modulo}: {erro}")
    
    print(f"Módulos instalados: {status['instalado']}/{status['total']}")
    
    if status["instalado"] == status["total"]:
        print("Simulador inicializado com sucesso!")
        return True
    else:
        print("Alguns módulos não foram carregados corretamente.")
        return False


# Executar inicialização se chamado diretamente
if __name__ == "__main__":
    inicializar()
    exemplo_rapido()
