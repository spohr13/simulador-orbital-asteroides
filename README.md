# 🚀 Simulador Orbital de Asteroides v2.0

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0-orange.svg)](https://github.com/seu-usuario/simulador-orbital)

Uma ferramenta modular e extensível para simulação de dinâmica orbital, detecção de colisões e análise de risco de impacto de asteroides.

## ✨ Características Principais

- **🏗️ Arquitetura Modular**: Código organizado em módulos especializados
- **🌍 Múltiplos Cenários**: 7+ cenários pré-configurados (Sistema Solar, Apophis, etc.)
- **🔬 Física Precisa**: Integração Runge-Kutta 4ª ordem com conservação de energia
- **💥 Detecção de Colisão**: Sistema avançado de detecção e análise de impacto
- **📊 Visualização Avançada**: Gráficos, animações e relatórios detalhados
- **⚙️ Configuração Flexível**: Sistema de configuração personalizável
- **🧪 Testes Abrangentes**: Cobertura completa de testes automatizados

## 🚀 Instalação Rápida

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/simulador-orbital.git
cd simulador-orbital

# Instalar dependências
pip install -r requirements.txt

# Executar testes
python test_simulator_v2.py
```

## 📖 Uso Básico

### Exemplo Simples
```python
from __init__ import *

# Executar exemplo rápido
sistema, resultado = exemplo_rapido()
print(f"Física válida: {resultado.fisica_valida()}")
```

### Cenários Pré-configurados
```python
from scenarios import *

# Sistema Solar Básico
sistema = criar_sistema_solar_basico()

# Cenário de Impacto
sistema = criar_sistema_impacto_direto()

# Asteroide Apophis
sistema = criar_sistema_apophis()

# Simular
resultado = sistema.simular(1.0 * ANOS_EM_SEGUNDOS, progresso=True)
```

### Interface de Linha de Comando
```bash
# Demonstração
python main.py --demo

# Cenário específico
python main.py --cenario apophis --tempo 2.0 --progresso

# Modo interativo
python main.py --interativo
```

## 🏗️ Estrutura do Projeto

```
simulador-orbital/
├── constants.py              # Constantes físicas
├── celestial_body.py        # Classe CorpoCeleste
├── simulation_result.py     # Classe ResultadoSimulacao
├── gravitational_system.py  # Classe SistemaGravitacional
├── scenarios.py             # Cenários pré-configurados
├── utils.py                 # Funções utilitárias
├── main.py                  # Ponto de entrada principal
├── config.py                # Configurações do sistema
├── __init__.py              # Módulo principal
├── test_simulator_v2.py     # Testes automatizados
├── exemplo_uso.py           # Exemplos de uso
├── requirements.txt         # Dependências
└── README.md               # Este arquivo
```

## 🎯 Cenários Disponíveis

| Cenário | Descrição | Uso |
|---------|-----------|-----|
| `sistema_solar_basico` | Sol, Terra, Lua | Órbitas básicas |
| `impacto_direto` | Asteroide em rota de colisão | Análise de impacto |
| `apophis` | Asteroide Apophis real | Estudos científicos |
| `sistema_solar_completo` | Todos os planetas | Simulações complexas |
| `asteroide_personalizado` | Parâmetros customizáveis | Pesquisa específica |
| `teste_conservacao` | Sistema simples | Validação física |
| `multi_asteroides` | Múltiplos asteroides | Análise estatística |

## 📊 Exemplos de Uso

### Análise de Impacto
```python
# Criar cenário de impacto
sistema = criar_sistema_impacto_direto(
    massa_asteroide=1e11,  # 100 milhões de toneladas
    distancia_inicial=R_TERRA * 20,  # 20 raios terrestres
    velocidade_aproximacao=25000  # 25 km/s
)

# Simular
resultado = sistema.simular(0.1 * ANOS_EM_SEGUNDOS, progresso=True)

# Analisar resultados
if resultado.houve_colisao:
    print(f"Energia de impacto: {resultado.equivalente_tnt:.2f} megatons TNT")
    print(f"Raio da cratera: {resultado.raio_cratera/1000:.2f} km")
```

### Visualização
```python
from utils import plotar_trajetorias, plotar_distancia_tempo

# Plotar trajetórias
plotar_trajetorias(sistema, "Trajetórias dos Corpos")

# Plotar distância vs tempo
plotar_distancia_tempo(sistema, "Terra", "Asteroide")
```

### Salvamento de Resultados
```python
from utils import salvar_simulacao

# Salvar simulação completa
diretorio = salvar_simulacao(sistema, resultado)
print(f"Resultados salvos em: {diretorio}")
```

## 🧪 Testes

```bash
# Executar todos os testes
python test_simulator_v2.py

# Executar exemplo completo
python exemplo_uso.py

# Teste específico
python -c "from test_simulator_v2 import executar_teste_basico; executar_teste_basico()"
```

## ⚙️ Configuração

### Configurações Básicas
```python
from config import ConfigPadrao

# Usar configuração padrão
config = ConfigPadrao()

# Personalizar configurações
config.SIMULACAO.DT_PADRAO = 1800  # 30 minutos
config.VISUALIZACAO.FIGURA_PADRAO = (15, 10)
```

### Arquivo de Configuração
```json
{
  "simulacao": {
    "dt_padrao": 3600,
    "tempo_padrao": 0.1,
    "mostrar_progresso": true
  },
  "visualizacao": {
    "figura_tamanho": [12, 8],
    "linha_espessura": 2
  }
}
```

## 🔬 Física Implementada

- **Gravitação Universal**: Lei de Newton com constante G
- **Integração Numérica**: Runge-Kutta 4ª ordem
- **Conservação de Energia**: Verificação automática
- **Conservação do Momento Angular**: Validação contínua
- **Detecção de Colisão**: Múltiplos critérios físicos
- **Cálculos de Impacto**: Energia, cratera, TNT equivalente

## 📈 Performance

- **Simulações Rápidas**: Otimizado para performance
- **Memória Eficiente**: Gerenciamento inteligente de dados
- **Paralelização**: Suporte para múltiplos núcleos (futuro)
- **Cache**: Armazenamento de cálculos repetitivos

## 🤝 Contribuindo

1. **Fork** o projeto
2. **Crie** uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra** um Pull Request

### Adicionando Novos Cenários
```python
# Em scenarios.py
def meu_novo_cenario():
    sistema = SistemaGravitacional(dt=DT_PADRAO, nome="Meu Cenário")
    # ... configuração ...
    return sistema
```

### Adicionando Novas Análises
```python
# Em utils.py
def minha_analise_personalizada(sistema, resultado):
    # ... implementar análise ...
    return dados_analise
```

## 📚 Documentação

- [Guia Completo](README_v2.md) - Documentação detalhada
- [Estrutura Modular](ESTRUTURA_v2.md) - Arquitetura do projeto
- [Exemplos de Uso](exemplo_uso.py) - Casos práticos
- [API Reference](docs/api.md) - Referência da API

## 🐛 Reportando Bugs

Encontrou um bug? Abra uma [issue](https://github.com/seu-usuario/simulador-orbital/issues) com:

- Descrição do problema
- Passos para reproduzir
- Versão do Python
- Sistema operacional

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Autores

- **Assistente IA** - *Desenvolvimento inicial* - [GitHub](https://github.com/assistente-ia)
- **Seu Nome** - *Contribuições* - [GitHub](https://github.com/seu-usuario)

## 🙏 Agradecimentos

- Comunidade Python
- Projetos de código aberto
- Contribuidores do projeto

---

**Simulador Orbital de Asteroides v2.0** - Modular, Extensível e Poderoso! 🚀

[⭐ Dê uma estrela](https://github.com/seu-usuario/simulador-orbital) se este projeto te ajudou!
