# Simulador Orbital de Asteroides

Ferramenta modular em Python para simulação de dinâmica orbital, detecção de colisões e análise de risco de impacto de asteroides. Utiliza integração numérica Runge-Kutta de 4ª ordem com verificação de conservação de energia e momento angular.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-v2.0-brightgreen)

---

## Sobre o Projeto

Este simulador foi desenvolvido como projeto de física computacional para modelar interações gravitacionais entre corpos celestes, com foco especial na análise de risco de impacto de asteroides com a Terra.

O sistema implementa gravitação Newtoniana com integração RK4, 7 cenários pré-configurados (incluindo Sistema Solar, Apophis e impactos diretos), detecção de colisão avançada com cálculo de cratera (baseado em Melosh, 1989), interface web (Flask) e CLI com modo interativo, e validação física automática.

## Instalação
```bash
git clone https://github.com/spohr13/simulador-orbital-asteroides.git
cd simulador-orbital-asteroides
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Uso Rápido

### Linha de Comando
```bash
python main.py --demo
python main.py --cenario impacto_direto --tempo 0.1 --progresso
python main.py --cenario apophis --tempo 2.0 --progresso --plotar
python main.py --interativo
```

### Python
```python
from scenarios import criar_sistema_impacto_direto
from constants import ANOS_EM_SEGUNDOS

sistema = criar_sistema_impacto_direto(
    massa_asteroide=1e11,
    distancia_inicial=6.371e6 * 20,
    velocidade_aproximacao=25000
)
resultado = sistema.simular(0.1 * ANOS_EM_SEGUNDOS, progresso=True)

if resultado.houve_colisao:
    print(f"Energia: {resultado.equivalente_tnt:.2f} megatons TNT")
    print(f"Cratera: {resultado.diametro_cratera/1000:.2f} km")
```

### Interface Web
```bash
python app.py
# Acesse http://localhost:5000
```

## Cenários Disponíveis

| Cenário | Descrição | Tempo sugerido |
|---------|-----------|---------------|
| `sistema_solar_basico` | Sol + Terra + Lua | 1.0 ano |
| `impacto_direto` | Asteroide em rota de colisão | 0.1 ano |
| `apophis` | Asteroide Apophis (dados reais) | 2.0 anos |
| `sistema_solar_completo` | Sol + 5 planetas | 1.0 ano |
| `teste_conservacao` | Sol + Terra (validação) | 1.0 ano |
| `multi_asteroides` | N asteroides simultâneos | 0.5 ano |

## Física Implementada

O simulador usa Runge-Kutta de 4ª ordem (RK4) para resolver o problema gravitacional de N-corpos (F = G x m1 x m2 / r2). A cada passo temporal, calcula 4 estimativas de derivada (k1-k4) para obter precisão O(dt4), com verificação automática de conservação de energia.

A detecção de colisão usa três critérios simultâneos: colisão física (distância entre superfícies <= 0), aproximação perigosa (distância < 10 raios terrestres com velocidade radial negativa), e rastreamento contínuo da menor separação.

Quando uma colisão é detectada, calcula energia cinética de impacto (Joules e megatons TNT), diâmetro e profundidade da cratera, e classificação da cratera (simples, complexa, anel central), baseado em Melosh (1989) e Collins et al. (2005).

## Deploy

O projeto está configurado para deploy em Render ou Heroku:
```bash
# Render (usar render.yaml)
# Heroku
heroku create simulador-orbital
git push heroku main
```

## Licença

MIT License — veja [LICENSE](LICENSE) para detalhes.

## Referências

- Melosh, H.J. (1989). *Impact Cratering: A Geologic Process*. Oxford University Press.
- Collins, G.S. et al. (2005). *Earth Impact Effects Program*. Meteoritics & Planetary Science.
- Murray, C.D. & Dermott, S.F. (1999). *Solar System Dynamics*. Cambridge University Press.
