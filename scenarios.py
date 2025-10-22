# ==============================================================================
# CENÁRIOS PRÉ-CONFIGURADOS PARA SIMULAÇÃO ORBITAL
# ==============================================================================

import numpy as np
from typing import List, Dict, Any, Optional

from constants import *
from celestial_body import CorpoCeleste
from gravitational_system import SistemaGravitacional


def criar_sistema_solar_basico() -> SistemaGravitacional:
    """
    Cria um sistema solar básico com Sol, Terra e Lua.
    """
    sistema = SistemaGravitacional(dt=DT_PADRAO, nome="Sistema Solar Básico")
    
    # Sol
    sol = CorpoCeleste(
        nome="Sol",
        massa=M_SOL,
        posicao=[0, 0, 0],
        velocidade=[0, 0, 0],
        cor=COR_SOL,
        raio_visual=TAMANHO_SOL,
        tipo=TIPO_SOL
    )
    
    # Terra
    v_orbital_terra = np.sqrt(G * M_SOL / UA)
    terra = CorpoCeleste(
        nome="Terra",
        massa=M_TERRA,
        posicao=[UA, 0, 0],
        velocidade=[0, v_orbital_terra, 0],
        cor=COR_TERRA,
        raio_visual=TAMANHO_TERRA,
        tipo=TIPO_PLANETA
    )
    
    # Lua
    distancia_terra_lua = 384400000  # 384,400 km
    v_orbital_lua = np.sqrt(G * M_TERRA / distancia_terra_lua)
    lua = CorpoCeleste(
        nome="Lua",
        massa=M_LUA,
        posicao=[UA + distancia_terra_lua, 0, 0],
        velocidade=[0, v_orbital_terra + v_orbital_lua, 0],
        cor=COR_LUA,
        raio_visual=TAMANHO_LUA,
        tipo=TIPO_LUA
    )
    
    sistema.adicionar_corpo(sol)
    sistema.adicionar_corpo(terra)
    sistema.adicionar_corpo(lua)
    
    return sistema


def criar_sistema_impacto_direto(massa_asteroide: float = 1e11,
                                 distancia_inicial: float = R_TERRA * 20,
                                 velocidade_aproximacao: float = 20000) -> SistemaGravitacional:
    """
    Cria um cenário de impacto direto com a Terra.
    
    Args:
        massa_asteroide: Massa do asteroide em kg
        distancia_inicial: Distância inicial da Terra em metros
        velocidade_aproximacao: Velocidade de aproximação em m/s
    """
    sistema = SistemaGravitacional(dt=DT_PRECISO, nome="Sistema de Impacto Direto")
    
    # Sol
    sol = CorpoCeleste(
        nome="Sol",
        massa=M_SOL,
        posicao=[0, 0, 0],
        velocidade=[0, 0, 0],
        cor=COR_SOL,
        raio_visual=TAMANHO_SOL,
        tipo=TIPO_SOL
    )
    
    # Terra
    v_orbital_terra = np.sqrt(G * M_SOL / UA)
    terra = CorpoCeleste(
        nome="Terra",
        massa=M_TERRA,
        posicao=[UA, 0, 0],
        velocidade=[0, v_orbital_terra, 0],
        cor=COR_TERRA,
        raio_visual=TAMANHO_TERRA,
        tipo=TIPO_PLANETA
    )
    
    # Asteroide em rota de colisão
    angulo = np.radians(15)  # Ângulo de aproximação rasante
    asteroide = CorpoCeleste(
        nome="Asteroide",
        massa=massa_asteroide,
        posicao=[UA + distancia_inicial * np.cos(angulo), 
                 distancia_inicial * np.sin(angulo), 0],
        velocidade=[-velocidade_aproximacao, v_orbital_terra - 3000, 0],
        cor=COR_ASTEROIDE,
        raio_visual=TAMANHO_ASTEROIDE,
        tipo=TIPO_ASTEROIDE
    )
    
    sistema.adicionar_corpo(sol)
    sistema.adicionar_corpo(terra)
    sistema.adicionar_corpo(asteroide)
    
    return sistema


