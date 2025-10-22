# Simulador Orbital de Asteroides v2.0

## Visão Geral

O Simulador Orbital de Asteroides v2.0 é uma versão completamente reestruturada e modular do simulador original. Esta versão oferece maior flexibilidade, extensibilidade e facilidade de manutenção.

## Arquitetura Modular

### Estrutura de Arquivos

```
simulador_v2/
├── constants.py              # Constantes físicas e configurações
├── celestial_body.py       # Classe CorpoCeleste
├── simulation_result.py     # Classe ResultadoSimulacao
├── gravitational_system.py  # Classe SistemaGravitacional
├── scenarios.py            # Cenários pré-configurados
├── utils.py                # Funções utilitárias
├── main.py                 # Ponto de entrada principal
├── test_simulator_v2.py    # Testes automatizados
└── README_v2.md           # Esta documentação
```

### Componentes Principais

#### 1. **constants.py** - Constantes e Configurações
- Constantes físicas fundamentais (G, massas, raios)
- Unidades astronômicas e conversões
- Configurações de simulação
- Parâmetros de detecção de colisão
- Cores e tamanhos para visualização

#### 2. **celestial_body.py** - Corpo Celeste
- Representa um corpo celeste no sistema
- Cálculos físicos (energia, momento angular, órbitas)
- Histórico de trajetória
- Métodos de análise orbital

#### 3. **simulation_result.py** - Resultado da Simulação
- Encapsula todos os resultados
- Parâmetros de impacto e cratera
- Validação física (conservação de energia/momento)
- Geração de relatórios (texto e JSON)

#### 4. **gravitational_system.py** - Sistema Gravitacional
- Gerencia múltiplos corpos
- Cálculo de forças gravitacionais
- Integração numérica (Runge-Kutta 4ª ordem)
- Detecção de colisões e aproximações
- Simulação temporal

#### 5. **scenarios.py** - Cenários Pré-configurados
- Sistema solar básico
- Cenários de impacto
- Asteroide Apophis
- Sistema solar completo
- Cenários personalizáveis

#### 6. **utils.py** - Funções Utilitárias
- Conversões de unidades
- Cálculos orbitais
- Visualização (gráficos e animações)
- Salvamento e carregamento de simulações
- Validação de sistemas

#### 7. **main.py** - Ponto de Entrada
- Interface de linha de comando
- Modo interativo
- Demonstrações
- Execução de cenários

## Funcionalidades Principais

### Simulação Física
- **Integração numérica**: Runge-Kutta 4ª ordem
- **Conservação de energia**: Verificação automática
- **Conservação do momento angular**: Validação contínua
- **Detecção de colisão**: Múltiplos critérios
- **Cálculos de impacto**: Energia, cratera, TNT equivalente

### Cenários Disponíveis
1. **Sistema Solar Básico**: Sol, Terra, Lua
2. **Impacto Direto**: Asteroide em rota de colisão
3. **Apophis**: Asteroide real com parâmetros orbitais
4. **Sistema Solar Completo**: Todos os planetas principais
5. **Asteroide Personalizado**: Parâmetros customizáveis
6. **Teste de Conservação**: Sistema simples para validação
7. **Multi-Asteroides**: Múltiplos asteroides

### Visualização
- **Trajetórias 2D**: Plotagem das órbitas
- **Distância vs Tempo**: Evolução da proximidade
- **Energia vs Tempo**: Conservação de energia
- **Animações**: Visualização dinâmica

### Análise de Resultados
- **Relatórios detalhados**: Texto e JSON
- **Classificação de impactos**: Por energia
- **Parâmetros de cratera**: Dimensões estimadas
- **Validação física**: Conservação de leis fundamentais

## Como Usar

### Instalação
```bash
# Instalar dependências
pip install numpy matplotlib

# Verificar instalação
python test_simulator_v2.py
```

### Uso Básico

#### 1. **Modo Simples**
```python
from scenarios import criar_sistema_impacto_direto
from main import exemplo_completo_colisao

# Executar exemplo completo
sistema, resultado = exemplo_completo_colisao()
```

#### 2. **Modo Interativo**
```bash
python main.py --interativo
```

#### 3. **Linha de Comando**
```bash
# Cenário específico
python main.py --cenario apophis --tempo 2.0 --progresso

# Demonstração
python main.py --demo

# Testes
python main.py --teste
```

