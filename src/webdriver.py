#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File: webdriver.py
@Desc: None
"""
import os
import time

import ddddocr
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from src.spider import Spider


class WebDriver(object):
    def __init__(self):
        self.driver = self.__generateDriver()

    def fetchCustoms(self, hs: str, criteria: str):
        url = self.__generateUrl(hs, criteria)
        self.driver.get(url)
        time.sleep(1)
        self.__handleLogin()
        time.sleep(5)
        self.driver.implicitly_wait(5)
        self.driver.get(url)
        time.sleep(2)

        sp = Spider()
        time.sleep(1)
        sp.generateDom(self.driver.page_source)
        time.sleep(1)
        pageTotal = sp.countPage()

        datas = []
        datas.extend(sp.crawlData())
        for p in range(1, pageTotal):
            self.driver.execute_script(f"__doPostBack('ctl00$PageContent$MyGridView1','Page${p + 1}')")
            time.sleep(1)
            sp.generateDom(self.driver.page_source)
            datas.extend(sp.crawlData())

        self.driver.close()

        return datas

    def __handleLogin(self):
        """
        dispatch Login

        :return: None
        """
        self.driver.execute_script("Login()")
        time.sleep(1)
        # find form element, then input user data.
        self.driver.find_element(By.ID, "Username").send_keys("royal872@163.com")
        time.sleep(1)
        self.driver.find_element(By.ID, "Password").send_keys("jngj8sl")
        time.sleep(1)
        self.driver.find_element_by_class_name("mb-1").click()
        time.sleep(1)

        # If url is login page, verify code
        if self.driver.current_url == "https://www.trademap.org/stCaptcha.aspx":
            codeImgUrl = self.driver.find_element(By.XPATH, "//img[@width=200]").get_attribute("src")
            time.sleep(1)
            code = self.__verifyCode(codeImgUrl)
            time.sleep(1)
            self.driver.find_element(By.ID, "ctl00_PageContent_CaptchaAnswer").send_keys(code)
            time.sleep(1)
            el = self.driver.find_element(By.NAME, "ctl00$PageContent$ButtonvalidateCaptcha")
            el.click()

    def __verifyCode(self, codeImgUrl: str):
        imgPath = self.__generateCodeImg(codeImgUrl)
        orc = ddddocr.DdddOcr(show_ad=False)
        with open(imgPath, 'rb') as f:
            image = f.read()
        code = orc.classification(image)

        os.remove(imgPath)

        return code

    def __generateDriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # 无头模式
        options.add_argument("--disable-gpu")  # 禁止弹窗
        options.add_argument('--incognito')  # 无痕隐身
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument('blink-settings=imagesEnabled=false')
        # options.add_argument("start-maximized")
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--log-level=OFF")  # 关闭日志打印

        driver = webdriver.Chrome(executable_path=ChromeDriverManager(print_first_line=False).install(),
                                  options=options)
        with open(f'{os.path.dirname(__file__)}/../stealth.min.js') as f:
            js = f.read()
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })

        return driver

    def __generateCodeImg(self, imgUrl: str):
        """
        create remote img.

        :param imgUrl: img url.
        :return: img path.
        """
        imgPath = f'{os.path.dirname(__file__)}/../cache/tmp.jpg'
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
        }
        img = requests.get(imgUrl, verify=False, headers=headers).content
        tmpFile = open(imgPath, 'wb')
        tmpFile.write(img)
        tmpFile.close()

        return imgPath

    def __generateUrl(self, hs: str, criteria: str):
        criteriaList = {
            "exports": f"https://www.trademap.org/Country_SelProduct.aspx?nvpm=1%7c%7c%7c%7c%7c{hs}%7c%7c%7c2%7c1%7c1%7c2%7c1%7c%7c2%7c1%7c1%7c1",
            "imports": f"https://www.trademap.org/Country_SelProduct.aspx?nvpm=1%7c%7c%7c%7c%7c{hs}%7c%7c%7c2%7c1%7c1%7c1%7c1%7c%7c2%7c1%7c1%7c1",
        }

        return criteriaList[criteria]
