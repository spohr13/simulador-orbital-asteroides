# ==============================================================================
# CLASSE CORPO CELESTE - REPRESENTA UM CORPO NO SISTEMA GRAVITACIONAL
# ==============================================================================

import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from constants import *


@dataclass
class CorpoCeleste:
    """
    Representa um corpo celeste no sistema gravitacional.
    
    Atributos:
        nome (str): Nome do corpo celeste
        massa (float): Massa em kg
        posicao (np.ndarray): Posição [x, y, z] em metros
        velocidade (np.ndarray): Velocidade [vx, vy, vz] em m/s
        cor (str): Cor para visualização
        raio_visual (float): Raio para visualização
        raio_fisico (float): Raio físico real do corpo (m)
        tipo (str): Tipo do corpo celeste
        densidade (float): Densidade média (kg/m³)
        historico_posicao (List): Histórico de posições
        historico_velocidade (List): Histórico de velocidades
        historico_tempo (List): Histórico de tempos
    """
    nome: str
    massa: float
    posicao: np.ndarray
    velocidade: np.ndarray
    cor: str = 'blue'
    raio_visual: float = 5.0
    raio_fisico: float = 0.0
    tipo: str = TIPO_PLANETA
    densidade: float = 0.0
    
    # Histórico de trajetória
    historico_posicao: List[np.ndarray] = field(default_factory=list)
    historico_velocidade: List[np.ndarray] = field(default_factory=list)
    historico_tempo: List[float] = field(default_factory=list)
    
    def __post_init__(self):
        """Inicializa arrays como numpy arrays e calcula propriedades."""
        self.posicao = np.array(self.posicao, dtype=np.float64)
        self.velocidade = np.array(self.velocidade, dtype=np.float64)
        self.aceleracao = np.zeros(3, dtype=np.float64)
        
        # Calcular raio físico se não foi definido
        if self.raio_fisico == 0.0:
            self.raio_fisico = self._calcular_raio_fisico()
        
        # Calcular densidade se não foi definida
        if self.densidade == 0.0:
            self.densidade = self._calcular_densidade()
    
    def _calcular_raio_fisico(self) -> float:
        """Calcula o raio físico baseado no nome e massa."""
        if self.nome == "Sol":
            return R_SOL
        elif self.nome == "Terra":
            return R_TERRA
        elif self.nome == "Lua":
            return R_LUA
        elif self.nome == "Jupiter":
            return R_JUPITER
        elif self.nome == "Marte":
            return R_MARTE
        elif self.nome == "Venus":
            return R_VENUS
        elif self.nome == "Mercurio":
            return R_MERCURIO
        elif "Asteroide" in self.nome or self.tipo == TIPO_ASTEROIDE:
            # Estimar raio do asteroide baseado na massa
            if self.densidade > 0:
                densidade = self.densidade
            else:
                densidade = DENSIDADE_ASTEROIDE_PADRAO
            volume = self.massa / densidade
            return (3 * volume / (4 * np.pi)) ** (1/3)
        else:
            # Valor padrão baseado na massa
            densidade_padrao = 3000  # kg/m³
            volume = self.massa / densidade_padrao
            return (3 * volume / (4 * np.pi)) ** (1/3)
    
    def _calcular_densidade(self) -> float:
        """Calcula a densidade média do corpo."""
        if self.raio_fisico > 0:
            volume = (4/3) * np.pi * self.raio_fisico**3
            return self.massa / volume
        return DENSIDADE_ASTEROIDE_PADRAO
    
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
    
    def get_trajetoria_3d(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Retorna arrays x, y e z da trajetória para plotagem 3D."""
        if not self.historico_posicao:
            return np.array([]), np.array([]), np.array([])
        posicoes = np.array(self.historico_posicao)
        return posicoes[:, 0], posicoes[:, 1], posicoes[:, 2]
    
    def distancia_para(self, outro_corpo: 'CorpoCeleste') -> float:
        """Calcula a distância até outro corpo."""
        return np.linalg.norm(self.posicao - outro_corpo.posicao)
    
    def velocidade_relativa(self, outro_corpo: 'CorpoCeleste') -> np.ndarray:
        """Calcula a velocidade relativa em relação a outro corpo."""
        return self.velocidade - outro_corpo.velocidade
    
    def velocidade_escalar(self) -> float:
        """Retorna a magnitude da velocidade."""
        return np.linalg.norm(self.velocidade)
    
    def energia_potencial_com(self, outro_corpo: 'CorpoCeleste') -> float:
        """Calcula a energia potencial gravitacional com outro corpo."""
        distancia = self.distancia_para(outro_corpo)
        if distancia > 0:
            return -G * self.massa * outro_corpo.massa / distancia
        return 0.0
    
    def aceleracao_gravitacional_de(self, outro_corpo: 'CorpoCeleste') -> np.ndarray:
        """Calcula a aceleração gravitacional causada por outro corpo."""
        r_vec = outro_corpo.posicao - self.posicao
        r_mag = np.linalg.norm(r_vec)
        
        if r_mag > 0:
            r_hat = r_vec / r_mag
            a_mag = G * outro_corpo.massa / (r_mag ** 2)
            return a_mag * r_hat
        return np.zeros(3)
    
    def periodo_orbital_aproximado(self, corpo_central: 'CorpoCeleste') -> float:
        """Calcula o período orbital aproximado em torno de um corpo central."""
        if corpo_central.massa <= 0:
            return 0.0
        
        # Lei de Kepler: T² = (4π²a³)/(GM)
        # Para órbita circular: a = r
        distancia = self.distancia_para(corpo_central)
        if distancia > 0:
            periodo = 2 * np.pi * np.sqrt(distancia**3 / (G * corpo_central.massa))
            return periodo
        return 0.0
    
    def velocidade_orbital_circular(self, corpo_central: 'CorpoCeleste') -> float:
        """Calcula a velocidade orbital circular em torno de um corpo central."""
        distancia = self.distancia_para(corpo_central)
        if distancia > 0:
            return np.sqrt(G * corpo_central.massa / distancia)
        return 0.0
    
    def excentricidade_orbital(self, corpo_central: 'CorpoCeleste') -> float:
        """Calcula a excentricidade orbital em relação a um corpo central."""
        # Implementação simplificada - requer análise mais complexa para precisão
        v_orbital = self.velocidade_orbital_circular(corpo_central)
        v_atual = self.velocidade_escalar()
        
        if v_orbital > 0:
            return abs(v_atual - v_orbital) / v_orbital
        return 0.0
    
    def esta_em_orbita_estavel(self, corpo_central: 'CorpoCeleste', 
                              tolerancia: float = 0.1) -> bool:
        """Verifica se está em órbita estável em torno de um corpo central."""
        v_orbital = self.velocidade_orbital_circular(corpo_central)
        v_atual = self.velocidade_escalar()
        
        if v_orbital > 0:
            diferenca_relativa = abs(v_atual - v_orbital) / v_orbital
            return diferenca_relativa < tolerancia
        return False
    
    def limpar_historico(self):
        """Limpa o histórico de trajetória."""
        self.historico_posicao.clear()
        self.historico_velocidade.clear()
        self.historico_tempo.clear()
    
    def get_estado_atual(self) -> dict:
        """Retorna o estado atual como dicionário."""
        return {
            'nome': self.nome,
            'massa': self.massa,
            'posicao': self.posicao.copy(),
            'velocidade': self.velocidade.copy(),
            'aceleracao': self.aceleracao.copy(),
            'raio_fisico': self.raio_fisico,
            'densidade': self.densidade,
            'tipo': self.tipo,
            'energia_cinetica': self.energia_cinetica(),
            'velocidade_escalar': self.velocidade_escalar()
        }
    
    def __str__(self) -> str:
        """Representação string do corpo celeste."""
        return (f"CorpoCeleste(nome='{self.nome}', massa={self.massa:.2e} kg, "
                f"posicao={self.posicao}, velocidade={self.velocidade})")
    
    def __repr__(self) -> str:
        """Representação detalhada do corpo celeste."""
        return (f"CorpoCeleste(nome='{self.nome}', tipo='{self.tipo}', "
                f"massa={self.massa:.2e} kg, raio={self.raio_fisico:.0f} m, "
                f"densidade={self.densidade:.0f} kg/m³)")
