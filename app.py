# ==============================================================================
# INTERFACE WEB PARA SIMULADOR ORBITAL DE ASTEROIDES
# ==============================================================================

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import numpy as np
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Usar backend não-interativo
import matplotlib.pyplot as plt
import io
import base64

# Importar módulos do simulador
from asteroid_simulator_fixed import (
    SistemaGravitacional, CorpoCeleste, ResultadoSimulacao,
    criar_sistema_impacto_melhorado, criar_sistema_apophis_melhorado,
    M_SOL, M_TERRA, R_TERRA, UA, ANOS_EM_SEGUNDOS
)
from config import obter_config_padrao, ConfigSimulacao, ConfigCenarios
from constants import *

app = Flask(__name__)
app.secret_key = 'simulador_orbital_2025'

# Configurações globais
SIMULACOES_ATIVAS = {}
RESULTADOS_RECENTES = {}

@app.route('/')
def index():
    """Página principal da interface."""
    return render_template('index.html')

@app.route('/simulador')
def simulador():
    """Página do simulador interativo."""
    return render_template('simulador.html')

@app.route('/resultados')
def resultados():
    """Página de visualização de resultados."""
    return render_template('resultados.html')

@app.route('/api/configuracoes', methods=['GET'])
def obter_configuracoes():
    """Retorna configurações disponíveis."""
    config = obter_config_padrao()
    
    # Adicionar opções de cenários
    cenarios = {
        'impacto_direto': {
            'nome': 'Impacto Direto',
            'descricao': 'Cenário de impacto garantido com asteroide',
            'dt_padrao': 900,
            'tempo_padrao': 0.1
        },
        'apophis': {
            'nome': 'Apophis 2029',
            'descricao': 'Simulação do asteroide Apophis em 2029',
            'dt_padrao': 1800,
            'tempo_padrao': 2.0
        },
        'sistema_solar': {
            'nome': 'Sistema Solar Básico',
            'descricao': 'Terra, Lua e Sol em órbita',
            'dt_padrao': 3600,
            'tempo_padrao': 1.0
        }
    }
    
    return jsonify({
        'configuracoes': config,
        'cenarios': cenarios,
        'constantes': {
            'G': G,
            'UA': UA,
            'M_SOL': M_SOL,
            'M_TERRA': M_TERRA,
            'R_TERRA': R_TERRA
        }
    })

@app.route('/api/simular', methods=['POST'])
def executar_simulacao():
    """Executa uma simulação com os parâmetros fornecidos."""
    try:
        dados = request.get_json()
        
        # Extrair parâmetros
        cenario = dados.get('cenario', 'impacto_direto')
        dt = float(dados.get('dt', 900))
        tempo_total = float(dados.get('tempo_total', 0.1))
        
        # Parâmetros do asteroide (se aplicável)
        massa_asteroide = float(dados.get('massa_asteroide', 1e11))
        distancia_inicial = float(dados.get('distancia_inicial', 20))
        velocidade_aproximacao = float(dados.get('velocidade_aproximacao', 20000))
        
        # Criar sistema baseado no cenário
        if cenario == 'impacto_direto':
            sistema = criar_sistema_impacto_melhorado()
            # Ajustar parâmetros do asteroide
            asteroide = next(c for c in sistema.corpos if c.nome == "Asteroide")
            asteroide.massa = massa_asteroide
        elif cenario == 'apophis':
            sistema = criar_sistema_apophis_melhorado()
        else:  # sistema_solar
            sistema = criar_sistema_solar_basico()
        
        # Configurar passo de tempo
        sistema.dt = dt
        
        # Executar simulação
        tempo_segundos = tempo_total * ANOS_EM_SEGUNDOS
        resultado = sistema.simular(tempo_segundos, progresso=False)
        
        # Gerar ID único para a simulação
        sim_id = f"sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Salvar resultados
        RESULTADOS_RECENTES[sim_id] = {
            'sistema': sistema,
            'resultado': resultado,
            'parametros': dados,
            'timestamp': datetime.now().isoformat()
        }
        
        # Preparar dados para resposta
        dados_resposta = {
            'sim_id': sim_id,
            'status': 'sucesso',
            'resultado': {
                'houve_colisao': resultado.houve_colisao,
                'distancia_minima': float(resultado.distancia_minima),
                'distancia_superficie': float(resultado.distancia_superficie),
                'tempo_minima': float(resultado.tempo_minima),
                'velocidade_relativa_minima': float(resultado.velocidade_relativa_minima),
                'aproximacao_perigosa': resultado.aproximacao_perigosa,
                'energia_impacto': float(resultado.energia_impacto) if resultado.houve_colisao else 0,
                'equivalente_tnt': float(resultado.equivalente_tnt) if resultado.houve_colisao else 0,
                'raio_cratera': float(resultado.raio_cratera) if resultado.houve_colisao else 0,
                'profundidade_cratera': float(resultado.profundidade_cratera) if resultado.houve_colisao else 0,
                'tempo_simulacao': float(resultado.tempo_simulacao),
                'numero_passos': resultado.numero_passos
            },
            'relatorio': resultado.gerar_relatorio()
        }
        
        return jsonify(dados_resposta)
        
    except Exception as e:
        return jsonify({
            'status': 'erro',
            'mensagem': str(e)
        }), 500

