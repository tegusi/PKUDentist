# -*- coding: utf-8
import os
os.environ['WDM_SSL_VERIFY'] = '0'
import env_check
from configparser import ConfigParser
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from func import *
import warnings
import sys
import os
import re
warnings.filterwarnings('ignore')

def go(config):
    conf = ConfigParser()
    conf.read(config, encoding='utf8')

    userName, password = dict(conf['login']).values()

    run(driver_pjs, userName, password)


if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver_pjs = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(),
            options=chrome_options,
            service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
    print('Driver Launched\n')

    print('||门户登录||')
    go('config.ini')

    driver_pjs.quit()
