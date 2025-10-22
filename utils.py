# ==============================================================================
# FUNÇÕES UTILITÁRIAS PARA O SIMULADOR ORBITAL
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import List, Tuple, Dict, Any, Optional, Union
import json
import os
from datetime import datetime

from constants import *
from celestial_body import CorpoCeleste
from gravitational_system import SistemaGravitacional
from simulation_result import ResultadoSimulacao


def converter_unidades(valor: float, unidade_origem: str, unidade_destino: str) -> float:
    """
    Converte valores entre diferentes unidades.
    
    Args:
        valor: Valor a ser convertido
        unidade_origem: Unidade de origem
        unidade_destino: Unidade de destino
        
    Returns:
        Valor convertido
    """
    # Conversões de distância
    if unidade_origem == "m" and unidade_destino == "km":
        return valor / 1000
    elif unidade_origem == "km" and unidade_destino == "m":
        return valor * 1000
    elif unidade_origem == "m" and unidade_destino == "UA":
        return valor / UA
    elif unidade_origem == "UA" and unidade_destino == "m":
        return valor * UA
    elif unidade_origem == "km" and unidade_destino == "UA":
        return valor * 1000 / UA
    elif unidade_origem == "UA" and unidade_destino == "km":
        return valor * UA / 1000
    
    # Conversões de tempo
    elif unidade_origem == "s" and unidade_destino == "h":
        return valor / 3600
    elif unidade_origem == "h" and unidade_destino == "s":
        return valor * 3600
    elif unidade_origem == "s" and unidade_destino == "d":
        return valor / 86400
    elif unidade_origem == "d" and unidade_destino == "s":
        return valor * 86400
    elif unidade_origem == "s" and unidade_destino == "a":
        return valor / ANOS_EM_SEGUNDOS
    elif unidade_origem == "a" and unidade_destino == "s":
        return valor * ANOS_EM_SEGUNDOS
    
    # Conversões de velocidade
    elif unidade_origem == "m/s" and unidade_destino == "km/s":
        return valor / 1000
    elif unidade_origem == "km/s" and unidade_destino == "m/s":
        return valor * 1000
    
    # Conversões de massa
    elif unidade_origem == "kg" and unidade_destino == "t":
        return valor / 1000
    elif unidade_origem == "t" and unidade_destino == "kg":
        return valor * 1000
    elif unidade_origem == "kg" and unidade_destino == "Mt":
        return valor / 1e9
    elif unidade_origem == "Mt" and unidade_destino == "kg":
        return valor * 1e9
    
    else:
        raise ValueError(f"Conversão não suportada: {unidade_origem} -> {unidade_destino}")


def calcular_orbita_circular(massa_central: float, distancia: float) -> float:
    """
    Calcula a velocidade orbital circular.
    
    Args:
        massa_central: Massa do corpo central em kg
        distancia: Distância do centro em metros
        
    Returns:
        Velocidade orbital em m/s
    """
    return np.sqrt(G * massa_central / distancia)


def calcular_periodo_orbital(massa_central: float, distancia: float) -> float:
    """
    Calcula o período orbital.
    
    Args:
        massa_central: Massa do corpo central em kg
        distancia: Distância do centro em metros
        
    Returns:
        Período orbital em segundos
    """
    return 2 * np.pi * np.sqrt(distancia**3 / (G * massa_central))


def calcular_energia_orbital(massa: float, massa_central: float, distancia: float) -> float:
    """
    Calcula a energia orbital total.
    
    Args:
        massa: Massa do corpo em órbita em kg
        massa_central: Massa do corpo central em kg
        distancia: Distância entre os corpos em metros
        
    Returns:
        Energia orbital total em Joules
    """
    return -G * massa * massa_central / (2 * distancia)


def classificar_orbita(energia: float) -> str:
    """
    Classifica o tipo de órbita baseado na energia.
    
    Args:
        energia: Energia orbital total em Joules
        
    Returns:
        Tipo de órbita
    """
    if energia < 0:
        return "Elíptica"
    elif energia == 0:
        return "Parabólica"
    else:
        return "Hiperbólica"


