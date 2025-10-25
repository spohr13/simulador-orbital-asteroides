# 🚀 Como Usar a Interface Web - Guia Rápido

## ✅ Instalação Concluída!

A interface web do simulador orbital foi instalada com sucesso e está funcionando!

## 🌐 Acessar a Interface

**URL:** http://localhost:5001

> **Nota:** A porta 5001 foi usada porque a porta 5000 estava ocupada.

## 🎯 Funcionalidades Principais

### 1. **Página Principal** (`/`)
- Visão geral dos recursos
- Cenários disponíveis
- Informações técnicas

### 2. **Simulador Interativo** (`/simulador`)
- Configure parâmetros de simulação
- Execute simulações em tempo real
- Visualize resultados instantaneamente

### 3. **Resultados** (`/resultados`)
- Histórico de simulações
- Gráficos detalhados
- Relatórios completos

## 🎮 Como Executar Simulações

1. **Acesse o Simulador**: http://localhost:5001/simulador

2. **Selecione um Cenário**:
   - **Impacto Direto**: Simula colisão garantida
   - **Apophis 2029**: Simula aproximação do asteroide Apophis
   - **Sistema Solar**: Simula Terra-Lua-Sol

3. **Configure Parâmetros**:
   - **Tempo de Simulação**: 0.01 a 100 anos
   - **Precisão**: 5 min a 2 horas por passo
   - **Parâmetros do Asteroide** (se aplicável)

4. **Execute**: Clique em "Executar Simulação"

5. **Visualize**: Veja gráficos e relatórios detalhados

## 🔧 Comandos Úteis

### Iniciar o Servidor
```bash
python app.py
```

### Parar o Servidor
- Pressione `Ctrl+C` no terminal

### Verificar se está Rodando
```bash
curl http://localhost:5001
```

### Mudar Porta
Edite o arquivo `app.py` na linha 321:
```python
app.run(debug=True, host='0.0.0.0', port=5002)  # Mude para 5002
```

## 🎨 Recursos da Interface

- ✅ **Design Responsivo**: Funciona em desktop e mobile
- ✅ **Gráficos Interativos**: Trajetórias e evolução temporal
- ✅ **Múltiplos Cenários**: 3 cenários pré-configurados
- ✅ **Parâmetros Personalizáveis**: Controle total sobre a simulação
- ✅ **Relatórios Detalhados**: Análise física completa
- ✅ **Histórico de Simulações**: Acompanhe todas as execuções

## 🐛 Solução de Problemas

### Servidor não Inicia
```bash
# Verificar se a porta está livre
lsof -i :5001

# Usar porta diferente
python app.py
```

### Erro de Dependências
```bash
# Reinstalar dependências
python install_web.py
```

### Interface não Carrega
- Verifique se o servidor está rodando
- Acesse http://localhost:5001
- Verifique o console do navegador para erros

## 📊 Exemplos de Simulações

### Simulação Rápida (Impacto Direto)
1. Cenário: Impacto Direto
2. Tempo: 0.05 anos
3. Precisão: 15 min
4. Execute e veja a colisão!

### Simulação Realista (Apophis)
1. Cenário: Apophis 2029
2. Tempo: 2 anos
3. Precisão: 1 hora
4. Veja a aproximação próxima!

### Simulação Educativa (Sistema Solar)
1. Cenário: Sistema Solar
2. Tempo: 1 ano
3. Precisão: 2 horas
4. Observe as órbitas estáveis!

## 🎉 Pronto para Usar!

A interface web está funcionando perfeitamente. Aproveite para explorar diferentes cenários e parâmetros do simulador orbital!

---

**Desenvolvido com ❤️ para educação e pesquisa científica**
