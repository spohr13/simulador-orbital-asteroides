# 🌌 Simulador Orbital de Asteroides v2.0

Um simulador orbital completo para análise de impactos de asteroides com **interface web interativa**, desenvolvido em Python com métodos numéricos avançados.

## 🚀 **Interface Web Disponível!**

**Acesse o simulador online:** `https://pattie-untreasonable-windedly.ngrok-free.dev`

### ✨ **Funcionalidades da Interface Web:**
- 🌐 **Acesso mundial** via ngrok
- 📱 **Interface responsiva** para desktop e mobile
- 🎯 **3 cenários de simulação** (Impacto Direto, Apophis 2029, Sistema Solar)
- ⚙️ **Parâmetros configuráveis** em tempo real
- 📊 **Gráficos interativos** e visualizações
- 📋 **Relatórios detalhados** com análise física
- 🔄 **Histórico de simulações** e comparações

## 🎯 **Como Usar a Interface Web**

### **Opção 1: Acesso Online (Recomendado)**
1. **Acesse:** `https://pattie-untreasonable-windedly.ngrok-free.dev`
2. **Configure** os parâmetros desejados
3. **Execute** a simulação
4. **Visualize** os resultados em tempo real

### **Opção 2: Executar Localmente**
```bash
# 1. Instalar dependências
python install_web.py

# 2. Iniciar servidor
python app.py

# 3. Acessar
# Local: http://localhost:5001
# Rede: http://10.0.111.149:5001
```

### **Opção 3: Script Simplificado**
```bash
# Interface completa com opções
python simulador_web.py
```

## 🏗️ **Arquitetura do Projeto**

### **Interface Web:**
- `app.py` - Aplicação Flask principal
- `templates/` - Páginas HTML responsivas
- `static/` - CSS e JavaScript customizados
- `simulador_web.py` - Script de gerenciamento

### **Simulador Core:**
- `asteroid_simulator_fixed.py` - Simulador principal
- `celestial_body.py` - Classes de corpos celestes
- `config.py` - Configurações do sistema
- `constants.py` - Constantes físicas

### **Deploy:**
- `Procfile` - Para Heroku
- `railway.json` - Para Railway
- `render.yaml` - Para Render
- `requirements.txt` - Dependências

## 🎮 **Cenários Disponíveis**

### 1. **Impacto Direto**
- Simula colisão garantida com asteroide
- Análise de energia de impacto
- Estimativa de cratera
- Parâmetros configuráveis

### 2. **Apophis 2029**
- Simula aproximação real do Apophis
- Parâmetros orbitais reais
- Análise de aproximação próxima
- Parâmetro de impacto

### 3. **Sistema Solar**
- Simula Terra-Lua-Sol
- Órbitas estáveis
- Conservação de energia
- Análise de estabilidade

## 🔧 **Configuração Avançada**

### **Parâmetros Configuráveis:**
- **Tempo de simulação:** 0.01 a 100 anos
- **Precisão:** 5 min a 2 horas por passo
- **Massa do asteroide:** 1e6 a 1e15 kg
- **Distância inicial:** 1 a 100 raios terrestres
- **Velocidade:** 1 a 100 km/s

### **Métodos Numéricos:**
- **Integração:** Runge-Kutta 4ª ordem
- **Detecção de colisão:** Múltiplos critérios
- **Validação:** Conservação de energia
- **Precisão:** Configurável

## 📊 **Recursos Técnicos**

### **Backend (Flask):**
- API RESTful para comunicação
- Processamento assíncrono
- Validação de dados
- Geração de gráficos

### **Frontend (HTML/CSS/JS):**
- Bootstrap 5 responsivo
- Chart.js para gráficos
- JavaScript modular
- Design moderno

### **Física:**
- Constantes astronômicas reais
- Integração numérica precisa
- Detecção de colisão avançada
- Análise de parâmetros de impacto

## 🌐 **Acesso Remoto**

### **Rede Local:**
- URL: `http://10.0.111.149:5001`
- Para pessoas na mesma WiFi
- Acesso imediato

### **Internet (ngrok):**
- URL: `https://pattie-untreasonable-windedly.ngrok-free.dev`
- Para qualquer lugar do mundo
- Túnel seguro

### **Deploy Permanente:**
- Heroku, Railway, Render
- URLs permanentes
- Disponível 24/7

## 🚀 **Deploy em Produção**

### **Heroku:**
```bash
heroku create seu-simulador-orbital
git push heroku main
```

### **Railway:**
1. Acesse: https://railway.app
2. Conecte repositório GitHub
3. Deploy automático

### **Render:**
1. Acesse: https://render.com
2. Conecte repositório GitHub
3. Configure serviço web

## 📱 **Como Compartilhar**

### **Mensagem para Enviar:**
```
🌌 Simulador Orbital de Asteroides
🔗 https://pattie-untreasonable-windedly.ngrok-free.dev

✨ Funcionalidades:
- 3 cenários de simulação
- Parâmetros configuráveis
- Gráficos interativos
- Relatórios detalhados

🌍 Acesse de qualquer lugar!
```

## 🎉 **Status Atual**

- ✅ **Interface Web:** Funcionando
- ✅ **ngrok:** Ativo e acessível
- ✅ **Servidor:** Rodando na porta 5001
- ✅ **Deploy:** Configurado para produção
- ✅ **Documentação:** Completa

## 📚 **Documentação Adicional**

- `README_WEB.md` - Documentação da interface web
- `COMO_USAR_WEB.md` - Guia de uso rápido
- `test_web.py` - Testes da interface

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 **Licença**

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**Desenvolvido com ❤️ para educação e pesquisa científica**

**Acesse agora:** `https://pattie-untreasonable-windedly.ngrok-free.dev` 🌟
