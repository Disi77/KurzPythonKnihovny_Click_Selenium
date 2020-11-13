import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import json
import datetime
from pathlib import Path
from os import mkdir


def login_page(driver, login_name, login_psw):
    try:
        driver.get('https://projekty.pyladies.cz/login')
        time.sleep(3)

        login = driver.find_element_by_name('email')
        login.clear()
        login.send_keys(login_name)

        psw = driver.find_element_by_name('password')
        psw.clear()
        psw.send_keys(login_psw)

        login_button_xpath = '/html/body/div/div/div[2]/div[2]/div/div[2]/div/form/div[3]/button'
        login_button = driver.find_element_by_xpath(login_button_xpath)
        login_button.click()
        time.sleep(2)
        if 'Nesprávný e-mail nebo heslo' in driver.page_source:
            return False, 'Nesprávný e-mail nebo heslo'
        return True, ''
    except:
        return False, 'Došlo k výjimce'


def open_course(driver, city, run):
    courses = driver.find_elements_by_class_name("course")
    for course in courses:
        if city in course.text and run in course.text:
            course.click()
            break
    time.sleep(5)


def create_lessons_list(driver):
    all_lessons_list = []

    lessons = driver.find_elements_by_class_name("session")
    for num, el in enumerate(lessons):
        lesson_dict = {}
        link = el.find_elements_by_class_name("button")
        if link:
            if (num+1) < 10:
                lesson_dict["name"] = "0" + str(num+1) + " " + el.text.split("\n")[0]
            else:
                lesson_dict["name"] = str(num+1) + " " + el.text.split("\n")[0]
            lesson_dict["date"] = el.text.split("\n")[1]
            lesson_dict["link"] = link[0].get_attribute("href")
            lesson_dict["button"] = link[0]
            all_lessons_list.append(lesson_dict)
    return all_lessons_list


def go_to_main_page(driver):
    logo_xpath = "/html/body/div/div/div[1]/div/div[1]"
    pyladies_logo = driver.find_element_by_xpath(logo_xpath)
    pyladies_logo.click()
    time.sleep(3)


def get_data(driver, all_lessons_list):
    all_together = {}
    for lesson in all_lessons_list:
        driver.get(lesson["link"])
        time.sleep(3)
        soup = bs(driver.page_source, 'html.parser')
        table = soup.find("table")
        table_data = []
        data = table.find_all("tr")

        for row in data:
            row_list = []
            for item in row:
                row_list.append(item.text)
            table_data.append(row_list)
        all_together[lesson["name"]] = table_data
    all_together["TimeStamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return all_together


def write_data_to_json(all_together):
    all_together_json = json.dumps(all_together, ensure_ascii=False)
    create_folder_for_results()
    path = Path.cwd() / 'results' / 'data.json'
    with open(str(path), mode="w", encoding="utf-8") as file:
        file.write(all_together_json)


def create_folder_for_results():
    while True:
        path = Path.cwd() / 'results'
        if not path.exists():
            mkdir(path)
        else:
            return


def scraping_homeworks_main(inputs):
    # Open browser and login into page
    path = inputs['driver-path']
    driver = webdriver.Chrome(path)
    driver.maximize_window()
    login_name = inputs['login']
    login_psw = inputs['psw']
    result = login_page(driver, login_name, login_psw)
    if not result[0]:
        print(30 * '=')
        print(result[1])
        print('Program bude ukončen')
        print(30 * '=')
        return

    # Find course PyLadies Ostrava podzim 2020
    city = inputs['city']
    run = inputs['run']
    time.sleep(3)
    open_course(driver, city, run)

    # Create list of lessons in course
    all_lessons_list = create_lessons_list(driver)
    all_together = get_data(driver, all_lessons_list)

    # Write data to JSON file
    write_data_to_json(all_together)
    driver.close()
