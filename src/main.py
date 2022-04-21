#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File: main.py
@Desc: None
"""
import os
import time

import ddddocr
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class WebDriver(object):
    def __init__(self):
        self.driver = self.createDriver()

    def createDriver(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument('blink-settings=imagesEnabled=false')
        # options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })
        # with open('./stealth.min.js') as f:
        #     js = f.read()
        # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        #     "source": js
        # })

        return driver

    def run(self, HS: str):
        url = f"https://www.trademap.org/Country_SelProduct.aspx?nvpm=1%7c%7c%7c%7c%7c{HS}%7c%7c%7c2%7c1%7c1%7c2%7c1%7c%7c2%7c1%7c1%7c1"
        self.driver.get(url)
        time.sleep(1)
        self.login()

        time.sleep(5)
        self.driver.implicitly_wait(5)
        self.driver.get(url)

        time.sleep(1)
        self.driver.execute_script("__doPostBack('ctl00$PageContent$MyGridView1','Page$2')")
        time.sleep(1)
        self.driver.execute_script("__doPostBack('ctl00$PageContent$MyGridView1','Page$3')")

    def login(self):
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
            code = self.verifCode(codeImgUrl)
            time.sleep(1)
            self.driver.find_element(By.ID, "ctl00_PageContent_CaptchaAnswer").send_keys(code)
            time.sleep(1)
            el = self.driver.find_element(By.NAME, "ctl00$PageContent$ButtonvalidateCaptcha")
            el.click()

    def verifCode(self, codeImgUrl: str):
        imgPath = self.__createCodeImg(codeImgUrl)
        orc = ddddocr.DdddOcr()
        with open(imgPath, 'rb') as f:
            image = f.read()
        code = orc.classification(image)
        os.remove(imgPath)

        return code

    def __createCodeImg(self, imgUrl: str):
        """
        create remote img.

        :param imgUrl: img url.
        :return: img path.
        """
        imgPath = "../cache/tmp.jpg"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
        }
        img = requests.get(imgUrl, verify=False, headers=headers).content
        tmpFile = open(imgPath, 'wb')
        tmpFile.write(img)
        tmpFile.close()
        return imgPath


class Spider(object):
    def __init__(self, HS: str):
        # self.url = f"https://www.trademap.org/Country_SelProduct.aspx?nvpm=1%7c%7c%7c%7c%7c{HS}%7c%7c%7c4%7c1%7c1%7c1%7c1%7c1%7c2%7c1%7c1%7c1"

        self.url = "https://www.trademap.org/Country_SelProduct.aspx?nvpm=1%7c%7c%7c%7c%7c0101%7c%7c%7c4%7c1%7c1%7c1%7c1%7c1%7c2%7c1%7c1%7c1"

        # self.url = "https://www.trademap.org/Country_SelProduct.aspx?nvpm=1%7c%7c%7c%7c%7c4602%7c%7c%7c4%7c1%7c1%7c1%7c1%7c1%7c2%7c1%7c1%7c1"

    def run(self):
        self.__createDomTree(self.fetchData())
        # res = self.domTree.find("table", id="ctl00_PageContent_MyGridView1")
        print(self.domTree)

    def __createDomTree(self, body: str):
        """生成 dom 树.
        :param body: html body.
        :return: None
        """
        self.domTree = BeautifulSoup(body, "lxml")

    def fetchData(self):
        """send request.
        :param url: request url
        :return: reps body
        """

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
            "Cookie": "AspxAutoDetectCookieSupport=1; ASP.NET_SessionId=ftkzurfkss3q3b45tmdqcf45; _ga=GA1.2.162965316.1650508419; _gid=GA1.2.1858068841.1650508419; TradeMap.session=F32E2C2FA0ECE257F3E98B667E5CDFE079B7BA5148D79A3FBB3F5014A9EEC4ADF0F7662E03EE8D667ECBCBF298EF3963B6C55BE17AD104BA499CD5FB9752D695350FD2E86C58F03076D783968A3B1D1082C1E620A3FA842C1D6FDD814E600173D244FB07586E6E5C22F0E2EFAFA05967A70F0E25A39EA337099DD1D6D3ED2CE5B1C0830754287C42338025A1CBA025977EE71D58; TradeMap.id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6IkNJQlpnTW9rQXhmcHhQZW8tS1BQa3ciLCJ0eXAiOiJKV1QifQ.eyJuYmYiOjE2NTA1MjAxOTIsImV4cCI6MTY1MDUyMDQ5MiwiaXNzIjoiaHR0cHM6Ly9pZHNlcnYubWFya2V0YW5hbHlzaXMuaW50cmFjZW4ub3JnIiwiYXVkIjoiVHJhZGVNYXAiLCJub25jZSI6IjdlOWFlODgzMzA1NDQyMTE4NzI4NmJjNTc2ODc0MDhhIiwiaWF0IjoxNjUwNTIwMTkyLCJjX2hhc2giOiJoaVVRaWNsbmV1dllBbU52aFIwc1F3Iiwic19oYXNoIjoiRE84WllxTm82eHdYQkhmV0pqclJRUSIsInNpZCI6ImROLWlXR3JWNUo0c1lheXNDRHlHbHciLCJzdWIiOiIxMmIyZDljMS1lZDExLTQxY2YtYWU5My04YmY5NTEyNzdiYTkiLCJhdXRoX3RpbWUiOjE2NTA1MjAxOTIsImlkcCI6ImxvY2FsIiwiZmFtaWx5X25hbWUiOiJIdWFuZyIsImdpdmVuX25hbWUiOiJLcmlzIiwiZ2VuZGVyIjoiTWFuIiwiY291bnRyeSI6IkNITiIsIm5hbWUiOiJrcmlzaHVhbmcwMDdAZ21haWwuY29tIiwiZW1haWwiOiJrcmlzaHVhbmcwMDdAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInVzZXJfaWQiOiIxNTg1OTc0IiwiYW1yIjpbInB3ZCJdfQ.Zd9gX_WZLxyZNnZHWbBkZZiVMbeRj0aN_u1DJcmA8smHV-rEsaKeTAi3FHZ694t2wnRnBIW-QJ8yWEHqUTxt9IybQY-L3zHI0AkdtZL-sJCgDtmiVi8NmZNR1-jVskxbRTXkuDgRtxVTgJM_FfV68nH9KsyTFLoFa6mHAdf7RevXP8ggYxlAZyNVinv926RIum8_mwrQVpIybB11cU07qIDZ-TeQlMj3WEluBCbdoKaKdC5q5AJP8LNcZrMln4GiLJ4InQZ3ot5MaK0ioHJa_JWBSchBKUT8Hb5S6VsXlCczH8FJWshu27tmd5y39XQ5TDEV7ARNgqiZiBqE1sc2kQ; TradeMap.access_token=eyJhbGciOiJSUzI1NiIsImtpZCI6IkNJQlpnTW9rQXhmcHhQZW8tS1BQa3ciLCJ0eXAiOiJhdCtqd3QifQ.eyJuYmYiOjE2NTA1MjAxOTMsImV4cCI6MTY1MDUyMTk5MywiaXNzIjoiaHR0cHM6Ly9pZHNlcnYubWFya2V0YW5hbHlzaXMuaW50cmFjZW4ub3JnIiwiYXVkIjoiTUFSSWRTZXJ2LkFQSSIsImNsaWVudF9pZCI6IlRyYWRlTWFwIiwic3ViIjoiMTJiMmQ5YzEtZWQxMS00MWNmLWFlOTMtOGJmOTUxMjc3YmE5IiwiYXV0aF90aW1lIjoxNjUwNTIwMTkyLCJpZHAiOiJsb2NhbCIsInVzZXJfaWQiOiIxNTg1OTc0IiwicHJvamVjdCI6IjEiLCJsaWNlbnNlIjoiOSIsImlzX2RldmVsb3BpbmciOiJUcnVlIiwiYWNjZXNzIjoiZnVsbCIsInNjb3BlIjpbIm9wZW5pZCIsImVtYWlsIiwicHJvZmlsZSIsIkFjdGl2aXR5TG9nIiwib2ZmbGluZV9hY2Nlc3MiXSwiYW1yIjpbInB3ZCJdfQ.qLj62Tzc1pSe6omYTKFkbisrmV6w68H_1G5Ez9ak-6Q0yjILQIVzdb6JitcclB0GqPw8hK_naorZSUiVBrKkqCEcbc6wvy-c6Lk8XDbPuFttRKkdc-6RWFnMpa_nBm0sySU1W46Ya-JkbifvnCkuoLGVZWou2NuMfkhMprP48QGK93Bh07wyZpJbQBEVLloxiygxkrll232yBxF8kJF6pyxHGhjR8tAp4u5zRJGfb4QGFCDto8D2-7J-DdjEpKTRPbXWPW0QGYZHAR-cnGKtvsK-Q36NmhbJQNN-tNdztLlBjIJZzU47wbm1BYD3c7MtjgsEW6LQ8DyOkxtC8nH1nQ; TradeMap.refresh_token=tW2xHtPCC38AJ17uN8XtgOujnOlNOAcqUcZ0cLCZbvk"
        }

        data = {
            "__EVENTARGUMENT": "Page%2"
        }

        return requests.post(url=self.url, headers=headers, data=data, verify=False).text


if __name__ == '__main__':
    s = WebDriver()
    s.run("0101")
