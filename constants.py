# ==============================================================================
# CONSTANTES FÍSICAS E CONFIGURAÇÕES DO SIMULADOR ORBITAL
# ==============================================================================

# Constantes Físicas Fundamentais
G = 6.67430e-11  # Constante gravitacional (m³/kg/s²)
C = 299792458    # Velocidade da luz (m/s)

# Unidades Astronômicas
UA = 1.496e11    # Unidade Astronômica (m)
ANO_LUZ = 9.461e15  # Ano-luz (m)
PARSEC = 3.086e16  # Parsec (m)

# Massas dos Corpos Celestes (kg)
M_SOL = 1.989e30      # Massa do Sol
M_TERRA = 5.972e24    # Massa da Terra
M_LUA = 7.342e22      # Massa da Lua
M_JUPITER = 1.898e27 # Massa de Júpiter
M_MARTE = 6.39e23    # Massa de Marte
M_VENUS = 4.867e24   # Massa de Vênus
M_MERCURIO = 3.301e23 # Massa de Mercúrio

# Raios dos Corpos Celestes (m)
R_SOL = 6.96e8       # Raio do Sol
R_TERRA = 6.371e6    # Raio da Terra
R_LUA = 1.737e6      # Raio da Lua
R_JUPITER = 6.9911e7 # Raio de Júpiter
R_MARTE = 3.389e6    # Raio de Marte
R_VENUS = 6.052e6    # Raio de Vênus
R_MERCURIO = 2.439e6  # Raio de Mercúrio

# Configurações de Simulação
DT_PADRAO = 3600           # Passo de tempo padrão: 1 hora (s)
DT_PRECISO = 900           # Passo de tempo preciso: 15 min (s)
DT_RAPIDO = 7200          # Passo de tempo rápido: 2 horas (s)
TOLERANCIA_ENERGIA = 1e-6 # Tolerância para conservação de energia
TOLERANCIA_MOMENTO = 1e-6 # Tolerância para conservação do momento angular

# Conversões de Tempo
ANOS_EM_SEGUNDOS = 365.25 * 24 * 3600
DIAS_EM_SEGUNDOS = 24 * 3600
HORAS_EM_SEGUNDOS = 3600

# Parâmetros de Detecção de Colisão
FATOR_SEGURANCA_COLISAO = 1.1        # Margem de segurança para detecção
DISTANCIA_MINIMA_DETECCAO = R_TERRA * 10  # Distância para monitoramento próximo
DISTANCIA_ALERTA = R_TERRA * 5       # Distância de alerta
DISTANCIA_CRITICA = R_TERRA * 2      # Distância crítica

# Parâmetros de Impacto
DENSIDADE_ASTEROIDE_PADRAO = 3000    # kg/m³ (silicatos típicos)
DENSIDADE_ALVO_PADRAO = 2700         # kg/m³ (crosta terrestre)
G_TERRA = 9.81                       # Aceleração da gravidade terrestre (m/s²)

# Constantes para Cálculos de Cratera
K_CRATERA = 1.8          # Constante empírica para diâmetro da cratera
BETA_CRATERA = 0.22      # Expoente de scaling para cratera
PROFUNDIDADE_FATOR = 0.2 # Fator profundidade/diâmetro da cratera

# Equivalências de Energia
MEGATON_TNT = 4.184e15  # 1 megaton TNT em Joules
KILOTON_TNT = 4.184e12  # 1 kiloton TNT em Joules

# Configurações de Visualização
COR_SOL = 'yellow'
COR_TERRA = 'blue'
COR_LUA = 'gray'
COR_ASTEROIDE = 'red'
COR_JUPITER = 'orange'
COR_MARTE = 'red'
COR_VENUS = 'gold'
COR_MERCURIO = 'brown'

# Tamanhos Visuais Padrão
TAMANHO_SOL = 20
TAMANHO_TERRA = 10
TAMANHO_LUA = 5
TAMANHO_ASTEROIDE = 8
TAMANHO_JUPITER = 15
TAMANHO_MARTE = 8
TAMANHO_VENUS = 9
TAMANHO_MERCURIO = 6

# Configurações de Integração
MAX_PASSOS_SIMULACAO = 1000000  # Máximo de passos por simulação
MIN_PASSO_TEMPO = 1             # Passo mínimo de tempo (s)
MAX_PASSO_TEMPO = 86400         # Passo máximo de tempo (1 dia)

# Configurações de Relatório
PRECISAO_DISTANCIA = 2          # Casas decimais para distâncias (km)
PRECISAO_VELOCIDADE = 2         # Casas decimais para velocidades (km/s)
PRECISAO_ENERGIA = 2            # Casas decimais para energias (J)
PRECISAO_TEMPO = 4              # Casas decimais para tempos (anos)

# Tipos de Corpos Celestes
TIPO_SOL = "Sol"
TIPO_PLANETA = "Planeta"
TIPO_LUA = "Lua"
TIPO_ASTEROIDE = "Asteroide"
TIPO_COMETA = "Cometa"
TIPO_SATELITE = "Satelite"

# Estados de Simulação
ESTADO_INICIANDO = "iniciando"
ESTADO_EXECUTANDO = "executando"
ESTADO_PAUSADO = "pausado"
ESTADO_FINALIZADO = "finalizado"
ESTADO_COLISAO = "colisao"
ESTADO_ERRO = "erro"
