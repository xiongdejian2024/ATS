#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@IDE     ：PyCharm
@Author  ：'wxa'
@Date    ：2022/11/30 9:40
"""
import base64
import os
import sys
import time


project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from codesrc.components.pressure.utils import get_config_info
from typing import List, Optional
from xat_ecu.legacy.common.logger import logger
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service



class AutoLogWiki:

    def __init__(self, docx_path, option):
        self.browser = None
        self.docx_path = docx_path
        self.option = option

    def auto_log_wiki(self):
        path = os.path.join(project_root, 'soa_lib/codesrc/chrome/opt/google/chrome/chromedriver')
        service = Service(executable_path=path)
        self.browser = webdriver.Chrome(service=service, options=self.option)
        
        url = 'https://wiki.jiduauto.com/pages/viewpage.action?pageId=682411640'
        self.browser.get(url)
        self.browser.maximize_window()
        time.sleep(5)
        # username = self.browser.find_element(By.ID, 'username')
        # wiki页面标签路径变更
        username = self.browser.find_element(By.XPATH,
                                             '//*[@id="app"]/div/div/div/form/div[1]/input')
        # passwd = self.browser.find_element(By.ID, 'password')
        passwd = self.browser.find_element(By.XPATH,
                                           '/html/body/div/div/div/div/form/div[2]/span/input')
        btn = self.browser.find_element(By.XPATH, '/html/body/div/div/div/div/button')
        config = get_config_info()
        name = base64.b64decode(config['wiki_uname'].encode()).decode('UTF-8')
        pwd = base64.b64decode(config['wiki_pwd'].encode()).decode('UTF-8')
        username.send_keys(name)
        passwd.send_keys(pwd)
        btn.click()
        time.sleep(15)
        # login_success = self.browser.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/div[2]/div[1]/div[2]/div[1]/ol/li[1]/span/a').text
        # login_success = self.browser.find_element(By.XPATH, '//*[@id="footer-logo"]/a').text
        # assert login_success == 'Atlassian'
        print("login_success")
        # time.sleep(8)

        create_page = self.browser.find_element(By.ID, 'quick-create-page-button')
        time.sleep(1)
        create_page.click()
        time.sleep(15)

        input_title = self.browser.find_element(By.ID, 'content-title')
        time.sleep(1)
        input_title.click()
        time.sleep(15)
        input_title.send_keys(self.docx_path.split('/')[-1])
        time.sleep(1)

        publish = self.browser.find_element(By.ID, 'rte-button-publish')
        time.sleep(1)
        publish.click()
        time.sleep(15)

        more_options = self.browser.find_element(By.XPATH, '//*[@id="action-menu-link"]/span/span')
        time.sleep(1)
        more_options.click()
        time.sleep(15)

        open_doc_page = self.browser.find_element(By.ID, 'import-word-doc')
        time.sleep(2)
        open_doc_page.click()
        time.sleep(15)

        many_btn = self.browser.find_element(By.ID, 'filename')
        time.sleep(1)
        many_btn.send_keys(self.docx_path)
        time.sleep(3)
        next_btn = self.browser.find_element(By.ID, 'next')
        time.sleep(2)
        next_btn.click()
        time.sleep(15)

        update_btn = self.browser.find_element(By.XPATH, '//*[@id="importwordform"]/fieldset[2]/div[2]/label')
        time.sleep(2)
        update_btn.click()
        time.sleep(15)

        update_btn1 = self.browser.find_element(By.XPATH, '//*[@id="importwordform"]/fieldset[3]/div[2]/label')
        time.sleep(2)
        update_btn1.click()
        time.sleep(15)
        try:
            ld_in_btn = self.browser.find_element(By.XPATH, '//*[@id="importwordform"]/div[3]/div/input')
        except Exception as e:
            ld_in_btn = self.browser.find_element(By.XPATH, '//*[@id="importwordform"]/div[2]/div/input')
            print(e)
        time.sleep(2)
        ld_in_btn.click()
        time.sleep(180)
        print(self.browser.current_url)
        return self.browser.current_url



class WikiTools(object):
    """
    @desp: wiki工具
    """

    pattern_list = {
        'text_username': '//*[@id="app"]/div/div/div/form/div[1]/input',
        'text_passwd': __import__("os").environ.get('XAT_CREDENTIAL____SOA_CASE_HELPER_CODESRC_COMPONENTS_PRESSURE_PUSH_DOCX_PY_TEXT_PASSWD', ""),
        'btn_login': '/html/body/div/div/div/div/button',
        'flag_login': '//*[@id="footer-logo"]/a',
        'quick-create-page-button':'//*[@id="quick-create-page-button"]',
        'btn_importdox_opt': '//*[@id="action-menu-link"]/span/span',
        'btn_importdox_update1': '//*[@id="importwordform"]/fieldset[2]/div[2]/label',
        'btn_importdox_update2': '//*[@id="importwordform"]/fieldset[3]/div[2]/label',
        'btn_importdox_ld_in_btn': '//*[@id="importwordform"]/div[3]/div/input',
        'btn_importdox_ld_in_btn_back': '//*[@id="importwordform"]/div[2]/div/input',
    }

    def __init__(self, driver_path: str = None, options_list: Optional[List[str]] = None, wiki_url: str = None):
        options = webdriver.ChromeOptions()
        if options_list:
            for opt in options_list:
                options.add_argument(opt)

        self._browser = webdriver.Chrome(service=Service(executable_path=driver_path), options=options)
        self._browser.implicitly_wait(30)
        self.url = wiki_url

    def login(self, wiki_url=None, username=None, passwd=None):
        if wiki_url:
            self.url = wiki_url
        self._browser.get(self.url)
        self._browser.maximize_window()
        self._wait(5)

        self._process_textedit(self.pattern_list['text_username'], msg=self.decode_msg(username))
        self._process_textedit(self.pattern_list['text_passwd'], msg=self.decode_msg(passwd))
        self._process_btn(self.pattern_list['btn_login'])
        self._wait(5)
        ans = self._find_elem(self.pattern_list['flag_login'])
        assert ans.text == 'Atlassian'
        logger.info('login success')
        self._wait(8)

    def create_pages(self, title='test'):
        self._process_btn(self.pattern_list['quick-create-page-button'])
        self._wait(2)
        item_title = self._process_btn('content-title', by=By.ID)
        item_title.send_keys(title)
        logger.info(f'item: {item_title} - {item_title.text}')
        self._wait(1)

        self._process_btn('rte-button-publish', by=By.ID)

    def import_docx(self, file_path):
        self._process_btn(self.pattern_list['btn_importdox_opt'])
        self._process_btn('import-word-doc', by=By.ID)
        self._process_textedit('filename', msg=file_path, by=By.ID)
        self._process_btn('next', by=By.ID)
        self._process_btn(self.pattern_list['btn_importdox_update1'])
        self._process_btn(self.pattern_list['btn_importdox_update2'])

        try:
            self._process_btn(self.pattern_list['btn_importdox_ld_in_btn'])
        except Exception as e:
            self._process_btn(self.pattern_list['btn_importdox_ld_in_btn_back'])
            logger.warning(f'err: {e}')
        self._wait(165)
        return self._browser.current_url

    @staticmethod
    def decode_msg(msg, encodings='utf-8'):
        from base64 import b64decode

        return b64decode(msg.encode()).decode(encodings)

    @staticmethod
    def _wait(t):
        from time import sleep

        sleep(t)

    def _find_elem(self, val: Optional[str] = None, by=By.XPATH):
        return self._browser.find_element(by=by, value=val)

    def _process_btn(self, val, by=By.XPATH):
        item = self._find_elem(val=val, by=by)
        item.click()
        self._wait(15)
        return item

    def _process_textedit(self, val, msg=None, by=By.XPATH):
        item = self._find_elem(val=val, by=by)
        item.send_keys(msg)
        return item


if __name__ == '__main__':
    wiki = WikiTools(
        driver_path='/root/ltg03/sat/soa_lib/codesrc/chrome/opt/google/chrome/chromedriver',
        options_list=[
            '--ignore-certificate-errors',
            '--ignore-ssl-errors',
            '--headless',
            '--no-sandbox',
            '--disable-dev-shm-usage',
        ],
    )

    wiki.login(
        wiki_url="https://wiki.jiduauto.com/pages/viewpage.action?pageId=672559750",
        username='amlhbGluLnhpYW4=',
        passwd=__import__("os").environ.get('XAT_CREDENTIAL____SOA_CASE_HELPER_CODESRC_COMPONENTS_PRESSURE_PUSH_DOCX_PY_PASSWD', ""),
    )
    logger.info('login OK')

    wiki.create_pages("111.docx")
    logger.info('new page OK')

    wiki_url = wiki.import_docx("/root/ltg03/pressure_log/111/111.docx")
    logger.info('import docx OK')

