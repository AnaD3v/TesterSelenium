from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def testar_login(url, username, password):
    options = Options()
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    resultado = {}

    try:
        print(f"➡️ Acessando: {url}")
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Verificando e entrando em iframe (se houver)
        try:
            iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            print("✅ iFrame encontrado, trocando para ele")
            driver.switch_to.frame(iframe)
        except:
            print("ℹ️ Nenhum iframe encontrado")

        # Campo de usuário
        campos_usuario = ["username", "login", "cpf", "cnpj"]
        username_field = None
        for name in campos_usuario:
            try:
                username_field = wait.until(
                    EC.presence_of_element_located((By.NAME, name))
                )
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
                password_field = wait.until(
                    EC.presence_of_element_located((By.NAME, name))
                )
                break
            except:
                continue
        if not password_field:
            raise Exception("Campo de senha não encontrado")

        # Botão de login
        seletores_login = [
            (By.ID, "kc-login"),
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

        print("⏳ Aguardando resposta da página...")

        # Verificação de sucesso
        seletores_sucesso = [
            (By.CLASS_NAME, "dropdown menu-usuario"),
            (By.ID, "barraSuperiorPrincipal"),
            (By.ID, "menuPrincipal"),
            (By.ID, "atalhos"),
            (By.CSS_SELECTOR, "a[href*='logout']"),
        ]
        sucesso = False
        for tipo, seletor in seletores_sucesso:
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((tipo, seletor))
                )
                sucesso = True
                break
            except:
                continue

        # Verificação de erro por seletores
        seletores_erro = [
            (By.CLASS_NAME, "error"),
            (By.CLASS_NAME, "alert-danger"),
            (By.CLASS_NAME, "alert"),
            (By.CLASS_NAME, "text-danger"),
            (By.ID, "mensagemErro"),
            (By.ID, "error-message"),
            (By.CSS_SELECTOR, ".kc-feedback-text"),
            (By.CSS_SELECTOR, ".kc-content-wrapper > div.text-danger > span"),
        ]

        erro_detectado = False
        seletores_encontrados = []
        mensagens_erro = []

        print("Verificando elementos de erro...")

        for tipo, seletor in seletores_erro:
            try:
                erro_elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((tipo, seletor))
                )
                texto_erro = erro_elem.text.strip()
                if not texto_erro:
                    texto_erro = erro_elem.get_attribute('innerText') or erro_elem.get_attribute('textContent')
                    texto_erro = texto_erro.strip() if texto_erro else ''

                if texto_erro:
                    erro_detectado = True
                    seletores_encontrados.append(f"{tipo} - {seletor}")
                    mensagens_erro.append(texto_erro)
                    print(f"⚠️ Erro detectado: {texto_erro} | Seletor: {tipo} - {seletor}")
                    break  # <-- Aqui ele para após encontrar o primeiro erro

            except Exception as e:
                print(f"❌ Erro ao tentar localizar seletor {tipo} - {seletor}: {e}")
                continue

        driver.switch_to.default_content()

        # Resultado final
        resultado["url"] = url
        if sucesso:
            resultado["resultado"] = "✅ Login bem-sucedido"
        elif erro_detectado:
            resultado["resultado"] = f"❌ Login falhou: {' / '.join(mensagens_erro)}"
            resultado["seletores_erro_detectados"] = seletores_encontrados
        else:
            resultado["resultado"] = "❓ Resultado inconclusivo (sem indicadores claros)"

    except Exception as e:
        resultado["url"] = url
        resultado["resultado"] = f"⚠️ Erro ao testar login: {repr(e)}"
    finally:
        driver.quit()

    return resultado
