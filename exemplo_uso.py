#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXEMPLO DE USO DO SIMULADOR ORBITAL v2.0
========================================

Este arquivo demonstra como usar o simulador orbital modular
para diferentes tipos de análises e simulações.

Autor: Assistente IA
Data: 2025
"""

import numpy as np
from constants import *
from celestial_body import CorpoCeleste
from gravitational_system import SistemaGravitacional
from scenarios import *
from utils import *


def exemplo_basico():
    """Exemplo 1: Uso básico do simulador"""
    print("\n" + "="*60)
    print("EXEMPLO 1: USO BÁSICO")
    print("="*60)
    
    # Criar sistema simples
    sistema = SistemaGravitacional(dt=3600, nome="Exemplo Básico")
    
    # Adicionar Sol
    sol = CorpoCeleste("Sol", M_SOL, [0,0,0], [0,0,0], COR_SOL, TAMANHO_SOL)
    sistema.adicionar_corpo(sol)
    
    # Adicionar Terra
    terra = CorpoCeleste("Terra", M_TERRA, [UA,0,0], [0,29780,0], COR_TERRA, TAMANHO_TERRA)
    sistema.adicionar_corpo(terra)
    
    # Simular por 1 ano
    print("Simulando por 1 ano...")
    resultado = sistema.simular(1.0 * ANOS_EM_SEGUNDOS, progresso=True)
    
    # Mostrar resultados
    print(f"\nResultados:")
    print(f"  Energia conservada: {resultado.energia_conservada()}")
    print(f"  Física válida: {resultado.fisica_valida()}")
    print(f"  Tempo simulado: {resultado.tempo_simulacao/ANOS_EM_SEGUNDOS:.2f} anos")


def exemplo_cenarios():
    """Exemplo 2: Usando cenários pré-configurados"""
    print("\n" + "="*60)
    print("EXEMPLO 2: CENÁRIOS PRÉ-CONFIGURADOS")
    print("="*60)
    
    # Listar cenários disponíveis
    cenarios = listar_cenarios_disponiveis()
    print("Cenários disponíveis:")
    for nome, descricao in cenarios.items():
        print(f"  - {nome}: {descricao}")
    
    # Testar diferentes cenários
    cenarios_teste = ["sistema_solar_basico", "impacto_direto", "apophis"]
    
    for nome in cenarios_teste:
        print(f"\nTestando cenário: {nome}")
        sistema = criar_cenario_por_nome(nome)
        print(f"  Sistema: {sistema.nome}")
        print(f"  Corpos: {len(sistema.corpos)}")
        
        # Simulação rápida
        resultado = sistema.simular(0.01 * ANOS_EM_SEGUNDOS, progresso=False)
        print(f"  Estado: {resultado.estado_final}")


def exemplo_asteroide_personalizado():
    """Exemplo 3: Asteroide personalizado"""
    print("\n" + "="*60)
    print("EXEMPLO 3: ASTEROIDE PERSONALIZADO")
    print("="*60)
    
    # Parâmetros do asteroide
    massa = 5e10  # 50 milhões de toneladas
    posicao = np.array([UA * 1.2, UA * 0.1, 0])  # 1.2 UA do Sol
    velocidade = np.array([-15000, 25000, 0])  # Velocidade personalizada
    
    # Criar sistema
    sistema = criar_sistema_asteroide_personalizado(
        massa_asteroide=massa,
        posicao_inicial=posicao,
        velocidade_inicial=velocidade,
        nome_asteroide="Meu Asteroide",
        densidade=2500  # kg/m³
    )
    
    print(f"Sistema criado: {sistema.nome}")
    
    # Analisar asteroide
    asteroide = sistema.get_corpo("Meu Asteroide")
    print(f"Asteroide: {asteroide.nome}")
    print(f"  Massa: {asteroide.massa/1e9:.1f} milhões de toneladas")
    print(f"  Raio: {asteroide.raio_fisico:.0f} m")
    print(f"  Densidade: {asteroide.densidade:.0f} kg/m³")
    print(f"  Velocidade: {asteroide.velocidade_escalar()/1000:.2f} km/s")
    
    # Simular
    print("\nSimulando...")
    resultado = sistema.simular(0.1 * ANOS_EM_SEGUNDOS, progresso=True)
    
    # Análise de resultados
    print(f"\nAnálise:")
    print(f"  Aproximação: {resultado.classificar_aproximacao()}")
    print(f"  Distância mínima: {resultado.distancia_minima/1000:.2f} km")
    print(f"  Em raios terrestres: {resultado.distancia_minima/R_TERRA:.2f} R⊕")


def exemplo_analise_detalhada():
    """Exemplo 4: Análise detalhada de resultados"""
    print("\n" + "="*60)
    print("EXEMPLO 4: ANÁLISE DETALHADA")
    print("="*60)
    
    # Criar sistema de impacto
    sistema = criar_sistema_impacto_direto(
        massa_asteroide=1e11,  # 100 milhões de toneladas
        distancia_inicial=R_TERRA * 15,  # 15 raios terrestres
        velocidade_aproximacao=25000  # 25 km/s
    )
    
    # Simular
    print("Executando simulação de impacto...")
    resultado = sistema.simular(0.05 * ANOS_EM_SEGUNDOS, progresso=True)
    
    # Análise detalhada
    print(f"\n{'='*50}")
    print("ANÁLISE DETALHADA DOS RESULTADOS")
    print(f"{'='*50}")
    
    # Informações gerais
    print(f"\nInformações Gerais:")
    print(f"  Tempo simulado: {resultado.tempo_simulacao/ANOS_EM_SEGUNDOS:.4f} anos")
    print(f"  Número de passos: {resultado.numero_passos:,}")
    print(f"  Estado final: {resultado.estado_final}")
    
    # Aproximação
    print(f"\nAproximação:")
    print(f"  Distância mínima: {resultado.distancia_minima/1000:.2f} km")
    print(f"  Distância da superfície: {resultado.distancia_superficie/1000:.2f} km")
    print(f"  Em raios terrestres: {resultado.distancia_minima/R_TERRA:.2f} R⊕")
    print(f"  Classificação: {resultado.classificar_aproximacao()}")
    
    # Eventos especiais
    if resultado.aproximacao_perigosa:
        print(f"\nAproximação Perigosa:")
        print(f"  Tempo: {resultado.tempo_aproximacao_perigosa/ANOS_EM_SEGUNDOS:.6f} anos")
    
    if resultado.houve_colisao:
        print(f"\nColisão Detectada:")
        print(f"  Tempo: {resultado.tempo_colisao/ANOS_EM_SEGUNDOS:.6f} anos")
        print(f"  Velocidade: {resultado.velocidade_impacto/1000:.2f} km/s")
        print(f"  Energia: {resultado.equivalente_tnt:.2f} megatons TNT")
        print(f"  Classificação: {resultado.classificar_impacto()}")
        
        if resultado.raio_cratera > 0:
            print(f"  Cratera:")
            print(f"    Diâmetro: {resultado.diametro_cratera/1000:.2f} km")
            print(f"    Raio: {resultado.raio_cratera/1000:.2f} km")
            print(f"    Profundidade: {resultado.profundidade_cratera/1000:.2f} km")
    
    # Validação física
    print(f"\nValidação Física:")
    print(f"  Energia conservada: {resultado.energia_conservada()}")
    print(f"  Momento angular conservado: {resultado.momento_angular_conservado()}")
    print(f"  Física válida: {resultado.fisica_valida()}")
    print(f"  Erro de energia: {resultado.erro_energia_relativo:.2e}")
    print(f"  Erro de momento: {resultado.erro_momento_relativo:.2e}")


def exemplo_visualizacao():
    """Exemplo 5: Visualização e gráficos"""
    print("\n" + "="*60)
    print("EXEMPLO 5: VISUALIZAÇÃO")
    print("="*60)
    
    # Criar sistema
    sistema = criar_sistema_apophis()
    
    # Simular
    print("Simulando sistema Apophis...")
    resultado = sistema.simular(0.5 * ANOS_EM_SEGUNDOS, progresso=True)
    
    # Gerar visualizações
    print("\nGerando visualizações...")
    try:
        # Trajetórias
        plotar_trajetorias(sistema, "Trajetórias - Sistema Apophis", 
                          salvar=True, arquivo="exemplo_trajetorias.png")
        
        # Distância vs tempo
        plotar_distancia_tempo(sistema, "Terra", "Apophis", 
                              "Distância Terra-Apophis", 
                              salvar=True, arquivo="exemplo_distancia.png")
        
        # Energia vs tempo
        plotar_energia_tempo(sistema, salvar=True, arquivo="exemplo_energia.png")
        
        print("Gráficos salvos com sucesso!")
        
    except ImportError:
        print("Matplotlib não disponível - pulando visualização")


def exemplo_salvamento():
    """Exemplo 6: Salvamento e carregamento"""
    print("\n" + "="*60)
    print("EXEMPLO 6: SALVAMENTO E CARREGAMENTO")
    print("="*60)
    
    # Criar sistema
    sistema = criar_sistema_solar_basico()
    
    # Simular
    print("Simulando sistema solar básico...")
    resultado = sistema.simular(0.1 * ANOS_EM_SEGUNDOS, progresso=True)
    
    # Salvar simulação
    print("\nSalvando simulação...")
    diretorio = salvar_simulacao(sistema, resultado, "exemplos")
    print(f"Simulação salva em: {diretorio}")
    
    # Gerar relatório completo
    print("\nGerando relatório completo...")
    relatorio = gerar_relatorio_completo(sistema, resultado, salvar=True, arquivo="exemplo")
    print("Relatório completo gerado!")


def exemplo_comparacao():
    """Exemplo 7: Comparação de simulações"""
    print("\n" + "="*60)
    print("EXEMPLO 7: COMPARAÇÃO DE SIMULAÇÕES")
    print("="*60)
    
    # Diferentes massas de asteroide
    massas = [1e10, 5e10, 1e11, 5e11]  # kg
    resultados = []
    nomes = []
    
    for i, massa in enumerate(massas):
        print(f"\nSimulando asteroide {i+1}/4 (massa: {massa/1e9:.0f} Mt)...")
        
        # Criar sistema personalizado
        sistema = criar_sistema_asteroide_personalizado(
            massa_asteroide=massa,
            posicao_inicial=np.array([UA * 1.1, 0, 0]),
            velocidade_inicial=np.array([-20000, 25000, 0]),
            nome_asteroide=f"Asteroide_{i+1}"
        )
        
        # Simular
        resultado = sistema.simular(0.05 * ANOS_EM_SEGUNDOS, progresso=False)
        resultados.append(resultado)
        nomes.append(f"{massa/1e9:.0f} Mt")
    
    # Comparar resultados
    print(f"\nComparação de resultados:")
    print(f"{'Massa (Mt)':<12} {'Dist. Mín (km)':<15} {'Colisão':<8} {'Energia (Mt TNT)':<15}")
    print("-" * 60)
    
    for i, (resultado, nome) in enumerate(zip(resultados, nomes)):
        energia = resultado.equivalente_tnt if resultado.houve_colisao else 0
        colisao = "Sim" if resultado.houve_colisao else "Não"
        print(f"{nome:<12} {resultado.distancia_minima/1000:<15.2f} {colisao:<8} {energia:<15.2f}")
    
    # Gráfico de comparação
    try:
        comparar_simulacoes(resultados, nomes)
        print("Gráfico de comparação gerado!")
    except ImportError:
        print("Matplotlib não disponível - pulando gráfico de comparação")


def main():
    """Executa todos os exemplos"""
    print("EXEMPLOS DE USO DO SIMULADOR ORBITAL v2.0")
    print("="*60)
    
    exemplos = [
        ("Uso Básico", exemplo_basico),
        ("Cenários Pré-configurados", exemplo_cenarios),
        ("Asteroide Personalizado", exemplo_asteroide_personalizado),
        ("Análise Detalhada", exemplo_analise_detalhada),
        ("Visualização", exemplo_visualizacao),
        ("Salvamento e Carregamento", exemplo_salvamento),
        ("Comparação de Simulações", exemplo_comparacao)
    ]
    
    for nome, funcao in exemplos:
        try:
            print(f"\n{'='*60}")
            print(f"EXECUTANDO: {nome}")
            print(f"{'='*60}")
            funcao()
            print(f"\n{nome} concluído com sucesso!")
        except Exception as e:
            print(f"\nErro em {nome}: {e}")
    
    print(f"\n{'='*60}")
    print("TODOS OS EXEMPLOS CONCLUÍDOS!")
    print("="*60)


if __name__ == "__main__":
    main()
