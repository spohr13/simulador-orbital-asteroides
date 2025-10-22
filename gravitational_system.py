# ==============================================================================
# CLASSE SISTEMA GRAVITACIONAL - GERENCIA O SISTEMA DE MÚLTIPLOS CORPOS
# ==============================================================================

import numpy as np
from typing import List, Tuple, Optional, Dict, Any
from datetime import datetime
import time

from constants import *
from celestial_body import CorpoCeleste
from simulation_result import ResultadoSimulacao


class SistemaGravitacional:
    """
    Gerencia o sistema de múltiplos corpos e a evolução temporal.
    
    Esta classe é responsável por:
    - Gerenciar os corpos celestes do sistema
    - Calcular forças gravitacionais
    - Integrar as equações de movimento
    - Detectar colisões e aproximações
    - Validar a conservação de energia e momento angular
    """
    
    def __init__(self, dt: float = DT_PADRAO, nome: str = "Sistema"):
        """
        Inicializa o sistema gravitacional.
        
        Args:
            dt (float): Passo de tempo da simulação em segundos
            nome (str): Nome do sistema
        """
        self.corpos: List[CorpoCeleste] = []
        self.dt = dt
        self.tempo_atual = 0.0
        self.nome = nome
        self.resultado = ResultadoSimulacao()
        self.estado = ESTADO_INICIANDO
        self.versao = "2.0"
        
        # Configurações de simulação
        self.tolerancia_energia = TOLERANCIA_ENERGIA
        self.tolerancia_momento = TOLERANCIA_MOMENTO
        self.verificar_conservacao_frequencia = 100  # A cada N passos
        
        # Estatísticas
        self.numero_simulacoes = 0
        self.tempo_total_simulado = 0.0
    
    def adicionar_corpo(self, corpo: CorpoCeleste):
        """Adiciona um corpo ao sistema."""
        self.corpos.append(corpo)
        self.resultado.corpos_participantes.append(corpo.nome)
    
    def remover_corpo(self, nome: str) -> bool:
        """Remove um corpo do sistema pelo nome."""
        for i, corpo in enumerate(self.corpos):
            if corpo.nome == nome:
                self.corpos.pop(i)
                if nome in self.resultado.corpos_participantes:
                    self.resultado.corpos_participantes.remove(nome)
                return True
        return False
    
    def get_corpo(self, nome: str) -> Optional[CorpoCeleste]:
        """Retorna um corpo pelo nome."""
        for corpo in self.corpos:
            if corpo.nome == nome:
                return corpo
        return None
    
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
        corpo1 = self.get_corpo(corpo1_nome)
        corpo2 = self.get_corpo(corpo2_nome)
        
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
            self.estado = ESTADO_COLISAO
        
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
        
        # Equivalente em TNT
        self.resultado.equivalente_tnt = self.resultado.energia_impacto / MEGATON_TNT
        
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
        densidade_asteroide = asteroide.densidade if asteroide.densidade > 0 else DENSIDADE_ASTEROIDE_PADRAO
        densidade_alvo = DENSIDADE_ALVO_PADRAO
        g = G_TERRA
        
        # Diâmetro do projétil
        d_proj = 2 * asteroide.raio_fisico
        
        # Energia específica
        energia_especifica = 0.5 * v_impacto**2
        
        # Diâmetro da cratera (fórmula de scaling)
        fator_densidade = (densidade_asteroide / densidade_alvo) ** (1/3)
        fator_velocidade = (v_impacto**2 / (g * d_proj)) ** BETA_CRATERA
        
        diametro_cratera = K_CRATERA * fator_densidade * d_proj * fator_velocidade
        self.resultado.diametro_cratera = diametro_cratera
        self.resultado.raio_cratera = diametro_cratera / 2
        
        # Profundidade da cratera
        self.resultado.profundidade_cratera = diametro_cratera * PROFUNDIDADE_FATOR
        
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
        if massa_total == 0:
            return np.zeros(3)
        
        cm = np.zeros(3)
        for corpo in self.corpos:
            cm += corpo.massa * corpo.posicao
        
        return cm / massa_total
    
    def verificar_conservacao_energia(self, passo: int) -> bool:
        """Verifica a conservação de energia."""
        if passo % self.verificar_conservacao_frequencia == 0:
            energia_atual = self.energia_total()
            erro_rel = abs(energia_atual - self.resultado.energia_inicial) / abs(self.resultado.energia_inicial)
            
            if erro_rel > self.tolerancia_energia:
                print(f"Aviso: Erro de conservação = {erro_rel:.2e} no passo {passo}")
                return False
        return True
    
    def simular(self, tempo_total: float, progresso: bool = True, 
                parar_em_colisao: bool = True) -> ResultadoSimulacao:
        """
        Executa a simulação por um tempo total especificado.
        
        Args:
            tempo_total (float): Tempo total da simulação em segundos
            progresso (bool): Se deve mostrar progresso
            parar_em_colisao (bool): Se deve parar quando detectar colisão
            
        Returns:
            ResultadoSimulacao: Resultados da simulação
        """
        # Inicializar resultado
        self.resultado.energia_inicial = self.energia_total()
        self.resultado.momento_angular_inicial = self.momento_angular_total()
        self.resultado.timestamp_inicio = time.time()
        self.resultado.dt_usado = self.dt
        self.estado = ESTADO_EXECUTANDO
        
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
            if self.resultado.houve_colisao and parar_em_colisao:
                if progresso:
                    print(f"Simulação interrompida devido à colisão no passo {passo}")
                break
            
            # Verificar conservação de energia
            if not self.verificar_conservacao_energia(passo):
                if progresso:
                    print(f"Erro de conservação detectado no passo {passo}")
            
            # Mostrar progresso
            if progresso and passo % (n_passos // 20) == 0:
                percentual = 100 * passo / n_passos
                print(f"Progresso: {percentual:.1f}% ({passo}/{n_passos} passos)")
        
        # Cálculos finais
        self.resultado.energia_final = self.energia_total()
        self.resultado.calcular_erro_energia()
        
        self.resultado.momento_angular_final = self.momento_angular_total()
        self.resultado.calcular_erro_momento_angular()
        
        self.resultado.timestamp_fim = time.time()
        self.estado = ESTADO_FINALIZADO
        
        # Atualizar estatísticas
        self.numero_simulacoes += 1
        self.tempo_total_simulado += self.tempo_atual
        
        if progresso:
            print("\nSimulação concluída!")
        
        return self.resultado
    
    def reset(self):
        """Reseta o sistema para o estado inicial."""
        self.tempo_atual = 0.0
        self.estado = ESTADO_INICIANDO
        self.resultado = ResultadoSimulacao()
        
        # Limpar histórico de todos os corpos
        for corpo in self.corpos:
            corpo.limpar_historico()
    
    def get_estatisticas(self) -> Dict[str, Any]:
        """Retorna estatísticas do sistema."""
        return {
            'nome': self.nome,
            'numero_corpos': len(self.corpos),
            'numero_simulacoes': self.numero_simulacoes,
            'tempo_total_simulado': self.tempo_total_simulado,
            'dt_atual': self.dt,
            'estado': self.estado,
            'versao': self.versao
        }
    
    def __str__(self) -> str:
        """Representação string do sistema."""
        return f"SistemaGravitacional('{self.nome}', {len(self.corpos)} corpos, dt={self.dt}s)"
    
    def __repr__(self) -> str:
        """Representação detalhada do sistema."""
        corpos_str = [corpo.nome for corpo in self.corpos]
        return (f"SistemaGravitacional(nome='{self.nome}', corpos={corpos_str}, "
                f"dt={self.dt}, estado='{self.estado}')")
