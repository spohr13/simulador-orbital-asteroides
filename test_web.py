#!/usr/bin/env python3
# ==============================================================================
# TESTE SIMPLES DA INTERFACE WEB
# ==============================================================================

import requests
import json

def testar_interface():
    """Testa se a interface web está funcionando corretamente."""
    
    base_url = "http://localhost:5001"
    
    print("🧪 Testando Interface Web do Simulador Orbital")
    print("=" * 50)
    
    # Teste 1: Página principal
    print("\n1. Testando página principal...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("   ✅ Página principal carregada")
        else:
            print(f"   ❌ Erro na página principal: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro de conexão: {e}")
        return False
    
    # Teste 2: Página do simulador
    print("\n2. Testando página do simulador...")
    try:
        response = requests.get(f"{base_url}/simulador")
        if response.status_code == 200:
            print("   ✅ Página do simulador carregada")
        else:
            print(f"   ❌ Erro na página do simulador: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro de conexão: {e}")
        return False
    
    # Teste 3: API de configurações
    print("\n3. Testando API de configurações...")
    try:
        response = requests.get(f"{base_url}/api/configuracoes")
        if response.status_code == 200:
            data = response.json()
            print("   ✅ API de configurações funcionando")
            print(f"   📊 Cenários disponíveis: {len(data.get('cenarios', {}))}")
        else:
            print(f"   ❌ Erro na API de configurações: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro na API: {e}")
        return False
    
    # Teste 4: Simulação simples
    print("\n4. Testando simulação...")
    try:
        dados_simulacao = {
            "cenario": "apophis",
            "tempo_total": 0.01,
            "dt": 3600
        }
        
        response = requests.post(
            f"{base_url}/api/simular",
            headers={"Content-Type": "application/json"},
            data=json.dumps(dados_simulacao)
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'sucesso':
                print("   ✅ Simulação executada com sucesso")
                print(f"   📊 Distância mínima: {data['resultado']['distancia_minima']/1000:.2f} km")
                print(f"   🎯 Colisão: {'Sim' if data['resultado']['houve_colisao'] else 'Não'}")
            else:
                print(f"   ❌ Erro na simulação: {data.get('mensagem', 'Erro desconhecido')}")
                return False
        else:
            print(f"   ❌ Erro HTTP na simulação: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro na simulação: {e}")
        return False
    
    # Teste 5: Lista de simulações
    print("\n5. Testando lista de simulações...")
    try:
        response = requests.get(f"{base_url}/api/lista_simulacoes")
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Lista de simulações funcionando")
            print(f"   📊 Simulações realizadas: {len(data.get('simulacoes', []))}")
        else:
            print(f"   ❌ Erro na lista de simulações: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro na lista: {e}")
        return False
    
    print("\n🎉 Todos os testes passaram! Interface web funcionando perfeitamente!")
    print(f"\n🌐 Acesse: {base_url}")
    print("📖 Para parar o servidor: Ctrl+C no terminal")
    
    return True

if __name__ == "__main__":
    testar_interface()
