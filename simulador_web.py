#!/usr/bin/env python3
# ==============================================================================
# SIMULADOR ORBITAL - INTERFACE WEB COMPLETA
# ==============================================================================

import subprocess
import sys
import webbrowser
import requests
import time
import socket

def verificar_servidor_rodando(porta=5001):
    """Verifica se o servidor Flask está rodando."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            resultado = s.connect_ex(('localhost', porta))
            return resultado == 0
    except Exception:
        return False

def obter_ip_local():
    """Obtém o IP local da máquina."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip_local = s.getsockname()[0]
        return ip_local
    except Exception:
        return "127.0.0.1"

def obter_url_ngrok():
    """Obtém a URL pública do ngrok se estiver rodando."""
    try:
        response = requests.get("http://localhost:4040/api/tunnels", timeout=2)
        if response.status_code == 200:
            data = response.json()
            if data.get('tunnels'):
                return data['tunnels'][0]['public_url']
    except Exception:
        pass
    return None

def iniciar_servidor():
    """Inicia o servidor Flask."""
    print("🚀 Iniciando servidor Flask...")
    try:
        subprocess.Popen([sys.executable, "app.py"], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
        print("⏳ Aguardando servidor inicializar...")
        time.sleep(3)
        return True
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        return False

def iniciar_ngrok():
    """Inicia ngrok para acesso público."""
    print("🌍 Iniciando ngrok...")
    try:
        subprocess.Popen(["ngrok", "http", "5001"], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
        print("⏳ Aguardando ngrok inicializar...")
        time.sleep(5)
        return True
    except FileNotFoundError:
        print("❌ ngrok não encontrado!")
        print("📥 Instale: brew install ngrok/ngrok/ngrok")
        return False
    except Exception as e:
        print(f"❌ Erro ao iniciar ngrok: {e}")
        return False

def mostrar_status():
    """Mostra o status atual do simulador."""
    print("🌌 SIMULADOR ORBITAL - STATUS")
    print("=" * 40)
    
    # Verificar servidor
    if verificar_servidor_rodando():
        print("✅ Servidor Flask: RODANDO")
        ip_local = obter_ip_local()
        print(f"🌐 URL Local: http://{ip_local}:5001")
    else:
        print("❌ Servidor Flask: PARADO")
        return False
    
    # Verificar ngrok
    url_ngrok = obter_url_ngrok()
    if url_ngrok:
        print("✅ ngrok: RODANDO")
        print(f"🌍 URL Pública: {url_ngrok}")
    else:
        print("⚠️  ngrok: NÃO RODANDO")
    
    print()
    return True

def main():
    """Função principal."""
    print("🌌 Simulador Orbital de Asteroides")
    print("=" * 40)
    print()
    
    # Verificar se servidor está rodando
    if not verificar_servidor_rodando():
        print("⚠️  Servidor não está rodando!")
        resposta = input("Deseja iniciar o servidor? (s/n): ").lower()
        if resposta == 's':
            if not iniciar_servidor():
                return
        else:
            print("❌ Servidor necessário para continuar")
            return
    
    # Mostrar status
    if not mostrar_status():
        return
    
    # Verificar ngrok
    url_ngrok = obter_url_ngrok()
    if not url_ngrok:
        print("🌍 Para acesso via internet:")
        print("1. Execute: ngrok http 5001")
        print("2. Use a URL fornecida")
        print()
    
    # Mostrar opções
    print("📋 OPÇÕES:")
    print("1. Abrir no navegador (local)")
    print("2. Iniciar ngrok (internet)")
    print("3. Mostrar URLs para compartilhar")
    print("4. Sair")
    
    try:
        opcao = input("\nEscolha uma opção (1-4): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n👋 Até logo!")
        return
    
    if opcao == "1":
        # Abrir local
        ip_local = obter_ip_local()
        url_local = f"http://{ip_local}:5001"
        print(f"🌐 Abrindo {url_local}...")
        webbrowser.open(url_local)
        
    elif opcao == "2":
        # Iniciar ngrok
        if iniciar_ngrok():
            time.sleep(3)
            url_ngrok = obter_url_ngrok()
            if url_ngrok:
                print(f"🎉 ngrok iniciado!")
                print(f"🌍 URL Pública: {url_ngrok}")
                print("📱 Compartilhe esta URL com qualquer pessoa!")
                
                resposta = input("Deseja abrir no navegador? (s/n): ").lower()
                if resposta == 's':
                    webbrowser.open(url_ngrok)
            else:
                print("⚠️  ngrok iniciado, mas URL não disponível")
                print("🌐 Acesse: http://localhost:4040 para ver a URL")
    
    elif opcao == "3":
        # Mostrar URLs
        ip_local = obter_ip_local()
        url_local = f"http://{ip_local}:5001"
        
        print("\n📱 URLs PARA COMPARTILHAR:")
        print("=" * 30)
        print(f"🌐 Local (mesma WiFi): {url_local}")
        
        url_ngrok = obter_url_ngrok()
        if url_ngrok:
            print(f"🌍 Internet (qualquer lugar): {url_ngrok}")
        else:
            print("🌍 Internet: Execute 'ngrok http 5001' primeiro")
        
        print("\n📋 MENSAGEM PARA COMPARTILHAR:")
        print("=" * 40)
        print("🌌 Simulador Orbital de Asteroides")
        print(f"🔗 {url_local}")
        if url_ngrok:
            print(f"🌍 {url_ngrok}")
        print("\n✨ Funcionalidades:")
        print("  - 3 cenários de simulação")
        print("  - Parâmetros configuráveis")
        print("  - Gráficos interativos")
        print("  - Relatórios detalhados")
    
    elif opcao == "4":
        print("👋 Até logo!")
    
    else:
        print("❌ Opção inválida!")

if __name__ == "__main__":
    main()