@app.route('/api/grafico/<sim_id>')
def gerar_grafico(sim_id):
    """Gera gráfico da simulação."""
    if sim_id not in RESULTADOS_RECENTES:
        return jsonify({'erro': 'Simulação não encontrada'}), 404
    
    dados = RESULTADOS_RECENTES[sim_id]
    sistema = dados['sistema']
    
    # Criar figura
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Gráfico 1: Trajetórias
    for corpo in sistema.corpos:
        x, y = corpo.get_trajetoria_2d()
        if len(x) > 0:
            ax1.plot(x/UA, y/UA, '-', label=corpo.nome, linewidth=2)
            ax1.plot(x[0]/UA, y[0]/UA, 'o', markersize=8)
            ax1.plot(x[-1]/UA, y[-1]/UA, 's', markersize=6)
    
    ax1.set_xlabel('x (UA)')
    ax1.set_ylabel('y (UA)')
    ax1.set_title('Trajetórias dos Corpos')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.axis('equal')
    
    # Gráfico 2: Distância vs Tempo
    terra = next(c for c in sistema.corpos if c.nome == "Terra")
    asteroide = next(c for c in sistema.corpos if c.nome == "Asteroide")
    
    if len(terra.historico_posicao) > 0 and len(asteroide.historico_posicao) > 0:
        n_pontos = min(len(terra.historico_posicao), len(asteroide.historico_posicao))
        tempos = np.array(terra.historico_tempo[:n_pontos]) / ANOS_EM_SEGUNDOS
        distancias = []
        
        for i in range(n_pontos):
            d = np.linalg.norm(asteroide.historico_posicao[i] - terra.historico_posicao[i])
            distancias.append(d)
        
        distancias = np.array(distancias)
        
        ax2.plot(tempos, distancias/1000, 'b-', linewidth=2, label='Distância Terra-Asteroide')
        ax2.axhline(R_TERRA/1000, color='green', linestyle='--', linewidth=2, 
                   alpha=0.7, label='Raio da Terra')
        
        # Marcar evento de colisão
        if dados['resultado'].houve_colisao:
            ax2.axvline(dados['resultado'].tempo_colisao/ANOS_EM_SEGUNDOS, color='red', 
                       linestyle=':', linewidth=3, label='Momento do Impacto')
    
    ax2.set_xlabel('Tempo (anos)')
    ax2.set_ylabel('Distância (km)')
    ax2.set_title('Evolução da Distância')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_yscale('log')
    
    plt.tight_layout()
    
    # Converter para base64
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    return jsonify({'grafico': img_base64})

@app.route('/api/resultados/<sim_id>')
def obter_resultado(sim_id):
    """Retorna resultado de uma simulação específica."""
    if sim_id not in RESULTADOS_RECENTES:
        return jsonify({'erro': 'Simulação não encontrada'}), 404
    
    dados = RESULTADOS_RECENTES[sim_id]
    return jsonify({
        'sim_id': sim_id,
        'parametros': dados['parametros'],
        'resultado': dados['resultado'],
        'timestamp': dados['timestamp']
    })

@app.route('/api/lista_simulacoes')
def listar_simulacoes():
    """Lista todas as simulações realizadas."""
    lista = []
    for sim_id, dados in RESULTADOS_RECENTES.items():
        lista.append({
            'sim_id': sim_id,
            'cenario': dados['parametros'].get('cenario', 'desconhecido'),
            'timestamp': dados['timestamp'],
            'houve_colisao': dados['resultado'].houve_colisao,
            'distancia_minima': float(dados['resultado'].distancia_minima)
        })
    
    return jsonify({'simulacoes': lista})

def criar_sistema_solar_basico():
    """Cria sistema solar básico com Terra, Lua e Sol."""
    sistema = SistemaGravitacional(dt=3600)
    
    # Sol
    sol = CorpoCeleste(
        nome="Sol",
        massa=M_SOL,
        posicao=[0, 0, 0],
        velocidade=[0, 0, 0],
        cor='yellow',
        raio_visual=20,
        raio_fisico=6.96e8
    )
    
    # Terra
    v_orbital_terra = np.sqrt(G * M_SOL / UA)
    terra = CorpoCeleste(
        nome="Terra",
        massa=M_TERRA,
        posicao=[UA, 0, 0],
        velocidade=[0, v_orbital_terra, 0],
        cor='blue',
        raio_visual=10,
        raio_fisico=R_TERRA
    )
    
    # Lua
    distancia_terra_lua = 3.844e8  # 384,400 km
    v_orbital_lua = np.sqrt(G * M_TERRA / distancia_terra_lua)
    lua = CorpoCeleste(
        nome="Lua",
        massa=7.342e22,
        posicao=[UA + distancia_terra_lua, 0, 0],
        velocidade=[0, v_orbital_terra + v_orbital_lua, 0],
        cor='gray',
        raio_visual=5,
        raio_fisico=1.737e6
    )
    
    sistema.adicionar_corpo(sol)
    sistema.adicionar_corpo(terra)
    sistema.adicionar_corpo(lua)
    
    return sistema

if __name__ == '__main__':
    # Criar diretórios necessários
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    
    # Verificar se a porta 5000 está disponível, senão usar 5001
    import socket
    def verificar_porta(porta):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', porta)) != 0
    
    porta = 5000 if verificar_porta(5000) else 5001
    
    print("Iniciando interface web do Simulador Orbital...")
    print(f"Acesse: http://localhost:{porta}")
    app.run(debug=True, host='0.0.0.0', port=porta)
