# ==============================================================================
# SIMULADOR ORBITAL DE ASTEROIDES - PONTO DE ENTRADA PRINCIPAL
# ==============================================================================

import sys
import argparse
from typing import Optional, Dict, Any
import numpy as np

# Importar módulos do simulador
from constants import *
from celestial_body import CorpoCeleste
from gravitational_system import SistemaGravitacional
from simulation_result import ResultadoSimulacao
from scenarios import *
from utils import *


def demonstrar_deteccao_melhorada():
    """Demonstra as melhorias na detecção de colisão."""
    print("\n" + "="*70)
    print("DEMONSTRAÇÃO: DETECÇÃO DE COLISÃO MELHORADA".center(70))
    print("="*70)
    
    print("\n1. CENÁRIO DE IMPACTO DIRETO:")
    print("-" * 40)
    
    # Teste 1: Impacto direto
    sistema_impacto = criar_sistema_impacto_direto()
    resultado_impacto = sistema_impacto.simular(0.05 * ANOS_EM_SEGUNDOS, progresso=False)
    
    print(f"Resultado: {('COLISÃO DETECTADA' if resultado_impacto.houve_colisao else 'SEM COLISÃO')}")
    if resultado_impacto.houve_colisao:
        print(f"  Tempo: {resultado_impacto.tempo_colisao/ANOS_EM_SEGUNDOS:.6f} anos")
        print(f"  Velocidade: {resultado_impacto.velocidade_impacto/1000:.2f} km/s")
        print(f"  Energia: {resultado_impacto.equivalente_tnt:.2f} megatons TNT")
    
    print(f"  Distância mínima: {resultado_impacto.distancia_minima/1000:.2f} km")
    print(f"  Distância da superfície: {resultado_impacto.distancia_superficie/1000:.2f} km")
    
    print("\n2. CENÁRIO APOPHIS (APROXIMAÇÃO PRÓXIMA):")
    print("-" * 40)
    
    # Teste 2: Apophis - aproximação próxima mas sem impacto
    sistema_apophis = criar_sistema_apophis()
    resultado_apophis = sistema_apophis.simular(2 * ANOS_EM_SEGUNDOS, progresso=False)
    
    print(f"Resultado: {('COLISÃO DETECTADA' if resultado_apophis.houve_colisao else 'SEM COLISÃO')}")
    print(f"  Aproximação perigosa: {resultado_apophis.aproximacao_perigosa}")
    print(f"  Distância mínima: {resultado_apophis.distancia_minima/1000:.2f} km")
    print(f"  Em raios terrestres: {resultado_apophis.distancia_minima/R_TERRA:.2f} R⊕")
    print(f"  Parâmetro de impacto: {resultado_apophis.parametro_impacto/1000:.2f} km")
    
    print("\n3. MELHORIAS IMPLEMENTADAS:")
    print("-" * 40)
    print("  Detecção baseada em distância de superfícies")
    print("  Raios físicos realistas dos corpos")
    print("  Critério de aproximação (velocidade radial)")
    print("  Parâmetro de impacto calculado")
    print("  Alertas de aproximação perigosa")
    print("  Cálculos melhorados de cratera")
    print("  Ângulo de impacto corrigido")
    print("  Interrupção da simulação após colisão")
    
    print("\n" + "="*70)
    
    return resultado_impacto, resultado_apophis


def exemplo_completo_colisao():
    """Exemplo completo mostrando todas as funcionalidades."""
    print("\n" + "="*70)
    print("EXEMPLO COMPLETO: ANÁLISE DE RISCO DE IMPACTO".center(70))
    print("="*70)
    
    # Criar sistema de impacto
    sistema = criar_sistema_impacto_direto()
    
    # Mostrar informações iniciais
    asteroide = sistema.get_corpo("Asteroide")
    terra = sistema.get_corpo("Terra")
    
    print(f"\nParâmetros do Asteroide:")
    print(f"  Massa: {asteroide.massa:.2e} kg ({asteroide.massa/1e9:.0f} milhões de toneladas)")
    print(f"  Raio estimado: {asteroide.raio_fisico:.0f} m")
    print(f"  Velocidade inicial: {asteroide.velocidade_escalar()/1000:.2f} km/s")
    
    distancia_inicial = asteroide.distancia_para(terra)
    print(f"  Distância inicial da Terra: {distancia_inicial/1000:.0f} km")
    print(f"  Em raios terrestres: {distancia_inicial/R_TERRA:.1f} R⊕")
    
    # Executar simulação
    print(f"\nExecutando simulação...")
    resultado = sistema.simular(0.2 * ANOS_EM_SEGUNDOS, progresso=True)
    
    # Mostrar relatório completo
    print("\n" + resultado.gerar_relatorio())
    
    # Plotar resultados se matplotlib estiver disponível
    try:
        plotar_trajetorias(sistema, "Trajetórias dos Corpos")
        plotar_distancia_tempo(sistema, "Terra", "Asteroide", "Distância Terra-Asteroide")
        
    except ImportError:
        print("Matplotlib não disponível - pulando visualização")
    
    return sistema, resultado


