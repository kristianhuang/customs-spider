#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File: spider.py
@Desc: None
"""
from bs4 import BeautifulSoup


class Spider(object):

    def __init__(self):
        self.table = None

    def generateDom(self, html: str):
        self.table = BeautifulSoup(html, "lxml").find("table", id="ctl00_PageContent_MyGridView1")

        return self

    def crawlData(self):
        """
        crawling data.

        :return: datas
        """

        data = self.table.find_all("tr")
        # del page tr element.
        del data[len(data) - 1]
        del data[len(data) - 1]

        res = []
        for tr in data[4:]:
            td = tr.find_all("td")
            item = self.__generateItemData(td)
            res.append(item)

        return res

    def __generateItemData(self, item, type="world"):
        if type == "world":
            res = {
                "Exporters": item[1].get_text(strip=True),
                "Value exported in 2020 (USD thousand)sortOrderDESC": item[2].get_text(strip=True),
                "Trade balance in 2020 (USD thousand)": item[3].get_text(strip=True),
                "Quantity exported in 2020": item[4].get_text(strip=True),
                "Quantity Unit": item[5].get_text(strip=True),
                "Unit value (USD/unit)": item[6].get_text(strip=True),
                "Annual growth in value between 2016-2020 (%)": item[7].get_text(strip=True),
                "Annual growth in quantity between 2016-2020 (%)": item[8].get_text(strip=True),
                "Annual growth in value between 2019-2020 (%)": item[9].get_text(strip=True),
                "Share in world exports (%)": item[10].get_text(strip=True),
                "Average distance of importing countries (km)": item[11].get_text(strip=True),
                "Concentration of importing countries": item[12].get_text(strip=True),
            }

        else:
            res = {
                "Exporters": item[1].get_text(strip=True),
                "Value imported in 2020 (USD thousand)sortOrderDESC": item[2].get_text(strip=True),
                "Trade balance 2020 (USD thousand)": item[3].get_text(strip=True),
                "Share in Angola's imports (%)": item[4].get_text(strip=True),
                "Quantity imported in 2020": item[5].get_text(strip=True),
                "Quantity unit": item[6].get_text(strip=True),
                "Unit value (USD/unit)": item[7].get_text(strip=True),
                "Growth in imported value between 2016-2020 (%, p.a.)": item[8].get_text(strip=True),
                "Growth in imported quantity between 2016-2020 (%, p.a.)": item[9].get_text(strip=True),
                "Growth in imported value between 2019-2020 (%, p.a.)": item[10].get_text(strip=True),
                "Ranking of partner countries in world exports": item[11].get_text(strip=True),
                "Share of partner countries in world exports (%)": item[12].get_text(strip=True),
                "Total exports growth in value of partner countries between 2016-2020 (%, p.a.)": item[13].get_text(
                    strip=True),
                "Average distance between partner countries and all their importing markets (km)": item[14].get_text(
                    strip=True),
                "Concentration of all importing countries of partner countries": item[15].get_text(strip=True),
                "Average tariff (estimated) applied by Angola (%)": item[16].get_text(strip=True)
            }

        return res

    def countPage(self):
        """
        count page total.

        :return: page total
        """
        data = self.table.find_all("tr")
        # del redundancy element
        del data[len(data) - 1]
        pageContainerEl = data[len(data) - 1]
        pages = pageContainerEl.find("tr").find_all("td")

        return len(pages)