def plotar_trajetorias(sistema: SistemaGravitacional, 
                      titulo: str = "Trajetórias dos Corpos",
                      salvar: bool = False,
                      arquivo: str = None) -> None:
    """
    Plota as trajetórias dos corpos do sistema.
    
    Args:
        sistema: Sistema gravitacional
        titulo: Título do gráfico
        salvar: Se deve salvar o gráfico
        arquivo: Nome do arquivo para salvar
    """
    plt.figure(figsize=(12, 8))
    
    for corpo in sistema.corpos:
        x, y = corpo.get_trajetoria_2d()
        if len(x) > 0:
            plt.plot(x/UA, y/UA, '-', label=corpo.nome, color=corpo.cor, linewidth=2)
            plt.plot(x[0]/UA, y[0]/UA, 'o', color=corpo.cor, markersize=8)
            plt.plot(x[-1]/UA, y[-1]/UA, 's', color=corpo.cor, markersize=6)
    
    plt.xlabel('x (UA)')
    plt.ylabel('y (UA)')
    plt.title(titulo)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    
    if salvar:
        if arquivo is None:
            arquivo = f"trajetorias_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(arquivo, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {arquivo}")
    
    plt.show()


def plotar_distancia_tempo(sistema: SistemaGravitacional,
                          corpo1_nome: str = "Terra",
                          corpo2_nome: str = "Asteroide",
                          salvar: bool = False,
                          arquivo: str = None) -> None:
    """
    Plota a distância entre dois corpos ao longo do tempo.
    
    Args:
        sistema: Sistema gravitacional
        corpo1_nome: Nome do primeiro corpo
        corpo2_nome: Nome do segundo corpo
        salvar: Se deve salvar o gráfico
        arquivo: Nome do arquivo para salvar
    """
    corpo1 = sistema.get_corpo(corpo1_nome)
    corpo2 = sistema.get_corpo(corpo2_nome)
    
    if corpo1 is None or corpo2 is None:
        print(f"Corpos não encontrados: {corpo1_nome}, {corpo2_nome}")
        return
    
    # Calcular distâncias
    n_pontos = min(len(corpo1.historico_posicao), len(corpo2.historico_posicao))
    tempos = np.array(corpo1.historico_tempo[:n_pontos]) / ANOS_EM_SEGUNDOS
    distancias = []
    
    for i in range(n_pontos):
        d = np.linalg.norm(corpo2.historico_posicao[i] - corpo1.historico_posicao[i])
        distancias.append(d)
    
    distancias = np.array(distancias)
    
    plt.figure(figsize=(12, 6))
    plt.plot(tempos, distancias/1000, 'b-', linewidth=2, 
             label=f'Distância {corpo1_nome}-{corpo2_nome}')
    plt.axhline(R_TERRA/1000, color='green', linestyle='--', linewidth=2, 
               alpha=0.7, label='Raio da Terra')
    
    # Marcar eventos especiais
    if sistema.resultado.houve_colisao:
        tempo_colisao = sistema.resultado.tempo_colisao / ANOS_EM_SEGUNDOS
        plt.axvline(tempo_colisao, color='red', linestyle=':', linewidth=3, 
                   label='Momento do Impacto')
    
    if sistema.resultado.aproximacao_perigosa:
        tempo_aproximacao = sistema.resultado.tempo_aproximacao_perigosa / ANOS_EM_SEGUNDOS
        plt.axvline(tempo_aproximacao, color='orange', linestyle=':', linewidth=2, 
                   label='Aproximação Perigosa')
    
    plt.xlabel('Tempo (anos)')
    plt.ylabel('Distância (km)')
    plt.title(f'Distância entre {corpo1_nome} e {corpo2_nome}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    
    if salvar:
        if arquivo is None:
            arquivo = f"distancia_tempo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(arquivo, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {arquivo}")
    
    plt.show()


