# ==============================================================================
# SIMULADOR ORBITAL DE ASTEROIDES - VERSÃO CORRIGIDA
# Melhorias na detecção de colisão e parâmetros de impacto
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
import json
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Constantes Físicas
G = 6.67430e-11  # Constante gravitacional (m³/kg/s²)
UA = 1.496e11    # Unidade Astronômica (m)
M_SOL = 1.989e30  # Massa do Sol (kg)
M_TERRA = 5.972e24  # Massa da Terra (kg)
R_TERRA = 6.371e6  # Raio da Terra (m)
M_LUA = 7.342e22  # Massa da Lua (kg)

# Configurações de Simulação
DT_PADRAO = 3600  # Passo de tempo padrão: 1 hora (s)
TOLERANCIA_ENERGIA = 1e-6  # Tolerância para conservação de energia
ANOS_EM_SEGUNDOS = 365.25 * 24 * 3600

# Novos parâmetros para detecção de colisão
FATOR_SEGURANCA_COLISAO = 1.1  # Margem de segurança para detecção
DISTANCIA_MINIMA_DETECCAO = R_TERRA * 10  # Distância para começar monitoramento próximo

@dataclass
class CorpoCeleste:
    """
    Representa um corpo celeste no sistema gravitacional.
    """
    nome: str
    massa: float  # kg
    posicao: np.ndarray  # [x, y, z] em metros
    velocidade: np.ndarray  # [vx, vy, vz] em m/s
    cor: str = 'blue'
    raio_visual: float = 5.0
    raio_fisico: float = 0.0  # Raio físico real do corpo (m)
    
    # Histórico de trajetória
    historico_posicao: List[np.ndarray] = field(default_factory=list)
    historico_velocidade: List[np.ndarray] = field(default_factory=list)
    historico_tempo: List[float] = field(default_factory=list)
    
    def __post_init__(self):
        """Inicializa arrays como numpy arrays."""
        self.posicao = np.array(self.posicao, dtype=np.float64)
        self.velocidade = np.array(self.velocidade, dtype=np.float64)
        self.aceleracao = np.zeros(3, dtype=np.float64)
        
        # Se raio físico não foi definido, usar valores padrão baseados no nome
        if self.raio_fisico == 0.0:
            if self.nome == "Terra":
                self.raio_fisico = R_TERRA
            elif self.nome == "Sol":
                self.raio_fisico = 6.96e8  # Raio do Sol
            elif "Asteroide" in self.nome:
                # Estimar raio do asteroide baseado na massa (assumindo densidade ~3000 kg/m³)
                densidade = 3000
                volume = self.massa / densidade
                self.raio_fisico = (3 * volume / (4 * np.pi)) ** (1/3)
            else:
                self.raio_fisico = 1000  # Valor padrão: 1 km
    
    def salvar_estado(self, tempo: float):
        """Salva o estado atual no histórico."""
        self.historico_posicao.append(self.posicao.copy())
        self.historico_velocidade.append(self.velocidade.copy())
        self.historico_tempo.append(tempo)
    
    def energia_cinetica(self) -> float:
        """Calcula a energia cinética do corpo."""
        v_quadrado = np.sum(self.velocidade ** 2)
        return 0.5 * self.massa * v_quadrado
    
    def momento_angular(self, origem: np.ndarray = None) -> np.ndarray:
        """Calcula o momento angular em relação a uma origem."""
        if origem is None:
            origem = np.zeros(3)
        r = self.posicao - origem
        return self.massa * np.cross(r, self.velocidade)
    
    def get_trajetoria_2d(self) -> Tuple[np.ndarray, np.ndarray]:
        """Retorna arrays x e y da trajetória para plotagem."""
        if not self.historico_posicao:
            return np.array([]), np.array([])
        posicoes = np.array(self.historico_posicao)
        return posicoes[:, 0], posicoes[:, 1]

