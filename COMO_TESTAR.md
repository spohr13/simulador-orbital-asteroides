# Como Testar o Simulador Orbital de Asteroides

Este guia explica como testar o código do simulador orbital de asteroides com detecção de colisão melhorada.

## Pré-requisitos

- Python 3.6 ou superior
- Bibliotecas: `numpy`, `matplotlib`
- Arquivo: `asteroid_simulator_fixed.py`

## Métodos de Teste

### 1. **Teste Automático Completo** (Recomendado)

Execute o script de teste organizado:

```bash
python3 test_asteroid_simulator.py
```

Este script executa uma bateria completa de testes:
- Funcionalidades básicas
- Detecção de colisão
- Cenário Apophis
- Conservação de energia
- Demonstração completa

### 2. **Testes Individuais**

#### Teste Básico
```python
python3 -c "
from asteroid_simulator_fixed import *
sistema = SistemaGravitacional()
print('Sistema criado com sucesso!')
"
```

#### Teste de Detecção de Colisão
```python
python3 -c "
from asteroid_simulator_fixed import *
resultado = teste_deteccao_colisao()
print('Teste de colisão concluído!')
"
```

#### Teste do Cenário Apophis
```python
python3 -c "
from asteroid_simulator_fixed import *
sistema = criar_sistema_apophis_melhorado()
resultado = sistema.simular(1.0 * ANOS_EM_SEGUNDOS, progresso=False)
print('Teste Apophis concluído!')
"
```

#### Demonstração Completa
```python
python3 -c "
from asteroid_simulator_fixed import *
demonstrar_deteccao_melhorada()
exemplo_completo_colisao()
"
```

### 3. **Testes Interativos no Python**

```python
# Abrir Python interativo
python3

# Importar o módulo
from asteroid_simulator_fixed import *

# Criar sistema personalizado
sistema = SistemaGravitacional(dt=1800)  # 30 min

# Adicionar corpos
sol = CorpoCeleste('Sol', M_SOL, [0,0,0], [0,0,0], 'yellow', 20)
terra = CorpoCeleste('Terra', M_TERRA, [UA,0,0], [0,29780,0], 'blue', 10)
asteroide = CorpoCeleste('Asteroide', 1e11, [UA*1.1,0,0], [-5000,25000,0], 'red', 5)

sistema.adicionar_corpo(sol)
sistema.adicionar_corpo(terra)
sistema.adicionar_corpo(asteroide)

# Executar simulação
resultado = sistema.simular(0.1 * ANOS_EM_SEGUNDOS, progresso=True)

# Ver resultados
print(f"Colisão: {resultado.houve_colisao}")
print(f"Distância mínima: {resultado.distancia_minima/1000:.2f} km")
```

## Interpretando os Resultados

### **Testes Bem-sucedidos**
- **Energia conservada**: Erro relativo < 1e-6
- **Momento angular conservado**: Erro relativo < 1e-6
- **Detecção de colisão**: Funciona corretamente
- **Aproximação perigosa**: Detectada quando apropriado

### **Possíveis Problemas**
- **Violação de energia**: Verificar passo de tempo (dt)
- **Erro de importação**: Verificar se todas as bibliotecas estão instaladas
- **Simulação muito lenta**: Reduzir tempo de simulação ou aumentar dt

## Configurações de Teste

### Parâmetros Recomendados

```python
# Para testes rápidos
dt = 3600        # 1 hora
tempo = 0.1      # 0.1 anos

# Para testes precisos
dt = 900         # 15 minutos
tempo = 1.0      # 1 ano

# Para testes de colisão
dt = 300         # 5 minutos
tempo = 0.05     # 0.05 anos
```

### Cenários de Teste

1. **Impacto Direto**: `criar_sistema_impacto_melhorado()`
2. **Apophis**: `criar_sistema_apophis_melhorado()`
3. **Sistema Personalizado**: Criar manualmente

## Visualização (Opcional)

Se matplotlib estiver disponível, os testes incluem gráficos automáticos:

```python
# Habilitar visualização
import matplotlib.pyplot as plt
plt.show()  # Mostrar gráficos
```

## Solução de Problemas

### Erro: "ModuleNotFoundError"
```bash
pip install numpy matplotlib
```

### Erro: "Simulação muito lenta"
```python
# Reduzir precisão para teste rápido
sistema = SistemaGravitacional(dt=7200)  # 2 horas
resultado = sistema.simular(0.01 * ANOS_EM_SEGUNDOS)  # 3.65 dias
```

### Erro: "Violação de energia"
```python
# Usar passo menor
sistema = SistemaGravitacional(dt=1800)  # 30 min
```

## Relatórios de Teste

O script `test_asteroid_simulator.py` gera um relatório completo:

```
Resumo: 5/5 testes passaram
TODOS OS TESTES PASSARAM! O simulador está funcionando corretamente.
```

## Próximos Passos

Após executar os testes com sucesso, você pode:

1. **Modificar parâmetros**: Alterar massas, posições, velocidades
2. **Adicionar corpos**: Lua, outros planetas, múltiplos asteroides
3. **Personalizar cenários**: Criar situações específicas
4. **Analisar resultados**: Estudar trajetórias e parâmetros de impacto

---

**Dica**: Execute sempre `python3 test_asteroid_simulator.py` primeiro para verificar se tudo está funcionando corretamente!
