# ==============================================================================
# CLASSE RESULTADO DE SIMULAÇÃO - ARMAZENA E ANALISA RESULTADOS
# ==============================================================================

import numpy as np
from typing import List, Optional
from dataclasses import dataclass, field

from constants import (
    ANOS_EM_SEGUNDOS, R_TERRA, MEGATON_TNT,
    TOLERANCIA_ENERGIA, TOLERANCIA_MOMENTO
)


@dataclass
class ResultadoSimulacao:
    """
    Armazena todos os resultados e métricas de uma simulação orbital.
    """

    # --- Estado geral ---
    estado_final: str = "pendente"
    corpos_participantes: List[str] = field(default_factory=list)
    tempo_simulacao: float = 0.0
    numero_passos: int = 0
    dt_usado: float = 0.0
    timestamp_inicio: float = 0.0
    timestamp_fim: float = 0.0

    # --- Detecção de colisão ---
    houve_colisao: bool = False
    tempo_colisao: float = 0.0
    velocidade_impacto: float = 0.0
    energia_impacto: float = 0.0
    equivalente_tnt: float = 0.0
    angulo_impacto: float = 0.0

    # --- Cratera ---
    diametro_cratera: float = 0.0
    raio_cratera: float = 0.0
    profundidade_cratera: float = 0.0

    # --- Aproximação ---
    aproximacao_perigosa: bool = False
    tempo_aproximacao_perigosa: float = 0.0
    distancia_minima: float = float("inf")
    distancia_superficie: float = float("inf")
    tempo_minima: float = 0.0
    posicao_minima_terra: Optional[np.ndarray] = None
    posicao_minima_asteroide: Optional[np.ndarray] = None
    velocidade_relativa_minima: float = 0.0
    parametro_impacto: float = 0.0

    # --- Conservação de energia ---
    energia_inicial: float = 0.0
    energia_final: float = 0.0
    erro_energia_relativo: float = 0.0

    # --- Conservação do momento angular ---
    momento_angular_inicial: Optional[np.ndarray] = None
    momento_angular_final: Optional[np.ndarray] = None
    erro_momento_angular: float = 0.0

    def calcular_erro_energia(self) -> float:
        if abs(self.energia_inicial) > 0:
            self.erro_energia_relativo = abs(self.energia_final - self.energia_inicial) / abs(self.energia_inicial)
        else:
            self.erro_energia_relativo = 0.0
        return self.erro_energia_relativo

    def calcular_erro_momento_angular(self) -> float:
        if self.momento_angular_inicial is not None and self.momento_angular_final is not None:
            mag_inicial = np.linalg.norm(self.momento_angular_inicial)
            if mag_inicial > 0:
                diferenca = np.linalg.norm(self.momento_angular_final - self.momento_angular_inicial)
                self.erro_momento_angular = diferenca / mag_inicial
            else:
                self.erro_momento_angular = 0.0
        return self.erro_momento_angular

    def fisica_valida(self) -> bool:
        energia_ok = self.erro_energia_relativo < TOLERANCIA_ENERGIA
        momento_ok = self.erro_momento_angular < TOLERANCIA_MOMENTO
        return energia_ok and momento_ok

    def gerar_relatorio(self) -> str:
        linhas: List[str] = []
        sep = "=" * 60
        linhas.append(sep)
        linhas.append("RELATÓRIO DA SIMULAÇÃO".center(60))
        linhas.append(sep)
        linhas.append(f"\nCorpos: {', '.join(self.corpos_participantes)}")
        linhas.append(f"Tempo simulado: {self.tempo_simulacao / ANOS_EM_SEGUNDOS:.4f} anos")
        linhas.append(f"Passos: {self.numero_passos:,}")
        linhas.append(f"Passo de tempo (dt): {self.dt_usado:.0f} s")
        tempo_exec = self.timestamp_fim - self.timestamp_inicio
        if tempo_exec > 0:
            linhas.append(f"Tempo de execução: {tempo_exec:.2f} s")
        linhas.append(f"\n--- Detecção de Colisão ---")
        if self.houve_colisao:
            linhas.append(f"  COLISÃO DETECTADA")
            linhas.append(f"  Tempo: {self.tempo_colisao / ANOS_EM_SEGUNDOS:.6f} anos")
            linhas.append(f"  Velocidade de impacto: {self.velocidade_impacto / 1000:.2f} km/s")
            linhas.append(f"  Energia de impacto: {self.energia_impacto:.2e} J")
            linhas.append(f"  Equivalente TNT: {self.equivalente_tnt:.2f} megatons")
            linhas.append(f"  Ângulo de impacto: {self.angulo_impacto:.1f}°")
            if self.diametro_cratera > 0:
                linhas.append(f"  Diâmetro da cratera: {self.diametro_cratera / 1000:.2f} km")
                linhas.append(f"  Profundidade da cratera: {self.profundidade_cratera / 1000:.2f} km")
        else:
            linhas.append(f"  Sem colisão")
        linhas.append(f"\n--- Aproximação ---")
        linhas.append(f"  Distância mínima: {self.distancia_minima / 1000:.2f} km")
        linhas.append(f"  Distância da superfície: {self.distancia_superficie / 1000:.2f} km")
        linhas.append(f"  Em raios terrestres: {self.distancia_minima / R_TERRA:.2f} R⊕")
        linhas.append(f"  Aproximação perigosa: {'Sim' if self.aproximacao_perigosa else 'Não'}")
        linhas.append(f"\n--- Conservação Física ---")
        linhas.append(f"  Erro de energia: {self.erro_energia_relativo:.2e}")
        linhas.append(f"  Erro de momento angular: {self.erro_momento_angular:.2e}")
        linhas.append(f"  Física válida: {'Sim' if self.fisica_valida() else 'NÃO'}")
        linhas.append(f"\n{sep}")
        return "\n".join(linhas)

    def __str__(self) -> str:
        status = "COLISÃO" if self.houve_colisao else "sem colisão"
        return f"ResultadoSimulacao({status}, dist_min={self.distancia_minima / 1000:.0f} km, erro_E={self.erro_energia_relativo:.2e})"

    def __repr__(self) -> str:
        return f"ResultadoSimulacao(houve_colisao={self.houve_colisao}, passos={self.numero_passos}, fisica_valida={self.fisica_valida()})"