def criar_sistema_apophis() -> SistemaGravitacional:
    """
    Cria sistema com asteroide Apophis com parâmetros orbitais reais.
    """
    sistema = SistemaGravitacional(dt=DT_PADRAO, nome="Sistema Apophis")
    
    # Sol
    sol = CorpoCeleste(
        nome="Sol",
        massa=M_SOL,
        posicao=[0, 0, 0],
        velocidade=[0, 0, 0],
        cor=COR_SOL,
        raio_visual=TAMANHO_SOL,
        tipo=TIPO_SOL
    )
    
    # Terra
    v_orbital_terra = np.sqrt(G * M_SOL / UA)
    terra = CorpoCeleste(
        nome="Terra",
        massa=M_TERRA,
        posicao=[UA, 0, 0],
        velocidade=[0, v_orbital_terra, 0],
        cor=COR_TERRA,
        raio_visual=TAMANHO_TERRA,
        tipo=TIPO_PLANETA
    )
    
    # Apophis com parâmetros orbitais reais
    a_apophis = 0.92 * UA  # Semi-eixo maior
    e_apophis = 0.19       # Excentricidade
    massa_apophis = 6.1e10  # ~61 milhões de toneladas
    
    # Posição no periélio
    r_perihelio = a_apophis * (1 - e_apophis)
    v_perihelio = np.sqrt(G * M_SOL * (2/r_perihelio - 1/a_apophis))
    
    # Ajustar posição para aproximação da Terra
    apophis = CorpoCeleste(
        nome="Apophis",
        massa=massa_apophis,
        posicao=[r_perihelio * 0.98, r_perihelio * 0.08, 0],
        velocidade=[-v_perihelio * 0.12, v_perihelio * 0.995, 0],
        cor=COR_ASTEROIDE,
        raio_visual=TAMANHO_ASTEROIDE,
        tipo=TIPO_ASTEROIDE
    )
    
    sistema.adicionar_corpo(sol)
    sistema.adicionar_corpo(terra)
    sistema.adicionar_corpo(apophis)
    
    return sistema


def criar_sistema_solar_completo() -> SistemaGravitacional:
    """
    Cria um sistema solar completo com todos os planetas principais.
    """
    sistema = SistemaGravitacional(dt=DT_RAPIDO, nome="Sistema Solar Completo")
    
    # Sol
    sol = CorpoCeleste(
        nome="Sol",
        massa=M_SOL,
        posicao=[0, 0, 0],
        velocidade=[0, 0, 0],
        cor=COR_SOL,
        raio_visual=TAMANHO_SOL,
        tipo=TIPO_SOL
    )
    
    # Planetas (distâncias em UA)
    planetas = [
        ("Mercurio", M_MERCURIO, 0.39, COR_MERCURIO, TAMANHO_MERCURIO),
        ("Venus", M_VENUS, 0.72, COR_VENUS, TAMANHO_VENUS),
        ("Terra", M_TERRA, 1.0, COR_TERRA, TAMANHO_TERRA),
        ("Marte", M_MARTE, 1.52, COR_MARTE, TAMANHO_MARTE),
        ("Jupiter", M_JUPITER, 5.2, COR_JUPITER, TAMANHO_JUPITER),
    ]
    
    for nome, massa, distancia_ua, cor, tamanho in planetas:
        distancia = distancia_ua * UA
        v_orbital = np.sqrt(G * M_SOL / distancia)
        
        planeta = CorpoCeleste(
            nome=nome,
            massa=massa,
            posicao=[distancia, 0, 0],
            velocidade=[0, v_orbital, 0],
            cor=cor,
            raio_visual=tamanho,
            tipo=TIPO_PLANETA
        )
        
        sistema.adicionar_corpo(planeta)
    
    sistema.adicionar_corpo(sol)
    
    return sistema


