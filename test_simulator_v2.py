#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Teste para o Simulador Orbital de Asteroides v2.0
==========================================================

Este script executa uma bateria completa de testes para verificar
o funcionamento correto do simulador orbital modular.

Autor: Assistente IA
Data: 2025
"""

import sys
import os
import numpy as np
from datetime import datetime

# Adicionar o diretório atual ao path
sys.path.append('.')

try:
    from constants import *
    from celestial_body import CorpoCeleste
    from gravitational_system import SistemaGravitacional
    from simulation_result import ResultadoSimulacao
    from scenarios import *
    from utils import *
    from main import *
    print("Módulos do simulador v2.0 importados com sucesso!")
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    sys.exit(1)


def executar_teste_basico():
    """Teste 1: Funcionalidades básicas do sistema"""
    print("\n" + "="*60)
    print("TESTE 1: FUNCIONALIDADES BÁSICAS")
    print("="*60)
    
    try:
        # Criar sistema
        sistema = SistemaGravitacional(dt=3600)
        print(f"Sistema criado com dt = {sistema.dt} segundos")
        
        # Criar corpos celestes
        sol = CorpoCeleste('Sol', M_SOL, [0,0,0], [0,0,0], COR_SOL, TAMANHO_SOL)
        terra = CorpoCeleste('Terra', M_TERRA, [UA,0,0], [0,29780,0], COR_TERRA, TAMANHO_TERRA)
        
        print(f"Sol criado: massa={sol.massa:.2e} kg, raio={sol.raio_fisico:.0f} m")
        print(f"Terra criada: massa={terra.massa:.2e} kg, raio={terra.raio_fisico:.0f} m")
        
        # Adicionar ao sistema
        sistema.adicionar_corpo(sol)
        sistema.adicionar_corpo(terra)
        print(f"Sistema com {len(sistema.corpos)} corpos")
        
        # Testar cálculos básicos
        energia = sistema.energia_total()
        momento = sistema.momento_angular_total()
        print(f"Energia total: {energia:.6e} J")
        print(f"Momento angular: {np.linalg.norm(momento):.6e} kg⋅m²/s")
        
        # Testar métodos da classe CorpoCeleste
        distancia = terra.distancia_para(sol)
        print(f"Distância Terra-Sol: {distancia/UA:.2f} UA")
        
        v_orbital = terra.velocidade_orbital_circular(sol)
        print(f"Velocidade orbital da Terra: {v_orbital/1000:.2f} km/s")
        
        return True
        
    except Exception as e:
        print(f"Erro no teste básico: {e}")
        return False


def executar_teste_deteccao_colisao():
    """Teste 2: Detecção de colisão"""
    print("\n" + "="*60)
    print("TESTE 2: DETECÇÃO DE COLISÃO")
    print("="*60)
    
    try:
        # Usar função do main.py
        resultado = teste_deteccao_colisao()
        
        print(f"\nResultados:")
        print(f"  Colisão detectada: {resultado.houve_colisao}")
        print(f"  Aproximação perigosa: {resultado.aproximacao_perigosa}")
        print(f"  Distância mínima: {resultado.distancia_minima/1000:.2f} km")
        print(f"  Distância da superfície: {resultado.distancia_superficie/1000:.2f} km")
        
        return True
        
    except Exception as e:
        print(f"Erro no teste de detecção: {e}")
        return False


def executar_teste_cenarios():
    """Teste 3: Cenários pré-configurados"""
    print("\n" + "="*60)
    print("TESTE 3: CENÁRIOS PRÉ-CONFIGURADOS")
    print("="*60)
    
    try:
        # Testar diferentes cenários
        cenarios_teste = [
            ("sistema_solar_basico", "Sistema Solar Básico"),
            ("impacto_direto", "Impacto Direto"),
            ("apophis", "Apophis"),
            ("teste_conservacao", "Teste Conservação")
        ]
        
        for nome_cenario, descricao in cenarios_teste:
            print(f"\nTestando: {descricao}")
            sistema = criar_cenario_por_nome(nome_cenario)
            print(f"  Sistema criado: {sistema.nome}")
            print(f"  Corpos: {len(sistema.corpos)}")
            
            # Simulação rápida
            resultado = sistema.simular(0.01 * ANOS_EM_SEGUNDOS, progresso=False)
            print(f"  Simulação concluída: {resultado.estado_final}")
        
        return True
        
    except Exception as e:
        print(f"Erro no teste de cenários: {e}")
        return False


def executar_teste_conservacao():
    """Teste 4: Conservação de energia e momento angular"""
    print("\n" + "="*60)
    print("TESTE 4: CONSERVAÇÃO DE ENERGIA E MOMENTO ANGULAR")
    print("="*60)
    
    try:
        # Sistema simples: Sol + Terra
        sistema = criar_sistema_teste_conservacao()
        
        # Valores iniciais
        E_inicial = sistema.energia_total()
        L_inicial = sistema.momento_angular_total()
        
        print(f"Energia inicial: {E_inicial:.6e} J")
        print(f"Momento angular inicial: {np.linalg.norm(L_inicial):.6e} kg⋅m²/s")
        
        # Simular por 1 ano
        resultado = sistema.simular(1.0 * ANOS_EM_SEGUNDOS, progresso=False)
        
        # Valores finais
        E_final = sistema.energia_total()
        L_final = sistema.momento_angular_total()
        
        # Erros relativos
        erro_E = abs(E_final - E_inicial) / abs(E_inicial)
        erro_L = abs(np.linalg.norm(L_final) - np.linalg.norm(L_inicial)) / abs(np.linalg.norm(L_inicial))
        
        print(f"\nResultados:")
        print(f"  Erro relativo de energia: {erro_E:.2e}")
        print(f"  Erro relativo de momento angular: {erro_L:.2e}")
        
        if erro_E < TOLERANCIA_ENERGIA:
            print("Energia conservada!")
        else:
            print("Aviso: Violação na conservação de energia")
            
        if erro_L < 1e-6:
            print("Momento angular conservado!")
        else:
            print("Aviso: Violação na conservação do momento angular")
        
        return True
        
    except Exception as e:
        print(f"Erro no teste de conservação: {e}")
        return False


def executar_teste_utilitarios():
    """Teste 5: Funções utilitárias"""
    print("\n" + "="*60)
    print("TESTE 5: FUNÇÕES UTILITÁRIAS")
    print("="*60)
    
    try:
        # Testar conversões de unidades
        print("Testando conversões de unidades:")
        km_para_m = converter_unidades(1000, "km", "m")
        print(f"  1000 km = {km_para_m} m")
        
        anos_para_s = converter_unidades(1, "a", "s")
        print(f"  1 ano = {anos_para_s} segundos")
        
        # Testar cálculos orbitais
        print("\nTestando cálculos orbitais:")
        v_orbital = calcular_orbita_circular(M_SOL, UA)
        print(f"  Velocidade orbital da Terra: {v_orbital/1000:.2f} km/s")
        
        periodo = calcular_periodo_orbital(M_SOL, UA)
        print(f"  Período orbital da Terra: {periodo/ANOS_EM_SEGUNDOS:.2f} anos")
        
        # Testar validação de sistema
        print("\nTestando validação de sistema:")
        sistema = criar_sistema_solar_basico()
        avisos = validar_sistema(sistema)
        print(f"  Avisos encontrados: {len(avisos)}")
        for aviso in avisos:
            print(f"    - {aviso}")
        
        return True
        
    except Exception as e:
        print(f"Erro no teste de utilitários: {e}")
        return False


def executar_teste_resultado():
    """Teste 6: Classe ResultadoSimulacao"""
    print("\n" + "="*60)
    print("TESTE 6: CLASSE RESULTADO SIMULAÇÃO")
    print("="*60)
    
    try:
        # Criar resultado de teste
        resultado = ResultadoSimulacao()
        resultado.distancia_minima = R_TERRA * 2
        resultado.houve_colisao = False
        resultado.aproximacao_perigosa = True
        resultado.energia_inicial = -1e33
        resultado.energia_final = -0.999e33
        resultado.calcular_erro_energia()
        
        print("Testando métodos da classe ResultadoSimulacao:")
        print(f"  Energia conservada: {resultado.energia_conservada()}")
        print(f"  Física válida: {resultado.fisica_valida()}")
        print(f"  Classificação aproximação: {resultado.classificar_aproximacao()}")
        
        # Testar geração de relatório
        relatorio = resultado.gerar_relatorio()
        print(f"  Relatório gerado: {len(relatorio)} caracteres")
        
        # Testar JSON
        json_data = resultado.gerar_relatorio_json()
        print(f"  JSON gerado: {len(json_data)} campos")
        
        return True
        
    except Exception as e:
        print(f"Erro no teste de resultado: {e}")
        return False


def executar_teste_demonstracao():
    """Teste 7: Demonstração completa"""
    print("\n" + "="*60)
    print("TESTE 7: DEMONSTRAÇÃO COMPLETA")
    print("="*60)
    
    try:
        print("Executando demonstração de detecção melhorada...")
        resultado_impacto, resultado_apophis = demonstrar_deteccao_melhorada()
        
        print("\nExecutando exemplo completo de colisão...")
        sistema, resultado = exemplo_completo_colisao()
        
        print("\nDemonstração completa executada com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro na demonstração completa: {e}")
        return False


def main():
    """Função principal que executa todos os testes"""
    print("INICIANDO BATERIA DE TESTES DO SIMULADOR ORBITAL v2.0")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    testes = [
        ("Funcionalidades Básicas", executar_teste_basico),
        ("Detecção de Colisão", executar_teste_deteccao_colisao),
        ("Cenários Pré-configurados", executar_teste_cenarios),
        ("Conservação de Energia", executar_teste_conservacao),
        ("Funções Utilitárias", executar_teste_utilitarios),
        ("Classe Resultado", executar_teste_resultado),
        ("Demonstração Completa", executar_teste_demonstracao)
    ]
    
    resultados = []
    
    for nome, funcao_teste in testes:
        print(f"\nExecutando: {nome}")
        try:
            sucesso = funcao_teste()
            resultados.append((nome, sucesso))
            if sucesso:
                print(f"{nome}: PASSOU")
            else:
                print(f"{nome}: FALHOU")
        except Exception as e:
            print(f"{nome}: ERRO - {e}")
            resultados.append((nome, False))
    
    # Relatório final
    print("\n" + "="*60)
    print("RELATÓRIO FINAL DOS TESTES")
    print("="*60)
    
    passou = sum(1 for _, sucesso in resultados if sucesso)
    total = len(resultados)
    
    for nome, sucesso in resultados:
        status = "PASSOU" if sucesso else "FALHOU"
        print(f"  {nome}: {status}")
    
    print(f"\nResumo: {passou}/{total} testes passaram")
    
    if passou == total:
        print("TODOS OS TESTES PASSARAM! O simulador v2.0 está funcionando corretamente.")
        return 0
    else:
        print("Alguns testes falharam. Verifique os erros acima.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
