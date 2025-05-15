from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def testar_login(url, username, password):
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')  
    options.add_argument('--remote-debugging-port=9222') 
    driver = webdriver.Chrome(options=options)
    resultado = {}

    try:
        print(f"Acessando: {url}")
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # iframe
        try:
            iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            print("iFrame encontrado, trocando para ele")
            driver.switch_to.frame(iframe)
        except Exception as e:
            print(f"ℹ Nenhum iframe encontrado ou erro ao alternar para o iFrame: {e}")

        # Campo de usuário
        campos_usuario = ["username", "login", "cpf", "cnpj", "CPF/CNPJ"]
        username_field = None
        for name in campos_usuario:
            try:
                username_field = wait.until(EC.presence_of_element_located((By.NAME, name)))
                break
            except:
                continue
        if not username_field:
            raise Exception("Campo de usuário não encontrado")

        # Campo de senha
        campos_senha = ["password", "senha"]
        password_field = None
        for name in campos_senha:
            try:
                password_field = wait.until(EC.presence_of_element_located((By.NAME, name)))
                break
            except:
                continue
        if not password_field:
            raise Exception("Campo de senha não encontrado")

        # Botão de login
        seletores_login = [
            (By.ID, "kc-login"),
            (By.ID, "btnEntrar"),
            (By.NAME, "login"),
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.XPATH, "//button[contains(text(), 'Entrar') or contains(text(), 'Login')]"),
        ]
        login_button = None
        for tipo, seletor in seletores_login:
            try:
                login_button = wait.until(EC.element_to_be_clickable((tipo, seletor)))
                break
            except:
                continue
        if not login_button:
            raise Exception("Botão de login não encontrado")

        print("Preenchendo dados e clicando")
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        
        def extrair_texto(elemento):
            texto = elemento.text.strip()
            if not texto:
                texto = elemento.get_attribute('innerText') or elemento.get_attribute('textContent')
                return texto.strip() if texto else ''

        print("⏳ Aguardando resposta da página...")

        # Verificação de sucesso
        seletores_sucesso = [
            (By.CLASS_NAME, "mat-button-wrapper"),
            (By.CLASS_NAME, "mat-button-focus-overlay"),
            (By.CLASS_NAME, "botao-menu"),
            (By.ID, "barraSuperiorPrincipal"),
            (By.ID, "menuPrincipal"),
            (By.ID, "j_id22"),
            (By.CSS_SELECTOR, "#barraSuperiorPrincipal > div > div.navbar-collapse > ul > li > a > span.hidden-xs.nome-sobrenome.tip-bottom"),
            (By.CSS_SELECTOR, "a[href*='logout']"),
            (By.CSS_SELECTOR, ".barraSuperiorPrincipal > div > div.navbar-header > ul"),
            (By.CSS_SELECTOR, ".barraSuperiorPrincipal > div > div.navbar-collapse > ul > li > a > span.avatar.tip-bottom > img")
        ]

        sucesso = False
        seletores_encontrados_sucesso = []
        mensagens_sucesso = []
        
        print("Verificando elementos de sucesso...")
        
        for tipo, seletor in seletores_sucesso:
            try:
                sucess_elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((tipo, seletor))
                )
                texto_sucesso = extrair_texto(sucess_elem)
                if texto_sucesso:
                    sucesso = True
                    seletores_encontrados_sucesso.append(f"{tipo} - {seletor}")
                    mensagens_sucesso.append(texto_sucesso)
                    print(f"✅ Sucesso detectado: {texto_sucesso} | Seletor: {tipo} - {seletor}")
            except Exception as e:
                print(f"❌ Erro ao tentar localizar seletor {tipo} - {seletor}: {e}")
                continue

        # Verificação de erro
        seletores_erro = [
            (By.CLASS_NAME, "kc-feedback-text"),
            (By.CLASS_NAME, "alert-danger"),
            (By.CLASS_NAME, "rich-messages-label"),
            (By.CLASS_NAME, "text-danger"),
            (By.ID, "mensagemErro"),
            (By.ID, "error-message"),
            (By.CSS_SELECTOR, ".kc-content-wrapper > div.text-danger > span"),
        ]

        erro_detectado = False
        seletores_encontrados_erro = []
        mensagens_erro = []

        if not sucesso:
            print("Verificando elementos de erro...")
            for tipo, seletor in seletores_erro:
                try:
                    erro_elem = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((tipo, seletor))
                    )
                    texto_erro = extrair_texto(erro_elem)
                    if texto_erro:
                        erro_detectado = True
                        seletores_encontrados_erro.append(f"{tipo} - {seletor}")
                        mensagens_erro.append(texto_erro)
                        print(f"⚠️ Erro detectado: {texto_erro} | Seletor: {tipo} - {seletor}")
                except Exception as e:
                    print(f"❌ Erro ao tentar localizar seletor {tipo} - {seletor}: {e}")
                    continue

        driver.switch_to.default_content()

        # Resultado final
        resultado["url"] = url
        if sucesso:
            resultado["resultado"] = "✅ Login bem-sucedido"
            resultado["seletores_sucesso_detectados"] = seletores_encontrados_sucesso
        elif erro_detectado:
            resultado["resultado"] = f"❌ Login falhou: {' / '.join(mensagens_erro)}"
            resultado["seletores_erro_detectados"] = seletores_encontrados_erro
        else:
            resultado["resultado"] = "❓ Resultado inconclusivo (sem indicadores claros)"

    except Exception as e:
        resultado["url"] = url
        resultado["resultado"] = f"⚠️ Erro ao testar login: {repr(e)}"
    finally:
        driver.quit()

    return resultado