def criar_sistema_asteroide_personalizado(
    massa_asteroide: float,
    posicao_inicial: np.ndarray,
    velocidade_inicial: np.ndarray,
    nome_asteroide: str = "Asteroide",
    densidade: float = DENSIDADE_ASTEROIDE_PADRAO
) -> SistemaGravitacional:
    """
    Cria um sistema personalizado com asteroide customizado.
    
    Args:
        massa_asteroide: Massa do asteroide em kg
        posicao_inicial: Posição inicial [x, y, z] em metros
        velocidade_inicial: Velocidade inicial [vx, vy, vz] em m/s
        nome_asteroide: Nome do asteroide
        densidade: Densidade do asteroide em kg/m³
    """
    sistema = SistemaGravitacional(dt=DT_PRECISO, nome="Sistema Asteroide Personalizado")
    
    # Sol
    sol = CorpoCeleste(
        nome="Sol",
        massa=M_SOL,
        posicao=[0, 0, 0],
        velocidade=[0, 0, 0],
        cor=COR_SOL,
        raio_visual=TAMANHO_SOL,
        tipo=TIPO_SOL
    )
    
    # Terra
    v_orbital_terra = np.sqrt(G * M_SOL / UA)
    terra = CorpoCeleste(
        nome="Terra",
        massa=M_TERRA,
        posicao=[UA, 0, 0],
        velocidade=[0, v_orbital_terra, 0],
        cor=COR_TERRA,
        raio_visual=TAMANHO_TERRA,
        tipo=TIPO_PLANETA
    )
    
    # Asteroide personalizado
    asteroide = CorpoCeleste(
        nome=nome_asteroide,
        massa=massa_asteroide,
        posicao=posicao_inicial,
        velocidade=velocidade_inicial,
        cor=COR_ASTEROIDE,
        raio_visual=TAMANHO_ASTEROIDE,
        tipo=TIPO_ASTEROIDE,
        densidade=densidade
    )
    
    sistema.adicionar_corpo(sol)
    sistema.adicionar_corpo(terra)
    sistema.adicionar_corpo(asteroide)
    
    return sistema


def criar_sistema_teste_conservacao() -> SistemaGravitacional:
    """
    Cria um sistema simples para testar conservação de energia e momento angular.
    """
    sistema = SistemaGravitacional(dt=3600, nome="Sistema Teste Conservação")
    
    # Sol
    sol = CorpoCeleste(
        nome="Sol",
        massa=M_SOL,
        posicao=[0, 0, 0],
        velocidade=[0, 0, 0],
        cor=COR_SOL,
        raio_visual=TAMANHO_SOL,
        tipo=TIPO_SOL
    )
    
    # Terra em órbita circular
    v_orbital = np.sqrt(G * M_SOL / UA)
    terra = CorpoCeleste(
        nome="Terra",
        massa=M_TERRA,
        posicao=[UA, 0, 0],
        velocidade=[0, v_orbital, 0],
        cor=COR_TERRA,
        raio_visual=TAMANHO_TERRA,
        tipo=TIPO_PLANETA
    )
    
    sistema.adicionar_corpo(sol)
    sistema.adicionar_corpo(terra)
    
    return sistema


def criar_sistema_multi_asteroides(num_asteroides: int = 3) -> SistemaGravitacional:
    """
    Cria um sistema com múltiplos asteroides.
    
    Args:
        num_asteroides: Número de asteroides a criar
    """
    sistema = SistemaGravitacional(dt=DT_PADRAO, nome=f"Sistema Multi-Asteroides ({num_asteroides})")
    
    # Sol
    sol = CorpoCeleste(
        nome="Sol",
        massa=M_SOL,
        posicao=[0, 0, 0],
        velocidade=[0, 0, 0],
        cor=COR_SOL,
        raio_visual=TAMANHO_SOL,
        tipo=TIPO_SOL
    )
    
    # Terra
    v_orbital_terra = np.sqrt(G * M_SOL / UA)
    terra = CorpoCeleste(
        nome="Terra",
        massa=M_TERRA,
        posicao=[UA, 0, 0],
        velocidade=[0, v_orbital_terra, 0],
        cor=COR_TERRA,
        raio_visual=TAMANHO_TERRA,
        tipo=TIPO_PLANETA
    )
    
    sistema.adicionar_corpo(sol)
    sistema.adicionar_corpo(terra)
    
    # Criar múltiplos asteroides
    for i in range(num_asteroides):
        # Posições e velocidades aleatórias
        angulo = 2 * np.pi * i / num_asteroides
        distancia = UA * (1.2 + 0.3 * i)  # Distâncias variadas
        
        posicao = [distancia * np.cos(angulo), distancia * np.sin(angulo), 0]
        v_orbital = np.sqrt(G * M_SOL / distancia)
        velocidade = [-v_orbital * np.sin(angulo), v_orbital * np.cos(angulo), 0]
        
        # Massa variada
        massa = 1e10 * (1 + i)  # Massas crescentes
        
        asteroide = CorpoCeleste(
            nome=f"Asteroide_{i+1}",
            massa=massa,
            posicao=posicao,
            velocidade=velocidade,
            cor=COR_ASTEROIDE,
            raio_visual=TAMANHO_ASTEROIDE,
            tipo=TIPO_ASTEROIDE
        )
        
        sistema.adicionar_corpo(asteroide)
    
    return sistema