### Programação Avançada

#### Criar Sistema Personalizado
```python
from celestial_body import CorpoCeleste
from gravitational_system import SistemaGravitacional

# Criar sistema
sistema = SistemaGravitacional(dt=1800, nome="Meu Sistema")

# Adicionar corpos
sol = CorpoCeleste("Sol", M_SOL, [0,0,0], [0,0,0])
terra = CorpoCeleste("Terra", M_TERRA, [UA,0,0], [0,29780,0])

sistema.adicionar_corpo(sol)
sistema.adicionar_corpo(terra)

# Simular
resultado = sistema.simular(1.0 * ANOS_EM_SEGUNDOS)
```

#### Análise de Resultados
```python
# Verificar conservação
if resultado.fisica_valida():
    print("Física válida!")

# Classificar impacto
if resultado.houve_colisao:
    print(f"Tipo de impacto: {resultado.classificar_impacto()}")
    print(f"Energia: {resultado.equivalente_tnt:.2f} megatons TNT")

# Gerar relatório
print(resultado.gerar_relatorio())
```

#### Visualização
```python
from utils import plotar_trajetorias, plotar_distancia_tempo

# Plotar trajetórias
plotar_trajetorias(sistema, "Minhas Trajetórias")

# Plotar distância vs tempo
plotar_distancia_tempo(sistema, "Terra", "Asteroide")
```

## Extensibilidade

### Adicionar Novos Cenários
```python
def meu_cenario_personalizado():
    sistema = SistemaGravitacional(dt=DT_PADRAO, nome="Meu Cenário")
    
    # Configurar corpos
    # ... código do cenário ...
    
    return sistema
```

### Adicionar Novos Tipos de Corpos
```python
# Criar corpo com tipo personalizado
asteroide = CorpoCeleste(
    nome="Meu Asteroide",
    massa=1e10,
    posicao=[UA*1.1, 0, 0],
    velocidade=[-5000, 25000, 0],
    tipo="Asteroide_Personalizado"
)
```

### Adicionar Novas Análises
```python
def minha_analise(sistema, resultado):
    # Implementar análise personalizada
    pass
```

## Testes

### Executar Todos os Testes
```bash
python test_simulator_v2.py
```

### Testes Específicos
```python
# Teste individual
from test_simulator_v2 import executar_teste_basico
executar_teste_basico()
```

## Vantagens da v2.0

### 1. **Modularidade**
- Código organizado em módulos especializados
- Fácil manutenção e extensão
- Reutilização de componentes

### 2. **Flexibilidade**
- Múltiplos cenários pré-configurados
- Parâmetros customizáveis
- Interface de linha de comando

### 3. **Extensibilidade**
- Fácil adição de novos cenários
- Novos tipos de corpos celestes
- Análises personalizadas

### 4. **Robustez**
- Validação de sistemas
- Tratamento de erros
- Testes automatizados

### 5. **Usabilidade**
- Interface interativa
- Documentação completa
- Exemplos práticos

## Comparação com v1.0

| Aspecto | v1.0 | v2.0 |
|---------|------|------|
| Estrutura | Monolítica | Modular |
| Cenários | 3 fixos | 7+ configuráveis |
| Interface | Apenas código | CLI + Interativo |
| Testes | Básicos | Completos |
| Documentação | Mínima | Completa |
| Extensibilidade | Limitada | Alta |

## Próximos Passos

### Funcionalidades Planejadas
1. **Simulação 3D**: Visualização tridimensional
2. **Efeitos Relativísticos**: Correções de Einstein
3. **Perturbações Planetárias**: Influência de outros planetas
4. **Banco de Dados**: Asteroides reais catalogados
5. **Interface Gráfica**: GUI desktop/web

### Contribuições
- Adicionar novos cenários
- Implementar novas análises
- Melhorar visualizações
- Otimizar performance
- Adicionar testes

## Suporte

Para dúvidas ou problemas:
1. Verificar se todos os módulos estão importados corretamente
2. Executar `python test_simulator_v2.py` para verificar funcionamento
3. Consultar a documentação dos módulos específicos
4. Verificar se as dependências estão instaladas

---

**Simulador Orbital de Asteroides v2.0** - Uma ferramenta poderosa e flexível para análise de dinâmica orbital e detecção de colisões.
