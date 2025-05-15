# 🧪 Teste Automatizado de Login em tribunais com Flask + Selenium

Este projeto permite testar automaticamente o funcionamento de formulários de login em tribunais diversos. A interface web é construída com Flask, e os testes são executados com Selenium WebDriver (Chrome).

## 🚀 Funcionalidades

- Interface web para inserir:
  - URL(s) de páginas de login
  - Usuário e senha
- Detecção automática de:
  - Campos de usuário e senha
  - Botão de login
  - Mensagens de erro e sucesso
- Suporte a páginas com `iframe`
- Resultados detalhados na tela com mensagens de sucesso ou falha

## 📂 Estrutura do Projeto

```
.
├── app.py                  # Aplicação Flask
├── selenium_login.py       # Função principal de teste com Selenium
├── templates/
│   └── index.html          # Página web com formulário e resultados
├── static/                 # Arquivos estáticos
```

## ⚙️ Requisitos

- Python 3.8+
- Google Chrome instalado
- ChromeDriver compatível com a versão do seu navegador

### Instalar dependências

```bash
pip install flask selenium
```

## 🛠️ Como rodar

1. **Configure o caminho do ChromeDriver (se necessário)**  
   No `selenium_login.py`, aponte para o caminho do seu `chromedriver.exe`.

2. **Inicie o servidor Flask**

```bash
python app.py
```

3. **Acesse no navegador:**

```
http://localhost:5000
```

4. **Insira as URLs, usuário e senha para testar.**

## 📌 Observações

- O Selenium pode rodar com ou sem interface gráfica.
- Funciona com sistemas de login simples. Logins com autenticação em múltiplas etapas (como CAPTCHA ou OTP) não são suportados.
- A função `testar_login` está preparada para identificar vários padrões de campos de login comuns.

## 🧑‍💻 Desenvolvido por

- Ana 💻✨
