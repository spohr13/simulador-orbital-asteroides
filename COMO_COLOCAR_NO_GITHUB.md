# 🚀 Como Colocar o Projeto no GitHub

## 📋 Pré-requisitos

1. **Conta no GitHub**: Crie uma conta em [github.com](https://github.com)
2. **Git instalado**: Verifique com `git --version`
3. **Projeto organizado**: ✅ Já feito!

## 🔧 Passo a Passo

### 1. **Criar Repositório no GitHub**

1. Acesse [github.com](https://github.com) e faça login
2. Clique no botão **"New"** ou **"+"** → **"New repository"**
3. Preencha os dados:
   - **Repository name**: `simulador-orbital-asteroides`
   - **Description**: `Simulador Orbital de Asteroides v2.0 - Modular e Extensível`
   - **Visibility**: Public (recomendado) ou Private
   - **Initialize**: ❌ NÃO marque (já temos arquivos)
4. Clique em **"Create repository"**

### 2. **Conectar Repositório Local ao GitHub**

```bash
# No terminal, dentro da pasta do projeto:
cd /Users/valentinaspohr/Desktop/tudo/unicamp/2s:2025/F625

# Adicionar o repositório remoto (substitua SEU_USUARIO)
git remote add origin https://github.com/SEU_USUARIO/simulador-orbital-asteroides.git

# Verificar se foi adicionado
git remote -v
```

### 3. **Fazer o Primeiro Push**

```bash
# Renomear branch para 'main' (padrão atual)
git branch -M main

# Fazer push para o GitHub
git push -u origin main
```

### 4. **Verificar no GitHub**

1. Acesse seu repositório no GitHub
2. Verifique se todos os arquivos estão lá
3. O README.md deve aparecer automaticamente na página inicial

## 🎯 Comandos Resumidos

```bash
# 1. Inicializar (já feito)
git init
git add .
git commit -m "Initial commit: Simulador Orbital v2.0"

# 2. Conectar ao GitHub
git remote add origin https://github.com/SEU_USUARIO/simulador-orbital-asteroides.git

# 3. Enviar para o GitHub
git branch -M main
git push -u origin main
```

## 🔄 Comandos para Futuras Atualizações

```bash
# Adicionar mudanças
git add .

# Fazer commit
git commit -m "Descrição das mudanças"

# Enviar para o GitHub
git push origin main
```

## 📁 Estrutura que Será Enviada

```
simulador-orbital-asteroides/
├── .gitignore              # Arquivos ignorados
├── LICENSE                 # Licença MIT
├── README.md               # Documentação principal
├── README_v2.md            # Documentação detalhada
├── ESTRUTURA_v2.md         # Guia da estrutura
├── COMO_TESTAR.md          # Guia de testes v1.0
├── COMO_COLOCAR_NO_GITHUB.md # Este arquivo
├── requirements.txt        # Dependências
├── __init__.py             # Módulo principal
├── constants.py            # Constantes físicas
├── celestial_body.py       # Classe CorpoCeleste
├── simulation_result.py    # Classe ResultadoSimulacao
├── gravitational_system.py # Classe SistemaGravitacional
├── scenarios.py            # Cenários pré-configurados
├── utils.py                # Funções utilitárias
├── main.py                 # Ponto de entrada principal
├── config.py               # Configurações do sistema
├── test_simulator_v2.py    # Testes automatizados
├── exemplo_uso.py          # Exemplos de uso
├── asteroid_simulator_fixed.py # Código original v1.0
└── test_asteroid_simulator.py  # Testes v1.0
```

## 🎨 Personalizações Recomendadas

### 1. **Badges no README**
Adicione badges ao seu README.md:

```markdown
[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0-orange.svg)](https://github.com/seu-usuario/simulador-orbital)
```

### 2. **Topics no GitHub**
Adicione topics relevantes:
- `python`
- `astronomy`
- `physics`
- `simulation`
- `orbital-mechanics`
- `asteroids`
- `numpy`
- `matplotlib`

### 3. **Descrição do Repositório**
```
Simulador Orbital de Asteroides v2.0 - Ferramenta modular para simulação de dinâmica orbital, detecção de colisões e análise de risco de impacto
```

## 🚀 Próximos Passos

### 1. **Configurar GitHub Pages** (Opcional)
- Vá em Settings → Pages
- Escolha source: Deploy from a branch
- Branch: main
- Pasta: / (root)

### 2. **Adicionar Issues Template**
Crie `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
---
name: Bug report
about: Create a report to help us improve
title: ''
labels: bug
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. macOS, Windows, Linux]
 - Python version: [e.g. 3.8.5]
 - Version: [e.g. 2.0]

**Additional context**
Add any other context about the problem here.
```

### 3. **Adicionar Contributing Guide**
Crie `CONTRIBUTING.md`:

```markdown
# Contributing to Simulador Orbital

## How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Development Setup

```bash
git clone https://github.com/seu-usuario/simulador-orbital.git
cd simulador-orbital
pip install -r requirements.txt
python test_simulator_v2.py
```

## Code Style

- Follow PEP 8
- Use type hints
- Add docstrings
- Write tests for new features
```

## 🎉 Resultado Final

Após seguir todos os passos, você terá:

- ✅ Repositório público no GitHub
- ✅ README.md profissional
- ✅ Estrutura modular organizada
- ✅ Documentação completa
- ✅ Licença MIT
- ✅ Arquivos de configuração
- ✅ Testes automatizados

## 🔗 Links Úteis

- [GitHub Docs](https://docs.github.com/)
- [Git Tutorial](https://git-scm.com/docs/gittutorial)
- [Markdown Guide](https://www.markdownguide.org/)
- [Python Packaging](https://packaging.python.org/)

---

**Boa sorte com seu projeto no GitHub! 🚀**