def listar_cenarios_disponiveis() -> Dict[str, str]:
    """
    Retorna uma lista dos cenários disponíveis com descrições.
    """
    return {
        "sistema_solar_basico": "Sistema solar básico (Sol, Terra, Lua)",
        "impacto_direto": "Cenário de impacto direto com a Terra",
        "apophis": "Sistema com asteroide Apophis (parâmetros reais)",
        "sistema_solar_completo": "Sistema solar completo com planetas principais",
        "asteroide_personalizado": "Sistema com asteroide personalizado",
        "teste_conservacao": "Sistema simples para testar conservação física",
        "multi_asteroides": "Sistema com múltiplos asteroides"
    }


def criar_cenario_por_nome(nome: str, **kwargs) -> SistemaGravitacional:
    """
    Cria um cenário pelo nome.
    
    Args:
        nome: Nome do cenário
        **kwargs: Parâmetros adicionais para o cenário
        
    Returns:
        SistemaGravitacional: Sistema configurado
    """
    cenarios = {
        "sistema_solar_basico": criar_sistema_solar_basico,
        "impacto_direto": lambda: criar_sistema_impacto_direto(**kwargs),
        "apophis": criar_sistema_apophis,
        "sistema_solar_completo": criar_sistema_solar_completo,
        "asteroide_personalizado": lambda: criar_sistema_asteroide_personalizado(**kwargs),
        "teste_conservacao": criar_sistema_teste_conservacao,
        "multi_asteroides": lambda: criar_sistema_multi_asteroides(**kwargs)
    }
    
    if nome not in cenarios:
        raise ValueError(f"Cenário '{nome}' não encontrado. Cenários disponíveis: {list(cenarios.keys())}")
    
    return cenarios[nome]()


def obter_parametros_cenario(nome: str) -> Dict[str, Any]:
    """
    Retorna os parâmetros necessários para um cenário.
    
    Args:
        nome: Nome do cenário
        
    Returns:
        Dict com parâmetros e seus tipos
    """
    parametros = {
        "sistema_solar_basico": {},
        "impacto_direto": {
            "massa_asteroide": (float, "Massa do asteroide em kg"),
            "distancia_inicial": (float, "Distância inicial da Terra em metros"),
            "velocidade_aproximacao": (float, "Velocidade de aproximação em m/s")
        },
        "apophis": {},
        "sistema_solar_completo": {},
        "asteroide_personalizado": {
            "massa_asteroide": (float, "Massa do asteroide em kg"),
            "posicao_inicial": (np.ndarray, "Posição inicial [x, y, z] em metros"),
            "velocidade_inicial": (np.ndarray, "Velocidade inicial [vx, vy, vz] em m/s"),
            "nome_asteroide": (str, "Nome do asteroide"),
            "densidade": (float, "Densidade do asteroide em kg/m³")
        },
        "teste_conservacao": {},
        "multi_asteroides": {
            "num_asteroides": (int, "Número de asteroides a criar")
        }
    }
    
    return parametros.get(nome, {})