@dataclass
class ResultadoSimulacao:
    """
    Encapsula todos os resultados de uma simulação.
    """
    distancia_minima: float = float('inf')
    tempo_minima: float = 0.0
    posicao_minima_terra: np.ndarray = field(default_factory=lambda: np.zeros(3))
    posicao_minima_asteroide: np.ndarray = field(default_factory=lambda: np.zeros(3))
    velocidade_relativa_minima: float = 0.0
    
    houve_colisao: bool = False
    tempo_colisao: float = 0.0
    velocidade_impacto: float = 0.0
    angulo_impacto: float = 0.0
    energia_impacto: float = 0.0
    equivalente_tnt: float = 0.0
    raio_cratera: float = 0.0
    profundidade_cratera: float = 0.0
    
    # Novos campos para detecção melhorada
    aproximacao_perigosa: bool = False
    tempo_aproximacao_perigosa: float = 0.0
    distancia_superficie: float = float('inf')
    parametro_impacto: float = 0.0
    
    energia_inicial: float = 0.0
    energia_final: float = 0.0
    erro_energia_relativo: float = 0.0
    
    momento_angular_inicial: np.ndarray = field(default_factory=lambda: np.zeros(3))
    momento_angular_final: np.ndarray = field(default_factory=lambda: np.zeros(3))
    erro_momento_relativo: float = 0.0
    
    tempo_simulacao: float = 0.0
    numero_passos: int = 0
    
    def gerar_relatorio(self) -> str:
        """Gera um relatório textual dos resultados."""
        relatorio = []
        relatorio.append("=" * 70)
        relatorio.append("RELATÓRIO DA SIMULAÇÃO ORBITAL".center(70))
        relatorio.append("=" * 70)
        relatorio.append("")
        
        # Informações temporais
        relatorio.append("INFORMAÇÕES TEMPORAIS:")
        relatorio.append(f"  Tempo total simulado: {self.tempo_simulacao/ANOS_EM_SEGUNDOS:.2f} anos")
        relatorio.append(f"  Número de passos: {self.numero_passos:,}")
        relatorio.append("")
        
        # Aproximação mínima
        relatorio.append("APROXIMAÇÃO MÍNIMA:")
        relatorio.append(f"  Distância mínima: {self.distancia_minima/1000:.2f} km")
        relatorio.append(f"  Distância da superfície: {self.distancia_superficie/1000:.2f} km")
        relatorio.append(f"  Distância em raios terrestres: {self.distancia_minima/R_TERRA:.2f} R⊕")
        relatorio.append(f"  Tempo da aproximação: {self.tempo_minima/ANOS_EM_SEGUNDOS:.4f} anos")
        relatorio.append(f"  Velocidade relativa: {self.velocidade_relativa_minima/1000:.2f} km/s")
        relatorio.append(f"  Parâmetro de impacto: {self.parametro_impacto/1000:.2f} km")
        relatorio.append("")
        
        # Aproximação perigosa
        if self.aproximacao_perigosa:
            relatorio.append("APROXIMAÇÃO PERIGOSA DETECTADA!")
            relatorio.append(f"  Tempo: {self.tempo_aproximacao_perigosa/ANOS_EM_SEGUNDOS:.4f} anos")
        
        # Colisão (se houver)
        if self.houve_colisao:
            relatorio.append("COLISÃO DETECTADA!")
            relatorio.append(f"  Tempo de impacto: {self.tempo_colisao/ANOS_EM_SEGUNDOS:.4f} anos")
            relatorio.append(f"  Velocidade de impacto: {self.velocidade_impacto/1000:.2f} km/s")
            relatorio.append(f"  Ângulo de impacto: {self.angulo_impacto:.2f}°")
            relatorio.append(f"  Energia de impacto: {self.energia_impacto:.2e} J")
            relatorio.append(f"  Equivalente em TNT: {self.equivalente_tnt:.2e} megatons")
            relatorio.append(f"  Raio estimado da cratera: {self.raio_cratera/1000:.2f} km")
            relatorio.append(f"  Profundidade da cratera: {self.profundidade_cratera/1000:.2f} km")
        else:
            relatorio.append("Nenhuma colisão detectada")
        relatorio.append("")
        
        # Conservação de energia
        relatorio.append("VALIDAÇÃO FÍSICA:")
        relatorio.append(f"  Energia inicial: {self.energia_inicial:.6e} J")
        relatorio.append(f"  Energia final: {self.energia_final:.6e} J")
        relatorio.append(f"  Erro relativo de energia: {self.erro_energia_relativo:.2e}")
        if abs(self.erro_energia_relativo) < TOLERANCIA_ENERGIA:
            relatorio.append("  Energia conservada dentro da tolerância")
        else:
            relatorio.append("  Aviso: Violação na conservação de energia")
        relatorio.append("")
        
        relatorio.append("=" * 70)
        
        return "\n".join(relatorio)

