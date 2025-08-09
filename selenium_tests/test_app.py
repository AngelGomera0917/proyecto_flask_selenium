

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Crear carpeta de capturas si no existe
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

@pytest.fixture
def browser(request):
    options = Options()
    options.add_argument('--headless=new')  # Quita esta línea si quieres ver el navegador
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("http://localhost:5000")

    yield driver

    # Guardar captura al final de cada prueba, pase o falle
    test_name = request.node.name
    screenshot_path = f"screenshots/{test_name}.png"
    try:
        driver.save_screenshot(screenshot_path)
        print(f"[INFO] Captura guardada: {screenshot_path}")
    except Exception as e:
        print(f"[ERROR] No se pudo guardar captura: {e}")

    driver.quit()

def login(browser, username, password):
    """Función de utilidad para iniciar sesión"""
    browser.find_element(By.NAME, "username").clear()
    browser.find_element(By.NAME, "username").send_keys(username)
    browser.find_element(By.NAME, "password").clear()
    browser.find_element(By.NAME, "password").send_keys(password)
    browser.find_element(By.TAG_NAME, "button").click()

def test_login_success(browser):
    login(browser, "admin", "admin")
    assert "Usuarios" in browser.page_source

def test_login_fail(browser):
    login(browser, "wrong", "wrong")
    assert "Usuarios" not in browser.page_source

def test_add_user(browser):
    login(browser, "admin", "admin")
    browser.find_element(By.NAME, "name").send_keys("Angel Antonio")
    browser.find_element(By.NAME, "email").send_keys("antoniogomera12@gmail.com")
    browser.find_element(By.NAME, "phone").send_keys("8299315927")
    browser.find_element(By.XPATH, "//form[@action='/add']//button").click()
    assert "antoniogomera12@gmail.com" in browser.page_source


def test_edit_user(browser):
    login(browser, "admin", "admin")
    # Asegurar que haya al menos un usuario para editar
    if "juan@example.com" not in browser.page_source:
        browser.find_element(By.NAME, "name").send_keys("Juan")
        browser.find_element(By.NAME, "email").send_keys("juan@example.com")
        browser.find_element(By.NAME, "phone").send_keys("8091234567")
        browser.find_element(By.XPATH, "//form[@action='/add']//button").click()
    edit_form = browser.find_elements(By.XPATH, "//form[contains(@action, '/edit/')]")[0]
    name_field = edit_form.find_element(By.NAME, "name")
    name_field.clear()
    name_field.send_keys("Juan Editado")
    edit_form.find_element(By.TAG_NAME, "button").click()
    assert "Juan Editado" in browser.page_source

def test_delete_user(browser):
    login(browser, "admin", "admin")
    # Asegurar que haya un usuario para borrar
    if "Juan Editado" not in browser.page_source:
        browser.find_element(By.NAME, "name").send_keys("Juan Editado")
        browser.find_element(By.NAME, "email").send_keys("juaneditado@example.com")
        browser.find_element(By.NAME, "phone").send_keys("8091234567")
        browser.find_element(By.XPATH, "//form[@action='/add']//button").click()
    delete_link = browser.find_elements(By.LINK_TEXT, "Eliminar")[0]
    delete_link.click()
    time.sleep(1)
    assert "Juan Editado" not in browser.page_source