def plotar_energia_tempo(sistema: SistemaGravitacional,
                        salvar: bool = False,
                        arquivo: str = None) -> None:
    """
    Plota a evolução da energia do sistema ao longo do tempo.
    
    Args:
        sistema: Sistema gravitacional
        salvar: Se deve salvar o gráfico
        arquivo: Nome do arquivo para salvar
    """
    # Calcular energias ao longo do tempo
    tempos = []
    energias = []
    
    for i, tempo in enumerate(sistema.corpos[0].historico_tempo):
        # Restaurar estado do sistema
        for j, corpo in enumerate(sistema.corpos):
            corpo.posicao = corpo.historico_posicao[i]
            corpo.velocidade = corpo.historico_velocidade[i]
        
        tempos.append(tempo / ANOS_EM_SEGUNDOS)
        energias.append(sistema.energia_total())
    
    plt.figure(figsize=(12, 6))
    plt.plot(tempos, energias, 'b-', linewidth=2, label='Energia Total')
    plt.axhline(sistema.resultado.energia_inicial, color='red', linestyle='--', 
               alpha=0.7, label='Energia Inicial')
    
    plt.xlabel('Tempo (anos)')
    plt.ylabel('Energia (J)')
    plt.title('Evolução da Energia do Sistema')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    
    if salvar:
        if arquivo is None:
            arquivo = f"energia_tempo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(arquivo, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {arquivo}")
    
    plt.show()


