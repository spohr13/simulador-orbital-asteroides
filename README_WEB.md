# 🌌 Interface Web - Simulador Orbital de Asteroides

Uma interface web moderna e interativa para o simulador orbital de asteroides, desenvolvida com Flask e Bootstrap.

## 🚀 Características

- **Interface Moderna**: Design responsivo com Bootstrap 5
- **Simulação Interativa**: Configure parâmetros e execute simulações em tempo real
- **Visualização Avançada**: Gráficos interativos e animações
- **Múltiplos Cenários**: Impacto direto, Apophis 2029, Sistema Solar
- **Análise Detalhada**: Relatórios completos com parâmetros físicos
- **Histórico de Simulações**: Acompanhe todas as simulações realizadas

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Módulos do simulador orbital (asteroid_simulator_fixed.py, config.py, constants.py)
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

## 🛠️ Instalação

### Opção 1: Instalação Automática (Recomendada)
```bash
python install_web.py
```

### Opção 2: Instalação Manual

**Se você tem conflitos com qiskit-metal ou outras bibliotecas:**

1. **Instalar apenas dependências essenciais**:
   ```bash
   pip install -r requirements_minimal.txt
   ```

2. **Ou instalar apenas Flask**:
   ```bash
   pip install Flask
   ```

**Se não há conflitos de dependências:**

1. **Instalar todas as dependências**:
   ```bash
   pip install -r requirements_web.txt
   ```

### Verificar estrutura de arquivos:
   ```
   F625/
   ├── app.py                          # Aplicação Flask principal
   ├── templates/                      # Templates HTML
   │   ├── base.html
   │   ├── index.html
   │   ├── simulador.html
   │   └── resultados.html
   ├── static/                         # Arquivos estáticos
   │   ├── css/
   │   │   └── style.css
   │   └── js/
   │       └── main.js
   ├── asteroid_simulator_fixed.py     # Simulador principal
   ├── config.py                       # Configurações
   ├── constants.py                    # Constantes físicas
   └── requirements_web.txt            # Dependências
   ```

## 🎯 Como Usar

### 1. Iniciar o Servidor

```bash
python app.py
```

O servidor será iniciado em `http://localhost:5000`

### 2. Acessar a Interface

Abra seu navegador e acesse:
- **Página Principal**: `http://localhost:5000`
- **Simulador**: `http://localhost:5000/simulador`
- **Resultados**: `http://localhost:5000/resultados`

### 3. Executar Simulações

1. **Selecione um Cenário**:
   - **Impacto Direto**: Simula colisão garantida
   - **Apophis 2029**: Simula aproximação do asteroide Apophis
   - **Sistema Solar**: Simula Terra-Lua-Sol

2. **Configure Parâmetros**:
   - Tempo de simulação (anos)
   - Precisão (passo de tempo)
   - Parâmetros do asteroide (se aplicável)

3. **Execute a Simulação**:
   - Clique em "Executar Simulação"
   - Aguarde o processamento
   - Visualize os resultados

## 🎨 Interface

### Página Principal
- Visão geral dos recursos
- Cenários disponíveis
- Informações técnicas

### Simulador Interativo
- Formulário de configuração
- Parâmetros personalizáveis
- Execução em tempo real
- Visualização de resultados

### Resultados
- Lista de simulações realizadas
- Detalhes de cada simulação
- Gráficos interativos
- Relatórios detalhados

## 🔧 Configuração Avançada

### Variáveis de Ambiente

Crie um arquivo `.env` para configurações personalizadas:

```env
FLASK_ENV=development
FLASK_DEBUG=True
HOST=0.0.0.0
PORT=5000
```

### Configurações do Simulador

As configurações podem ser modificadas em `config.py`:

```python
# Passos de tempo disponíveis
DT_ULTRA_PRECISO = 300    # 5 minutos
DT_PRECISO = 900          # 15 minutos
DT_PADRAO = 3600          # 1 hora
DT_RAPIDO = 7200          # 2 horas

# Tempos de simulação
TEMPO_CURTO = 0.01        # 3.65 dias
TEMPO_MEDIO = 0.1         # 36.5 dias
TEMPO_LONGO = 1.0         # 1 ano
```

## 📊 Cenários Disponíveis

### 1. Impacto Direto
- **Objetivo**: Simular colisão garantida
- **Parâmetros**: Massa, distância inicial, velocidade
- **Análise**: Energia de impacto, cratera, consequências

### 2. Apophis 2029
- **Objetivo**: Simular aproximação real do Apophis
- **Parâmetros**: Órbitas reais, dados da NASA
- **Análise**: Aproximação próxima, parâmetro de impacto

### 3. Sistema Solar
- **Objetivo**: Simular dinâmica orbital básica
- **Parâmetros**: Terra, Lua, Sol
- **Análise**: Estabilidade orbital, conservação de energia

## 🎯 Recursos Técnicos

### Backend (Flask)
- **API RESTful**: Endpoints para simulação e dados
- **Processamento Assíncrono**: Simulações não bloqueiam interface
- **Validação de Dados**: Verificação de parâmetros de entrada
- **Geração de Gráficos**: Matplotlib para visualizações

### Frontend (HTML/CSS/JS)
- **Bootstrap 5**: Framework CSS responsivo
- **Chart.js**: Gráficos interativos
- **JavaScript Vanilla**: Sem dependências externas
- **Design Responsivo**: Funciona em desktop e mobile

### Simulador
- **Integração Numérica**: Runge-Kutta 4ª ordem
- **Detecção de Colisão**: Múltiplos critérios
- **Conservação de Energia**: Validação física
- **Parâmetros Físicos**: Constantes astronômicas reais

## 🐛 Solução de Problemas

### Conflitos de Dependências com qiskit-metal
```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed
```
**Soluções**:
1. **Use o instalador automático**: `python install_web.py`
2. **Instale apenas Flask**: `pip install Flask`
3. **Use requirements_minimal.txt**: `pip install -r requirements_minimal.txt`
4. **Crie ambiente virtual**: `python -m venv venv && source venv/bin/activate`

### Erro de Importação
```
ModuleNotFoundError: No module named 'asteroid_simulator_fixed'
```
**Solução**: Certifique-se de que todos os arquivos do simulador estão no mesmo diretório.

### Erro de Porta
```
Address already in use
```
**Solução**: Mude a porta no arquivo `app.py` ou mate o processo que está usando a porta 5000.

### Erro de Dependências
```
ImportError: No module named 'flask'
```
**Solução**: Instale as dependências com `pip install -r requirements_minimal.txt`.

### Versões Incompatíveis
```
numpy version conflicts
```
**Solução**: A interface web funciona com as versões já instaladas. Use `requirements_minimal.txt`.

### Simulação Lenta
**Soluções**:
- Reduza o tempo de simulação
- Use passo de tempo maior (menos preciso)
- Verifique recursos do sistema

## 🚀 Deploy em Produção

### Usando Gunicorn

```bash
# Instalar gunicorn
pip install gunicorn

# Executar em produção
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Usando Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements_web.txt .
RUN pip install -r requirements_web.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 📈 Melhorias Futuras

- [ ] Simulações em tempo real com WebSockets
- [ ] Exportação de dados em CSV/JSON
- [ ] Animações 3D com Three.js
- [ ] Simulações em lote
- [ ] API para integração externa
- [ ] Sistema de usuários e autenticação
- [ ] Cache de simulações
- [ ] Paralelização de cálculos

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Suporte

Para suporte e dúvidas:
- Abra uma issue no GitHub
- Consulte a documentação do simulador
- Verifique os logs do servidor Flask

---

**Desenvolvido com ❤️ para educação e pesquisa científica**
