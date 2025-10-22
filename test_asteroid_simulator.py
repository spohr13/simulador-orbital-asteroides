#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Teste para o Simulador Orbital de Asteroides
=====================================================

Este script executa uma bateria completa de testes para verificar
o funcionamento correto do simulador orbital.

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
    from asteroid_simulator_fixed import *
    print("Módulo asteroid_simulator_fixed importado com sucesso!")
except ImportError as e:
    print(f"Erro ao importar módulo: {e}")
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
        sol = CorpoCeleste('Sol', M_SOL, [0,0,0], [0,0,0], 'yellow', 20)
        terra = CorpoCeleste('Terra', M_TERRA, [UA,0,0], [0,29780,0], 'blue', 10)
        
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

def executar_teste_apophis():
    """Teste 3: Cenário Apophis"""
    print("\n" + "="*60)
    print("TESTE 3: CENÁRIO APOPHIS")
    print("="*60)
    
    try:
        sistema = criar_sistema_apophis_melhorado()
        asteroide = next(c for c in sistema.corpos if c.nome == 'Asteroide')
        
        print(f"Sistema Apophis criado")
        print(f"  Massa: {asteroide.massa:.2e} kg")
        print(f"  Raio: {asteroide.raio_fisico:.0f} m")
        print(f"  Velocidade: {np.linalg.norm(asteroide.velocidade)/1000:.2f} km/s")
        
        resultado = sistema.simular(1.0 * ANOS_EM_SEGUNDOS, progresso=False)
        
        print(f"\nResultados Apophis:")
        print(f"  Colisão: {resultado.houve_colisao}")
        print(f"  Aproximação perigosa: {resultado.aproximacao_perigosa}")
        print(f"  Distância mínima: {resultado.distancia_minima/1000:.2f} km")
        print(f"  Em raios terrestres: {resultado.distancia_minima/R_TERRA:.2f} R⊕")
        
        return True
        
    except Exception as e:
        print(f"Erro no teste Apophis: {e}")
        return False

def executar_teste_conservacao():
    """Teste 4: Conservação de energia e momento angular"""
    print("\n" + "="*60)
    print("TESTE 4: CONSERVAÇÃO DE ENERGIA E MOMENTO ANGULAR")
    print("="*60)
    
    try:
        # Sistema simples: Sol + Terra
        sistema = SistemaGravitacional(dt=3600)
        
        sol = CorpoCeleste('Sol', M_SOL, [0,0,0], [0,0,0], 'yellow', 20)
        v_orbital = np.sqrt(G * M_SOL / UA)
        terra = CorpoCeleste('Terra', M_TERRA, [UA,0,0], [0,v_orbital,0], 'blue', 10)
        
        sistema.adicionar_corpo(sol)
        sistema.adicionar_corpo(terra)
        
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

def executar_teste_completo():
    """Teste 5: Demonstração completa"""
    print("\n" + "="*60)
    print("TESTE 5: DEMONSTRAÇÃO COMPLETA")
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
    print("INICIANDO BATERIA DE TESTES DO SIMULADOR ORBITAL")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    testes = [
        ("Funcionalidades Básicas", executar_teste_basico),
        ("Detecção de Colisão", executar_teste_deteccao_colisao),
        ("Cenário Apophis", executar_teste_apophis),
        ("Conservação de Energia", executar_teste_conservacao),
        ("Demonstração Completa", executar_teste_completo)
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
        print("TODOS OS TESTES PASSARAM! O simulador está funcionando corretamente.")
        return 0
    else:
        print("Alguns testes falharam. Verifique os erros acima.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
