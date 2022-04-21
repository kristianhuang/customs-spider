import re

import requests
from bs4 import BeautifulSoup
import pandas as pd


class Demo(object):

    def __init__(self):
        self.tree = None

    def fetch(self):
        url = f"https://www.trademap.org/Country_SelProductCountry.aspx?nvpm=1%7c024%7c%7c%7c%7c460212%7c%7c%7c6%7c1%7c2%7c1%7c1%7c1%7c2%7c1%7c1%7c1"
        header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
        }

        html = requests.get(url, headers=header, verify=False).content
        self.tree = BeautifulSoup(html, "lxml")

        data = self.generateData(self.tree.find("table", id="ctl00_PageContent_MyGridView1"))
        self.generateExcel(data)

    def generateData(self, table):
        datas = table.find_all("tr")

        # del page tr element.
        del datas[len(datas) - 1]
        del datas[len(datas) - 1]

        res = []
        for tr in datas[4:]:
            tds = tr.find_all("td")
            res.append({
                "Exporters": tds[1].get_text(strip=True),
                "Value imported in 2020 (USD thousand)sortOrderDESC": tds[2].get_text(strip=True),
                "Trade balance 2020 (USD thousand)": tds[3].get_text(strip=True),
                "Share in Angola's imports (%)": tds[4].get_text(strip=True),
                "Quantity imported in 2020": tds[5].get_text(strip=True),
                "Quantity unit": tds[6].get_text(strip=True),
                "Unit value (USD/unit)": tds[7].get_text(strip=True),
                "Growth in imported value between 2016-2020 (%, p.a.)": tds[8].get_text(strip=True),
                "Growth in imported quantity between 2016-2020 (%, p.a.)": tds[9].get_text(strip=True),
                "Growth in imported value between 2019-2020 (%, p.a.)": tds[10].get_text(strip=True),
                "Ranking of partner countries in world exports": tds[11].get_text(strip=True),
                "Share of partner countries in world exports (%)": tds[12].get_text(strip=True),
                "Total exports growth in value of partner countries between 2016-2020 (%, p.a.)": tds[13].get_text(
                    strip=True),
                "Average distance between partner countries and all their importing markets (km)": tds[14].get_text(
                    strip=True),
                "Concentration of all importing countries of partner countries": tds[15].get_text(strip=True),
                "Average tariff (estimated) applied by Angola (%)": tds[16].get_text(strip=True)
            })

        return res

    def generateExcel(self, data):
        df = pd.DataFrame(data)
        df.to_excel("../data/demo.xlsx", sheet_name='Sheet1', engine='xlsxwriter')


if __name__ == '__main__':
    d = Demo()
    d.fetch()
