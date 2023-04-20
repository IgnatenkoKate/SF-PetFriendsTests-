import pytest
from settings import valid_email, valid_password
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



# python -m pytest -v --driver Chrome --driver-path G:\chromedriver\chromedriver.exe tests_25_3.py

def test_show_my_pets():
    """Проверяем, что мы находимся на странице 'Мои питомцы'"""
    # Устанавливаем явное ожидание
    element = WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.ID, "email")))
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys(valid_email)

    element = WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.ID, "pass")))
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys(valid_password)

    element = WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    pytest.driver.set_window_size(1200, 800)
    # Проверяем, что мы оказались на странице пользователя
    pytest.driver.find_element(By.CSS_SELECTOR, '[href="/my_pets"]').click()
    assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'


def test_show_pet_friends():
    """Проверка карточек питомцев"""
    # Вводим email
    pytest.driver.implicitly_wait(5)
    pytest.driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # картинки питомцев
    images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card')
    # имена питомцев
    names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-body .card-title')
    # виды и возраста питомцев
    descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-body .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(', ')
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


def test_all_my_pets(user_page):
    """Присутствуют все питомцы"""
    # Сохраняем данные статистики
    statistic = pytest.driver.find_elements(By.CSS_SELECTOR, ".\\.col-sm-4.left")

    # Сохраняем данные карточек питомцев
    pets = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    # Получаем количество питомцев из данных статистики
    number = statistic[0].text.split('\n')
    number = number[1].split(' ')
    number = int(number[1])

    # Получаем количество карточек питомцев
    number_of_pets = len(pets)

    # Проверяем что количество питомцев из статистики совпадает с количеством карточек питомцев
    assert number == number_of_pets


def test_half_pets_have_photos(user_page):
    """Хотя бы у половины питомцев есть фото"""
    statistic = pytest.driver.find_elements(By.CSS_SELECTOR, ".\\.col-sm-4.left")

    # Сохраняем элементы с атрибутом img
    images = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover img')

    # Получаем количество питомцев из данных статистики
    number = statistic[0].text.split('\n')
    number = number[1].split(' ')
    number = int(number[1])

    # Находим половину от количества питомцев
    half = number // 2

    # Находим количество питомцев с фотографией
    quantity_of_pets = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            quantity_of_pets += 1

    # Проверяем что количество питомцев с фотографией больше или равно половине количества питомцев
    assert quantity_of_pets >= half
    print(f'количество фото: {quantity_of_pets}')
    print(f'Половина от числа питомцев: {half}')


def test_all_pets_have_descriptions(user_page):
    """У всех питомцев есть имя, возраст и порода"""
    statistic = pytest.driver.find_elements(By.CSS_SELECTOR, ".\\.col-sm-4.left")

    # Получаем количество питомцев из данных статистики
    number = statistic[0].text.split('\n')
    number = number[1].split(' ')
    number = int(number[1])

    pets = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')
    for i in range(len(pets)):
        data_pet = pets[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        result = len(split_data_pet)
        assert result == number


def test_pets_different_names(user_page):
    """У всех питомцев разные имена"""
    names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-body .card-title')
    list_names = []
    pets_count = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')

    for i in range(len(pets_count)):
        list_names.append(names[i].text)  # записываем имена животных
        assert names[i].text != ''  # проверяем что имя не пустое
    # Проверяем что у всех питомцев разные имена
    set_names = set(list_names)  # получаем из списка множество с уникальными именами
    assert len(set_names) == len(list_names)



