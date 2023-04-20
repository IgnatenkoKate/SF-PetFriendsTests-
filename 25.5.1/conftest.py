from settings import valid_email, valid_password
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By



@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('G:\\chromedriver\\chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.close()


@pytest.fixture()
def user_page():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.set_window_size(1200, 800)
    pytest.driver.find_element(By.CLASS_NAME, 'btn.btn-success').click()
    # Проверяем, что мы оказались на странице пользователя
    pytest.driver.find_element(By.CSS_SELECTOR, '[href="/my_pets"]').click()
    assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'