class SistemaGravitacional:
    """
    Gerencia o sistema de múltiplos corpos e a evolução temporal.
    """
    
    def __init__(self, dt: float = DT_PADRAO):
        self.corpos: List[CorpoCeleste] = []
        self.dt = dt
        self.tempo_atual = 0.0
        self.resultado = ResultadoSimulacao()
        
    def adicionar_corpo(self, corpo: CorpoCeleste):
        """Adiciona um corpo ao sistema."""
        self.corpos.append(corpo)
    
    def calcular_forca_gravitacional(self, corpo1: CorpoCeleste, 
                                     corpo2: CorpoCeleste) -> np.ndarray:
        """
        Calcula a força gravitacional que corpo2 exerce sobre corpo1.
        F = G * m1 * m2 / r² * r_hat
        """
        r_vec = corpo2.posicao - corpo1.posicao
        r_mag = np.linalg.norm(r_vec)
        
        # Distância mínima para evitar singularidades
        r_min = max(corpo1.raio_fisico + corpo2.raio_fisico, 1e3)
        if r_mag < r_min:
            r_mag = r_min
        
        r_hat = r_vec / r_mag
        f_mag = G * corpo1.massa * corpo2.massa / (r_mag ** 2)
        
        return f_mag * r_hat / corpo1.massa  # Retorna aceleração
    
    def calcular_aceleracoes(self):
        """Calcula as acelerações de todos os corpos."""
        # Zerar acelerações
        for corpo in self.corpos:
            corpo.aceleracao = np.zeros(3)
        
        # Calcular forças entre todos os pares
        n = len(self.corpos)
        for i in range(n):
            for j in range(i + 1, n):
                # Força que j exerce sobre i
                a_i = self.calcular_forca_gravitacional(self.corpos[i], self.corpos[j])
                # Força que i exerce sobre j (terceira lei de Newton)
                a_j = -a_i * self.corpos[i].massa / self.corpos[j].massa
                
                self.corpos[i].aceleracao += a_i
                self.corpos[j].aceleracao += a_j
    
    def detectar_colisao_melhorada(self, corpo1_nome: str = "Terra", 
                                   corpo2_nome: str = "Asteroide"):
        """
        Detecção de colisão melhorada com múltiplos critérios.
        """
        corpo1 = next((c for c in self.corpos if c.nome == corpo1_nome), None)
        corpo2 = next((c for c in self.corpos if c.nome == corpo2_nome), None)
        
        if corpo1 is None or corpo2 is None:
            return
        
        # Calcular distância centro-a-centro
        r_vec = corpo2.posicao - corpo1.posicao
        distancia_centros = np.linalg.norm(r_vec)
        
        # Calcular distância das superfícies
        distancia_superficies = distancia_centros - corpo1.raio_fisico - corpo2.raio_fisico
        
        # Velocidade relativa
        v_relativa = corpo2.velocidade - corpo1.velocidade
        v_rel_mag = np.linalg.norm(v_relativa)
        
        # Verificar se está se aproximando (produto escalar negativo)
        if distancia_centros > 0:
            r_hat = r_vec / distancia_centros
            v_radial = np.dot(v_relativa, r_hat)
            aproximando = v_radial < 0
        else:
            aproximando = False
        
        # CRITÉRIO 1: Colisão física (superfícies se tocam)
        if distancia_superficies <= 0 and not self.resultado.houve_colisao:
            self.resultado.houve_colisao = True
            self.resultado.tempo_colisao = self.tempo_atual
            self.calcular_parametros_impacto_melhorados(corpo1, corpo2, v_relativa, r_vec)
            print(f"COLISÃO DETECTADA no tempo {self.tempo_atual/ANOS_EM_SEGUNDOS:.4f} anos!")
        
        # CRITÉRIO 2: Aproximação perigosa (dentro de 10 raios terrestres)
        elif distancia_centros < DISTANCIA_MINIMA_DETECCAO and aproximando and not self.resultado.aproximacao_perigosa:
            self.resultado.aproximacao_perigosa = True
            self.resultado.tempo_aproximacao_perigosa = self.tempo_atual
            print(f"Aproximação perigosa detectada no tempo {self.tempo_atual/ANOS_EM_SEGUNDOS:.4f} anos!")
        
        # CRITÉRIO 3: Atualizar distância mínima
        if distancia_centros < self.resultado.distancia_minima:
            self.resultado.distancia_minima = distancia_centros
            self.resultado.distancia_superficie = distancia_superficies
            self.resultado.tempo_minima = self.tempo_atual
            self.resultado.posicao_minima_terra = corpo1.posicao.copy()
            self.resultado.posicao_minima_asteroide = corpo2.posicao.copy()
            self.resultado.velocidade_relativa_minima = v_rel_mag
            
            # Calcular parâmetro de impacto
            if aproximando and distancia_centros > 0:
                # Parâmetro de impacto = distância perpendicular à velocidade
                v_rel_hat = v_relativa / v_rel_mag if v_rel_mag > 0 else np.array([0, 0, 1])
                r_perp = r_vec - np.dot(r_vec, v_rel_hat) * v_rel_hat
                self.resultado.parametro_impacto = np.linalg.norm(r_perp)
    
    def calcular_parametros_impacto_melhorados(self, terra: CorpoCeleste, 
                                              asteroide: CorpoCeleste, 
                                              v_relativa: np.ndarray,
                                              r_vec: np.ndarray):
        """Calcula parâmetros físicos do impacto com melhor precisão."""
        v_impacto = np.linalg.norm(v_relativa)
        self.resultado.velocidade_impacto = v_impacto
        
        # Energia cinética de impacto
        self.resultado.energia_impacto = 0.5 * asteroide.massa * v_impacto**2
        
        # Equivalente em TNT (1 megaton = 4.184e15 J)
        self.resultado.equivalente_tnt = self.resultado.energia_impacto / 4.184e15
        
        # Ângulo de impacto (em relação à normal da superfície)
        if np.linalg.norm(r_vec) > 0:
            r_hat = r_vec / np.linalg.norm(r_vec)
            cos_angulo = np.dot(v_relativa, r_hat) / v_impacto
            # Ângulo com a superfície (90° - ângulo com a normal)
            angulo_normal = np.arccos(np.clip(abs(cos_angulo), 0, 1))
            self.resultado.angulo_impacto = 90.0 - np.degrees(angulo_normal)
        
        # Estimativas de cratera mais precisas
        self.calcular_cratera_melhorada(asteroide, v_impacto)
    
    def calcular_cratera_melhorada(self, asteroide: CorpoCeleste, v_impacto: float):
        """
        Calcula dimensões da cratera usando fórmulas empíricas mais precisas.
        Baseado em Melosh (1989) e Collins et al. (2005).
        """
        # Parâmetros físicos
        densidade_asteroide = 3000  # kg/m³ (silicatos típicos)
        densidade_alvo = 2700  # kg/m³ (crosta terrestre)
        g = 9.81  # m/s²
        
        # Diâmetro do projétil
        d_proj = 2 * asteroide.raio_fisico
        
        # Energia específica
        energia_especifica = 0.5 * v_impacto**2
        
        # Diâmetro da cratera (fórmula de scaling)
        # D_crater = K * (ρ_proj/ρ_target)^(1/3) * d_proj * (v²/gR)^β
        K = 1.8  # Constante empírica
        beta = 0.22  # Expoente de scaling
        
        fator_densidade = (densidade_asteroide / densidade_alvo) ** (1/3)
        fator_velocidade = (v_impacto**2 / (g * d_proj)) ** beta
        
        diametro_cratera = K * fator_densidade * d_proj * fator_velocidade
        self.resultado.raio_cratera = diametro_cratera / 2
        
        # Profundidade da cratera (tipicamente 1/5 a 1/3 do diâmetro)
        self.resultado.profundidade_cratera = diametro_cratera * 0.2
        
        # Verificação de regime de cratera
        if self.resultado.raio_cratera > 50e3:  # > 50 km
            print("  Cratera de impacto complexa (anel central)")
        elif self.resultado.raio_cratera > 2e3:  # > 2 km
            print("  Cratera simples de grande escala")
        else:
            print("  Cratera simples")
    
    def get_estado(self) -> np.ndarray:
        """Retorna o estado atual do sistema como vetor."""
        estado = []
        for corpo in self.corpos:
            estado.extend(corpo.posicao)
            estado.extend(corpo.velocidade)
        return np.array(estado, dtype=np.float64)
    
    def set_estado(self, estado: np.ndarray):
        """Define o estado do sistema a partir de um vetor."""
        idx = 0
        for corpo in self.corpos:
            corpo.posicao = estado[idx:idx+3].copy()
            corpo.velocidade = estado[idx+3:idx+6].copy()
            idx += 6
    
    def derivada(self, estado: np.ndarray) -> np.ndarray:
        """
        Calcula a derivada temporal do estado.
        Para cada corpo: d/dt[posição, velocidade] = [velocidade, aceleração]
        """
        # Salvar estado atual
        estado_original = self.get_estado()
        
        # Aplicar estado fornecido
        self.set_estado(estado)
        
        # Calcular acelerações
        self.calcular_aceleracoes()
        
        # Construir vetor de derivadas
        derivadas = []
        for corpo in self.corpos:
            derivadas.extend(corpo.velocidade)  # d(posição)/dt = velocidade
            derivadas.extend(corpo.aceleracao)  # d(velocidade)/dt = aceleração
        
        # Restaurar estado original
        self.set_estado(estado_original)
        
        return np.array(derivadas, dtype=np.float64)
    
    def integrador_rk4(self) -> np.ndarray:
        """
        Implementa o método de Runge-Kutta de 4ª ordem.
        """
        y = self.get_estado()
        
        k1 = self.derivada(y)
        k2 = self.derivada(y + 0.5 * self.dt * k1)
        k3 = self.derivada(y + 0.5 * self.dt * k2)
        k4 = self.derivada(y + self.dt * k3)
        
        y_novo = y + (self.dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        
        return y_novo
    
    def energia_cinetica_total(self) -> float:
        """Calcula a energia cinética total do sistema."""
        return sum(corpo.energia_cinetica() for corpo in self.corpos)
    
    def energia_potencial_total(self) -> float:
        """Calcula a energia potencial gravitacional total do sistema."""
        ep_total = 0.0
        n = len(self.corpos)
        
        for i in range(n):
            for j in range(i + 1, n):
                r = np.linalg.norm(self.corpos[j].posicao - self.corpos[i].posicao)
                if r > 1e3:  # Evitar divisão por zero
                    ep = -G * self.corpos[i].massa * self.corpos[j].massa / r
                    ep_total += ep
        
        return ep_total
    
    def energia_total(self) -> float:
        """Calcula a energia total do sistema."""
        return self.energia_cinetica_total() + self.energia_potencial_total()
    
    def momento_angular_total(self) -> np.ndarray:
        """Calcula o momento angular total do sistema em relação ao centro de massa."""
        centro_massa = self.centro_de_massa()
        l_total = np.zeros(3)
        
        for corpo in self.corpos:
            l_total += corpo.momento_angular(origem=centro_massa)
        
        return l_total
    
    def centro_de_massa(self) -> np.ndarray:
        """Calcula o centro de massa do sistema."""
        massa_total = sum(corpo.massa for corpo in self.corpos)
        cm = np.zeros(3)
        
        for corpo in self.corpos:
            cm += corpo.massa * corpo.posicao
        
        return cm / massa_total
    
    def simular(self, tempo_total: float, progresso: bool = True):
        """
        Executa a simulação por um tempo total especificado.
        """
        # Inicializar resultado
        self.resultado.energia_inicial = self.energia_total()
        self.resultado.momento_angular_inicial = self.momento_angular_total()
        
        # Salvar estados iniciais
        for corpo in self.corpos:
            corpo.salvar_estado(self.tempo_atual)
        
        # Número de passos
        n_passos = int(tempo_total / self.dt)
        self.resultado.numero_passos = n_passos
        self.resultado.tempo_simulacao = tempo_total
        
        if progresso:
            print(f"Iniciando simulação com {n_passos:,} passos...")
            print(f"Passo de tempo: {self.dt/3600:.2f} horas")
        
        # Loop principal
        for passo in range(n_passos):
            # Integrar um passo
            novo_estado = self.integrador_rk4()
            self.set_estado(novo_estado)
            self.tempo_atual += self.dt
            
            # Salvar histórico
            for corpo in self.corpos:
                corpo.salvar_estado(self.tempo_atual)
            
            # Detectar eventos com método melhorado
            self.detectar_colisao_melhorada()
            
            # Parar simulação se houve colisão
            if self.resultado.houve_colisao:
                if progresso:
                    print(f"Simulação interrompida devido à colisão no passo {passo}")
                break
            
            # Verificar conservação de energia (a cada 100 passos)
            if passo % 100 == 0:
                energia_atual = self.energia_total()
                erro_rel = abs(energia_atual - self.resultado.energia_inicial) / abs(self.resultado.energia_inicial)
                
                if erro_rel > TOLERANCIA_ENERGIA and progresso:
                    print(f"Aviso: Erro de conservação = {erro_rel:.2e} no passo {passo}")
            
            # Mostrar progresso
            if progresso and passo % (n_passos // 20) == 0:
                percentual = 100 * passo / n_passos
                print(f"Progresso: {percentual:.1f}% ({passo}/{n_passos} passos)")
        
        # Cálculos finais
        self.resultado.energia_final = self.energia_total()
        self.resultado.erro_energia_relativo = ((self.resultado.energia_final - 
                                                 self.resultado.energia_inicial) / 
                                                abs(self.resultado.energia_inicial))
        
        self.resultado.momento_angular_final = self.momento_angular_total()
        
        if progresso:
            print("\nSimulação concluída!")
        
        return self.resultado

# ==============================================================================
# FUNÇÕES DE CONFIGURAÇÃO ATUALIZADAS
# ==============================================================================

def criar_sistema_impacto_melhorado() -> SistemaGravitacional:
    """Cria cenário hipotético de impacto com detecção melhorada."""
    sistema = SistemaGravitacional(dt=900)  # 15 min para maior precisão
    
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
    
    # Asteroide em rota de colisão (mais realista)
    distancia_inicial = R_TERRA * 20  # 20 raios terrestres
    angulo = np.radians(15)  # Ângulo de aproximação rasante
    
    # Massa baseada em asteroides conhecidos perigosos
    massa_asteroide = 1e11  # 100 milhões de toneladas (similar ao Apophis)
    
    asteroide = CorpoCeleste(
        nome="Asteroide",
        massa=massa_asteroide,
        posicao=[UA + distancia_inicial * np.cos(angulo), 
                 distancia_inicial * np.sin(angulo), 0],
        velocidade=[-20000, v_orbital_terra - 3000, 0],  # Velocidade para colisão
        cor='red',
        raio_visual=8
        # raio_fisico será calculado automaticamente baseado na massa
    )
    
    sistema.adicionar_corpo(sol)
    sistema.adicionar_corpo(terra)
    sistema.adicionar_corpo(asteroide)
    
    return sistema

def criar_sistema_apophis_melhorado() -> SistemaGravitacional:
    """
    Cria sistema com asteroide Apophis com parâmetros mais precisos.
    """
    sistema = SistemaGravitacional(dt=1800)  # 30 min
    
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
    
    # Apophis com parâmetros orbitais reais
    # Dados aproximados para 2029
    a_apophis = 0.92 * UA  # Semi-eixo maior
    e_apophis = 0.19       # Excentricidade
    massa_apophis = 6.1e10  # ~61 milhões de toneladas
    
    # Posição no periélio
    r_perihelio = a_apophis * (1 - e_apophis)
    v_perihelio = np.sqrt(G * M_SOL * (2/r_perihelio - 1/a_apophis))
    
    # Ajustar posição para aproximação da Terra
    apophis = CorpoCeleste(
        nome="Asteroide",
        massa=massa_apophis,
        posicao=[r_perihelio * 0.98, r_perihelio * 0.08, 0],
        velocidade=[-v_perihelio * 0.12, v_perihelio * 0.995, 0],
        cor='red',
        raio_visual=5
    )
    
    sistema.adicionar_corpo(sol)
    sistema.adicionar_corpo(terra)
    sistema.adicionar_corpo(apophis)
    
    return sistema

def teste_deteccao_colisao():
    """Testa especificamente a detecção de colisão."""
    print("\nTESTE: Detecção de Colisão Melhorada")
    print("="*70)
    
    # Criar cenário de impacto garantido
    sistema = criar_sistema_impacto_melhorado()
    
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

# ==============================================================================
# FUNÇÃO PRINCIPAL DE DEMONSTRAÇÃO
# ==============================================================================

def demonstrar_deteccao_melhorada():
    """Demonstra as melhorias na detecção de colisão."""
    print("\n" + "="*70)
    print("DEMONSTRAÇÃO: DETECÇÃO DE COLISÃO MELHORADA".center(70))
    print("="*70)
    
    print("\n1. CENÁRIO DE IMPACTO DIRETO:")
    print("-" * 40)
    
    # Teste 1: Impacto direto
    sistema_impacto = criar_sistema_impacto_melhorado()
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
    sistema_apophis = criar_sistema_apophis_melhorado()
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

# ==============================================================================
# EXEMPLO DE USO COMPLETO
# ==============================================================================

def exemplo_completo_colisao():
    """Exemplo completo mostrando todas as funcionalidades."""
    print("\n" + "="*70)
    print("EXEMPLO COMPLETO: ANÁLISE DE RISCO DE IMPACTO".center(70))
    print("="*70)
    
    # Criar sistema de impacto
    sistema = criar_sistema_impacto_melhorado()
    
    # Mostrar informações iniciais
    asteroide = next(c for c in sistema.corpos if c.nome == "Asteroide")
    terra = next(c for c in sistema.corpos if c.nome == "Terra")
    
    print(f"\nParâmetros do Asteroide:")
    print(f"  Massa: {asteroide.massa:.2e} kg ({asteroide.massa/1e9:.0f} milhões de toneladas)")
    print(f"  Raio estimado: {asteroide.raio_fisico:.0f} m")
    print(f"  Velocidade inicial: {np.linalg.norm(asteroide.velocidade)/1000:.2f} km/s")
    
    distancia_inicial = np.linalg.norm(asteroide.posicao - terra.posicao)
    print(f"  Distância inicial da Terra: {distancia_inicial/1000:.0f} km")
    print(f"  Em raios terrestres: {distancia_inicial/R_TERRA:.1f} R⊕")
    
    # Executar simulação
    print(f"\nExecutando simulação...")
    resultado = sistema.simular(0.2 * ANOS_EM_SEGUNDOS, progresso=True)
    
    # Mostrar relatório completo
    print("\n" + resultado.gerar_relatorio())
    
    # Plotar resultados se matplotlib estiver disponível
    try:
        import matplotlib.pyplot as plt
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Gráfico 1: Trajetórias
        for corpo in sistema.corpos:
            x, y = corpo.get_trajetoria_2d()
            if len(x) > 0:
                ax1.plot(x/UA, y/UA, '-', label=corpo.nome, color=corpo.cor, linewidth=2)
                ax1.plot(x[0]/UA, y[0]/UA, 'o', color=corpo.cor, markersize=8)
                ax1.plot(x[-1]/UA, y[-1]/UA, 's', color=corpo.cor, markersize=6)
        
        ax1.set_xlabel('x (UA)')
        ax1.set_ylabel('y (UA)')
        ax1.set_title('Trajetórias dos Corpos')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.axis('equal')
        
        # Gráfico 2: Distância vs Tempo
        terra = next(c for c in sistema.corpos if c.nome == "Terra")
        asteroide = next(c for c in sistema.corpos if c.nome == "Asteroide")
        
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
        if resultado.houve_colisao:
            ax2.axvline(resultado.tempo_colisao/ANOS_EM_SEGUNDOS, color='red', 
                       linestyle=':', linewidth=3, label='Momento do Impacto')
        
        ax2.set_xlabel('Tempo (anos)')
        ax2.set_ylabel('Distância (km)')
        ax2.set_title('Evolução da Distância')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_yscale('log')
        
        plt.tight_layout()
        plt.show()
        
    except ImportError:
        print("Matplotlib não disponível - pulando visualização")
    
    return sistema, resultado

print("Código corrigido com detecção de colisão melhorada!")
print("\nPara testar as melhorias, execute:")
print("  • demonstrar_deteccao_melhorada()")
print("  • exemplo_completo_colisao()")
print("  • teste_deteccao_colisao()")