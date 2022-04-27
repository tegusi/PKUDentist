from textwrap import fill
from matplotlib.pyplot import text
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from urllib.parse import quote
from urllib import request
import time
import warnings
import json
warnings.filterwarnings('ignore')


def login(driver, userName, password, retry=0):
    if retry == 3:
        raise Exception('门户登录失败')

    print('门户登陆中...')

    appID = 'portal2017'
    iaaaUrl = 'https://iaaa.pku.edu.cn/iaaa/oauth.jsp'
    appName = quote('北京大学校内信息门户新版')
    redirectUrl = 'https://portal.pku.edu.cn/portal2017/ssoLogin.do'

    driver.get('https://portal.pku.edu.cn/portal2017/')
    driver.get(
        f'{iaaaUrl}?appID={appID}&appName={appName}&redirectUrl={redirectUrl}')
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, 'logon_button')))
    driver.find_element_by_id('user_name').send_keys(userName)
    time.sleep(0.1)
    driver.find_element_by_id('password').send_keys(password)
    time.sleep(0.1)
    driver.find_element_by_id('logon_button').click()
    try:
        WebDriverWait(driver,
                      5).until(EC.visibility_of_element_located((By.ID, 'all')))
        print('门户登录成功！')
    except:
        print('Retrying...')
        login(driver, userName, password, retry + 1)


def go_to_simso(driver):
    butt_all = driver.find_element_by_id('all')
    driver.execute_script('arguments[0].click();', butt_all)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'tag_s_stuCampusExEnReq')))
    driver.find_element_by_id('tag_s_stuCampusExEnReq').click()
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'el-card__body')))

def go_to_dentist(driver):
    butt_all = driver.find_element_by_id('all')
    driver.execute_script('arguments[0].click();', butt_all)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'dentistAppointment')))
    driver.find_element_by_id('dentistAppointment').click()
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'li1')))
    driver.find_element_by_id('li1').click()
    time.sleep(2)
    
def fill_appointment(driver):

    # Iterate over all available items
    driver.switch_to.frame(0)
    lines = driver.find_elements_by_class_name('li-table')
    items = []
    item_buttons = []
    for line in lines:
        for item in line.find_elements_by_tag_name('td'):
            if item.text not in ['有号', '无号']:
                items.append(item.text)
            else:
                item_buttons.append((item.text, item.find_element_by_tag_name('button')))
    available_item = []
    for i in range(len(items)):
        if item_buttons[i][0] == '有号':
            available_item.append(i)
    print('Choose an item:')
    for i in range(len(available_item)):
        print(f'{i + 1}. {items[available_item[i]]}')
    item_select = int(input('> ')) - 1
    item_buttons[available_item[item_select]][1].click()
    time.sleep(0.1)

    WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.ID, 'ModalNotice')))
    time.sleep(0.1)

    # Click the confirmation button
    buttons = driver.find_element_by_xpath("//div[@id='ModalNotice']").find_elements_by_tag_name("button")
    for button in buttons:
        if button.text == '确定':
            button.click()
            time.sleep(0.1)
            break

    # Select physician
    physician_list = []
    physicians = driver.find_elements_by_class_name('li-table')
    for physician in physicians:
        name = physician.find_element_by_class_name('itemname').text
        memo = physician.find_element_by_class_name('memo').text
        for button in physician.find_elements_by_tag_name('button'):
            if button.text in ['有号', '无号']:
                physician_list.append((name, memo, button))
                break
    print('Choose a physician:')
    for i, physician in enumerate(physician_list):
        print(f'{i + 1}. {physician[2].text} {physician[0]} {physician[1]}')
    physician_select = int(input('> ')) - 1
    physician_list[physician_select][2].click()
    time.sleep(0.1)

    # Select appointment time
    WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.ID, 'dateList')))
    time_slots = driver.find_element_by_xpath("//div[@id='dateList']").find_elements_by_tag_name("button")
    print('Choose the appointment time:')
    for i, time_slot in enumerate(time_slots):
        print(f'{i + 1}. {time_slot.text}')
    time_select = int(input('> ')) - 1
    time_slots[time_select].click()
    time.sleep(0.1)

    WebDriverWait(driver, 3).until(
        EC.alert_is_present())
    alert = driver.switch_to.alert
    if alert.text == '预约成功':
        print('预约成功！')
    else:
        print(f'错误:{alert.text}')
        print('抱歉，请重新预约！')
    alert.accept()
    return

def run(driver, userName, password):
    login(driver, userName, password)
    print('=================================')

    go_to_dentist(driver)
    fill_appointment(driver)


if __name__ == '__main__':
    pass