def teste_deteccao_colisao():
    """Testa especificamente a detecção de colisão."""
    print("\nTESTE: Detecção de Colisão Melhorada")
    print("="*70)
    
    # Criar cenário de impacto garantido
    sistema = criar_sistema_impacto_direto()
    
    # Simular por tempo curto
    resultado = sistema.simular(0.1 * ANOS_EM_SEGUNDOS, progresso=True)
    
    # Verificar detecção
    print(f"\nResultados da detecção:")
    print(f"  Colisão detectada: {resultado.houve_colisao}")
    print(f"  Aproximação perigosa: {resultado.aproximacao_perigosa}")
    print(f"  Distância mínima: {resultado.distancia_minima/1000:.2f} km")
    print(f"  Distância da superfície: {resultado.distancia_superficie/1000:.2f} km")
    
    if resultado.houve_colisao:
        print(f"  Velocidade de impacto: {resultado.velocidade_impacto/1000:.2f} km/s")
        print(f"  Energia de impacto: {resultado.energia_impacto:.2e} J")
        print(f"  Equivalente TNT: {resultado.equivalente_tnt:.2f} megatons")
        print(f"  Raio da cratera: {resultado.raio_cratera/1000:.2f} km")
    
    return resultado


def executar_cenario_interativo():
    """Executa um cenário de forma interativa."""
    print("\n" + "="*60)
    print("SIMULADOR ORBITAL INTERATIVO")
    print("="*60)
    
    # Listar cenários disponíveis
    cenarios = listar_cenarios_disponiveis()
    print("\nCenários disponíveis:")
    for i, (nome, descricao) in enumerate(cenarios.items(), 1):
        print(f"  {i}. {nome}: {descricao}")
    
    # Selecionar cenário
    try:
        escolha = int(input("\nEscolha um cenário (número): ")) - 1
        nome_cenario = list(cenarios.keys())[escolha]
    except (ValueError, IndexError):
        print("Escolha inválida, usando cenário padrão")
        nome_cenario = "impacto_direto"
    
    # Criar sistema
    print(f"\nCriando cenário: {nome_cenario}")
    sistema = criar_cenario_por_nome(nome_cenario)
    
    # Configurar simulação
    tempo_anos = float(input("Tempo de simulação (anos): ") or "0.1")
    tempo_total = tempo_anos * ANOS_EM_SEGUNDOS
    
    mostrar_progresso = input("Mostrar progresso? (s/n): ").lower().startswith('s')
    
    # Executar simulação
    print(f"\nExecutando simulação por {tempo_anos} anos...")
    resultado = sistema.simular(tempo_total, progresso=mostrar_progresso)
    
    # Mostrar resultados
    print("\n" + resultado.gerar_relatorio())
    
    # Opções adicionais
    salvar = input("\nSalvar resultados? (s/n): ").lower().startswith('s')
    if salvar:
        diretorio = salvar_simulacao(sistema, resultado)
        print(f"Resultados salvos em: {diretorio}")
    
    plotar = input("Plotar gráficos? (s/n): ").lower().startswith('s')
    if plotar:
        try:
            plotar_trajetorias(sistema)
            plotar_distancia_tempo(sistema)
        except ImportError:
            print("Matplotlib não disponível")
    
    return sistema, resultado


def main():
    """Função principal do programa."""
    parser = argparse.ArgumentParser(description='Simulador Orbital de Asteroides')
    parser.add_argument('--cenario', '-c', choices=listar_cenarios_disponiveis().keys(),
                       default='impacto_direto', help='Cenário a executar')
    parser.add_argument('--tempo', '-t', type=float, default=0.1,
                       help='Tempo de simulação em anos')
    parser.add_argument('--progresso', '-p', action='store_true',
                       help='Mostrar progresso da simulação')
    parser.add_argument('--salvar', '-s', action='store_true',
                       help='Salvar resultados')
    parser.add_argument('--plotar', action='store_true',
                       help='Plotar gráficos')
    parser.add_argument('--interativo', '-i', action='store_true',
                       help='Modo interativo')
    parser.add_argument('--demo', '-d', action='store_true',
                       help='Executar demonstração')
    parser.add_argument('--teste', action='store_true',
                       help='Executar testes')
    
    args = parser.parse_args()
    
    print("SIMULADOR ORBITAL DE ASTEROIDES v2.0")
    print("="*50)
    
    try:
        if args.interativo:
            # Modo interativo
            sistema, resultado = executar_cenario_interativo()
            
        elif args.demo:
            # Demonstração
            demonstrar_deteccao_melhorada()
            
        elif args.teste:
            # Testes
            resultado = teste_deteccao_colisao()
            
        else:
            # Modo normal
            print(f"Executando cenário: {args.cenario}")
            sistema = criar_cenario_por_nome(args.cenario)
            
            print(f"Tempo de simulação: {args.tempo} anos")
            resultado = sistema.simular(args.tempo * ANOS_EM_SEGUNDOS, 
                                      progresso=args.progresso)
            
            print("\n" + resultado.gerar_relatorio())
            
            if args.salvar:
                diretorio = salvar_simulacao(sistema, resultado)
                print(f"Resultados salvos em: {diretorio}")
            
            if args.plotar:
                try:
                    plotar_trajetorias(sistema)
                    plotar_distancia_tempo(sistema)
                except ImportError:
                    print("Matplotlib não disponível")
    
    except KeyboardInterrupt:
        print("\nSimulação interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"Erro durante a simulação: {e}")
        sys.exit(1)
    
    print("\nSimulação concluída!")


if __name__ == "__main__":
    main()
