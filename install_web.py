#!/usr/bin/env python3
# ==============================================================================
# SCRIPT DE INSTALAÇÃO PARA INTERFACE WEB DO SIMULADOR ORBITAL
# ==============================================================================

import subprocess
import sys
import importlib
import pkg_resources

def verificar_pacote(pacote, versao_minima=None):
    """Verifica se um pacote está instalado e se atende à versão mínima."""
    try:
        if versao_minima:
            pkg_resources.require(f"{pacote}>={versao_minima}")
        else:
            importlib.import_module(pacote)
        return True
    except (ImportError, pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
        return False

def instalar_pacote(pacote, versao=None):
    """Instala um pacote usando pip."""
    try:
        if versao:
            subprocess.check_call([sys.executable, "-m", "pip", "install", f"{pacote}=={versao}"])
        else:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🌌 Instalando Interface Web do Simulador Orbital")
    print("=" * 60)
    
    # Lista de dependências essenciais
    dependencias = {
        'flask': '2.0.0',
        'werkzeug': '2.0.0',
        'python-dateutil': None,
        'pytz': None,
        'python-dotenv': None
    }
    
    # Verificar dependências já instaladas
    print("\n📋 Verificando dependências...")
    
    dependencias_faltando = []
    for pacote, versao_minima in dependencias.items():
        if verificar_pacote(pacote, versao_minima):
            print(f"✅ {pacote} - OK")
        else:
            print(f"❌ {pacote} - Faltando")
            dependencias_faltando.append((pacote, versao_minima))
    
    # Verificar dependências do simulador
    print("\n🔬 Verificando dependências do simulador...")
    
    simulador_deps = ['numpy', 'scipy', 'matplotlib', 'pandas']
    simulador_ok = True
    
    for dep in simulador_deps:
        if verificar_pacote(dep):
            print(f"✅ {dep} - OK")
        else:
            print(f"❌ {dep} - Faltando")
            simulador_ok = False
    
    if not simulador_ok:
        print("\n⚠️  ATENÇÃO: Algumas dependências do simulador estão faltando!")
        print("   A interface web pode não funcionar corretamente.")
        print("   Instale as dependências do simulador primeiro:")
        print("   pip install numpy scipy matplotlib pandas")
    
    # Instalar dependências faltando
    if dependencias_faltando:
        print(f"\n📦 Instalando {len(dependencias_faltando)} dependências...")
        
        for pacote, versao in dependencias_faltando:
            print(f"   Instalando {pacote}...")
            if instalar_pacote(pacote, versao):
                print(f"   ✅ {pacote} instalado com sucesso")
            else:
                print(f"   ❌ Erro ao instalar {pacote}")
                return False
    else:
        print("\n✅ Todas as dependências já estão instaladas!")
    
    # Verificar se os arquivos do simulador existem
    print("\n📁 Verificando arquivos do simulador...")
    
    arquivos_necessarios = [
        'asteroid_simulator_fixed.py',
        'config.py',
        'constants.py'
    ]
    
    arquivos_ok = True
    for arquivo in arquivos_necessarios:
        try:
            with open(arquivo, 'r'):
                print(f"✅ {arquivo} - OK")
        except FileNotFoundError:
            print(f"❌ {arquivo} - Não encontrado")
            arquivos_ok = False
    
    if not arquivos_ok:
        print("\n⚠️  ATENÇÃO: Alguns arquivos do simulador estão faltando!")
        print("   Certifique-se de que todos os arquivos estão no mesmo diretório.")
        return False
    
    # Teste final
    print("\n🧪 Testando importações...")
    
    try:
        import flask
        print("✅ Flask importado com sucesso")
        
        # Testar importação do simulador
        try:
            from asteroid_simulator_fixed import SistemaGravitacional
            print("✅ Simulador importado com sucesso")
        except ImportError as e:
            print(f"❌ Erro ao importar simulador: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ Erro ao importar Flask: {e}")
        return False
    
    print("\n🎉 Instalação concluída com sucesso!")
    print("\n📖 Para executar a interface web:")
    print("   python app.py")
    print("\n🌐 Acesse: http://localhost:5000")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