def criar_animacao(sistema: SistemaGravitacional,
                   titulo: str = "Animação Orbital",
                   salvar: bool = False,
                   arquivo: str = None,
                   fps: int = 30) -> None:
    """
    Cria uma animação das trajetórias dos corpos.
    
    Args:
        sistema: Sistema gravitacional
        titulo: Título da animação
        salvar: Se deve salvar a animação
        arquivo: Nome do arquivo para salvar
        fps: Frames por segundo
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Configurar limites do gráfico
    x_min, x_max, y_min, y_max = float('inf'), float('-inf'), float('inf'), float('-inf')
    
    for corpo in sistema.corpos:
        x, y = corpo.get_trajetoria_2d()
        if len(x) > 0:
            x_min = min(x_min, np.min(x))
            x_max = max(x_max, np.max(x))
            y_min = min(y_min, np.min(y))
            y_max = max(y_max, np.max(y))
    
    # Adicionar margem
    margem = 0.1 * max(x_max - x_min, y_max - y_min)
    ax.set_xlim(x_min - margem, x_max + margem)
    ax.set_ylim(y_min - margem, y_max + margem)
    
    # Inicializar elementos gráficos
    pontos = []
    linhas = []
    
    for corpo in sistema.corpos:
        x, y = corpo.get_trajetoria_2d()
        if len(x) > 0:
            linha, = ax.plot([], [], '-', color=corpo.cor, linewidth=2, alpha=0.7)
            ponto, = ax.plot([], [], 'o', color=corpo.cor, markersize=8)
            linhas.append(linha)
            pontos.append(ponto)
    
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_title(titulo)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    def animar(frame):
        for i, corpo in enumerate(sistema.corpos):
            x, y = corpo.get_trajetoria_2d()
            if len(x) > 0:
                # Mostrar trajetória até o frame atual
                idx = min(frame, len(x) - 1)
                linhas[i].set_data(x[:idx+1], y[:idx+1])
                pontos[i].set_data([x[idx]], [y[idx]])
        
        return linhas + pontos
    
    # Criar animação
    anim = FuncAnimation(fig, animar, frames=len(sistema.corpos[0].historico_posicao),
                        interval=1000//fps, blit=True, repeat=True)
    
    if salvar:
        if arquivo is None:
            arquivo = f"animacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.gif"
        anim.save(arquivo, writer='pillow', fps=fps)
        print(f"Animação salva em: {arquivo}")
    
    plt.show()


def salvar_simulacao(sistema: SistemaGravitacional, 
                    resultado: ResultadoSimulacao,
                    diretorio: str = "resultados") -> str:
    """
    Salva os resultados de uma simulação em arquivos.
    
    Args:
        sistema: Sistema gravitacional
        resultado: Resultado da simulação
        diretorio: Diretório para salvar os arquivos
        
    Returns:
        Caminho do diretório criado
    """
    # Criar diretório se não existir
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    dir_simulacao = os.path.join(diretorio, f"simulacao_{timestamp}")
    os.makedirs(dir_simulacao, exist_ok=True)
    
    # Salvar relatório
    resultado.salvar_relatorio(os.path.join(dir_simulacao, "relatorio.txt"))
    resultado.salvar_json(os.path.join(dir_simulacao, "resultado.json"))
    
    # Salvar dados dos corpos
    dados_corpos = {}
    for corpo in sistema.corpos:
        dados_corpos[corpo.nome] = {
            'massa': corpo.massa,
            'posicao_inicial': corpo.posicao.tolist(),
            'velocidade_inicial': corpo.velocidade.tolist(),
            'raio_fisico': corpo.raio_fisico,
            'densidade': corpo.densidade,
            'tipo': corpo.tipo,
            'trajetoria': {
                'posicoes': [pos.tolist() for pos in corpo.historico_posicao],
                'velocidades': [vel.tolist() for vel in corpo.historico_velocidade],
                'tempos': corpo.historico_tempo
            }
        }
    
    with open(os.path.join(dir_simulacao, "dados_corpos.json"), 'w', encoding='utf-8') as f:
        json.dump(dados_corpos, f, indent=2, ensure_ascii=False)
    
    # Salvar configuração do sistema
    config_sistema = {
        'nome': sistema.nome,
        'dt': sistema.dt,
        'tempo_simulacao': resultado.tempo_simulacao,
        'numero_passos': resultado.numero_passos,
        'versao': sistema.versao,
        'timestamp': timestamp
    }
    
    with open(os.path.join(dir_simulacao, "config_sistema.json"), 'w', encoding='utf-8') as f:
        json.dump(config_sistema, f, indent=2, ensure_ascii=False)
    
    print(f"Simulação salva em: {dir_simulacao}")
    return dir_simulacao


def carregar_simulacao(diretorio: str) -> Tuple[SistemaGravitacional, ResultadoSimulacao]:
    """
    Carrega uma simulação salva.
    
    Args:
        diretorio: Diretório da simulação
        
    Returns:
        Tupla com sistema e resultado
    """
    # Carregar configuração do sistema
    with open(os.path.join(diretorio, "config_sistema.json"), 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Criar sistema
    sistema = SistemaGravitacional(dt=config['dt'], nome=config['nome'])
    
    # Carregar dados dos corpos
    with open(os.path.join(diretorio, "dados_corpos.json"), 'r', encoding='utf-8') as f:
        dados_corpos = json.load(f)
    
    for nome, dados in dados_corpos.items():
        corpo = CorpoCeleste(
            nome=nome,
            massa=dados['massa'],
            posicao=dados['posicao_inicial'],
            velocidade=dados['velocidade_inicial'],
            raio_fisico=dados['raio_fisico'],
            densidade=dados['densidade'],
            tipo=dados['tipo']
        )
        
        # Restaurar trajetória
        corpo.historico_posicao = [np.array(pos) for pos in dados['trajetoria']['posicoes']]
        corpo.historico_velocidade = [np.array(vel) for vel in dados['trajetoria']['velocidades']]
        corpo.historico_tempo = dados['trajetoria']['tempos']
        
        sistema.adicionar_corpo(corpo)
    
    # Carregar resultado
    with open(os.path.join(diretorio, "resultado.json"), 'r', encoding='utf-8') as f:
        dados_resultado = json.load(f)
    
    resultado = ResultadoSimulacao()
    # Preencher resultado com dados carregados
    # (implementação detalhada seria muito longa aqui)
    
    return sistema, resultado


def gerar_relatorio_completo(sistema: SistemaGravitacional, 
                           resultado: ResultadoSimulacao,
                           salvar: bool = True,
                           arquivo: str = None) -> str:
    """
    Gera um relatório completo com gráficos.
    
    Args:
        sistema: Sistema gravitacional
        resultado: Resultado da simulação
        salvar: Se deve salvar os gráficos
        arquivo: Prefixo do nome dos arquivos
        
    Returns:
        Texto do relatório
    """
    relatorio = []
    relatorio.append("=" * 80)
    relatorio.append("RELATÓRIO COMPLETO DE SIMULAÇÃO ORBITAL".center(80))
    relatorio.append("=" * 80)
    relatorio.append("")
    
    # Informações do sistema
    relatorio.append("INFORMAÇÕES DO SISTEMA:")
    relatorio.append(f"  Nome: {sistema.nome}")
    relatorio.append(f"  Número de corpos: {len(sistema.corpos)}")
    relatorio.append(f"  Passo de tempo: {sistema.dt} segundos")
    relatorio.append(f"  Versão: {sistema.versao}")
    relatorio.append("")
    
    # Informações dos corpos
    relatorio.append("CORPOS PARTICIPANTES:")
    for corpo in sistema.corpos:
        relatorio.append(f"  {corpo.nome}:")
        relatorio.append(f"    Massa: {corpo.massa:.2e} kg")
        relatorio.append(f"    Raio: {corpo.raio_fisico:.0f} m")
        relatorio.append(f"    Densidade: {corpo.densidade:.0f} kg/m³")
        relatorio.append(f"    Tipo: {corpo.tipo}")
    relatorio.append("")
    
    # Adicionar relatório do resultado
    relatorio.append(resultado.gerar_relatorio())
    
    # Gerar gráficos se solicitado
    if salvar:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        prefixo = arquivo if arquivo else f"relatorio_{timestamp}"
        
        plotar_trajetorias(sistema, salvar=True, arquivo=f"{prefixo}_trajetorias.png")
        plotar_distancia_tempo(sistema, salvar=True, arquivo=f"{prefixo}_distancia.png")
        plotar_energia_tempo(sistema, salvar=True, arquivo=f"{prefixo}_energia.png")
    
    return "\n".join(relatorio)


def validar_sistema(sistema: SistemaGravitacional) -> List[str]:
    """
    Valida um sistema gravitacional e retorna avisos.
    
    Args:
        sistema: Sistema a ser validado
        
    Returns:
        Lista de avisos encontrados
    """
    avisos = []
    
    # Verificar se há corpos
    if len(sistema.corpos) < 2:
        avisos.append("Sistema deve ter pelo menos 2 corpos")
    
    # Verificar massas
    for corpo in sistema.corpos:
        if corpo.massa <= 0:
            avisos.append(f"Massa inválida para {corpo.nome}: {corpo.massa}")
    
    # Verificar posições
    for i, corpo1 in enumerate(sistema.corpos):
        for j, corpo2 in enumerate(sistema.corpos[i+1:], i+1):
            distancia = corpo1.distancia_para(corpo2)
            raio_total = corpo1.raio_fisico + corpo2.raio_fisico
            if distancia < raio_total:
                avisos.append(f"Corpos {corpo1.nome} e {corpo2.nome} estão sobrepostos")
    
    # Verificar passo de tempo
    if sistema.dt <= 0:
        avisos.append("Passo de tempo deve ser positivo")
    elif sistema.dt > MAX_PASSO_TEMPO:
        avisos.append(f"Passo de tempo muito grande: {sistema.dt}s")
    elif sistema.dt < MIN_PASSO_TEMPO:
        avisos.append(f"Passo de tempo muito pequeno: {sistema.dt}s")
    
    return avisos


def comparar_simulacoes(resultados: List[ResultadoSimulacao],
                          nomes: List[str] = None) -> None:
    """
    Compara múltiplas simulações em gráficos.
    
    Args:
        resultados: Lista de resultados
        nomes: Nomes para as simulações
    """
    if nomes is None:
        nomes = [f"Simulação {i+1}" for i in range(len(resultados))]
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Distâncias mínimas
    distancias = [r.distancia_minima/1000 for r in resultados]
    axes[0,0].bar(nomes, distancias)
    axes[0,0].set_title('Distância Mínima (km)')
    axes[0,0].set_ylabel('Distância (km)')
    
    # Energias de impacto
    energias = [r.equivalente_tnt if r.houve_colisao else 0 for r in resultados]
    axes[0,1].bar(nomes, energias)
    axes[0,1].set_title('Energia de Impacto (megatons TNT)')
    axes[0,1].set_ylabel('Energia (Mt)')
    
    # Erros de conservação
    erros_energia = [abs(r.erro_energia_relativo) for r in resultados]
    axes[1,0].bar(nomes, erros_energia)
    axes[1,0].set_title('Erro de Conservação de Energia')
    axes[1,0].set_ylabel('Erro Relativo')
    axes[1,0].set_yscale('log')
    
    # Tempos de simulação
    tempos = [r.tempo_simulacao/ANOS_EM_SEGUNDOS for r in resultados]
    axes[1,1].bar(nomes, tempos)
    axes[1,1].set_title('Tempo de Simulação (anos)')
    axes[1,1].set_ylabel('Tempo (anos)')
    
    plt.tight_layout()
    plt.show()
