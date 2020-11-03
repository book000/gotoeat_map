# coding: utf-8
import requests
from bs4 import BeautifulSoup
import re
import json
import os
from xml.etree import ElementTree
import time
import io
import pandas as pd
from gotoeat_map.module import getLatLng, checkRemovedMerchant


def main():
    merchantFilePath = os.path.dirname(
        os.path.abspath(__file__)) + "/merchants.json"

    if os.path.exists(merchantFilePath):
        json_open = open(merchantFilePath, "r", encoding="utf8")
        merchants = json.load(json_open)
    else:
        merchants = {
            "data": [],
            "names": []
        }
    findMerchants = []

    page = 0
    while True:
        time.sleep(1)
        page += 1
        print("----- Page {page} -----".format(page=page))
        html = requests.get(
            "https://area34.smp.ne.jp/area/table/27130/3jFZ4A/M?_limit_27130=100&S=pimgn2lbtind&_page_27130={page}".format(page=page))
        soup = BeautifulSoup(html.content, "html.parser",
                             from_encoding="shift-jis")
        table = soup.findAll("table", {"class": "smp-table"})[0]

        rows = table.findAll("tr", {"class": "smp-row-data"})
        if len(rows) == 0:
            break
        for row in rows:
            cells = row.findAll("td")
            if len(cells) != 6:
                continue
            merchant_type = cells[0].text.strip()
            merchant_name = cells[1].text.strip()
            merchant_tel = cells[2].text.strip()
            merchant_address = cells[3].text.strip() + " " + cells[4].text.strip()

            print(merchant_name + " - " + merchant_address)
            findMerchants.append(merchant_name)

            if merchant_name in merchants["names"]:
                continue

            lat, lng = getLatLng(merchant_address)
            print(str(lat) + " " + str(lng))

            merchants["data"].append({
                "name": merchant_name,
                "type": merchant_type,
                "address": merchant_address,
                "tel": merchant_tel,
                "lat": lat,
                "lng": lng
            })
            merchants["names"].append(merchant_name)

            with open(merchantFilePath, mode="w", encoding="utf8") as f:
                f.write(json.dumps(merchants, indent=4, ensure_ascii=False))

    merchants = checkRemovedMerchant(merchants, findMerchants)

    with open(merchantFilePath, mode="w", encoding="utf8") as f:
        f.write(json.dumps(merchants, indent=4, ensure_ascii=False))


main()
