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
        page += 1
        print("----- Page {page} -----".format(page=page))
        html = requests.get(
            "https://www.kagawa-gotoeat.com/gtes/store-list?mode=&p={page}".format(page=page))
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.content, "html.parser")
        lists = soup.findChildren("div", {"class": "store-list"})
        if (len(lists) == 0):
            break
        for merchant in lists:
            merchant_name = merchant.find(
                "h4").text.strip()

            rows = merchant.find("table").findChildren("tr")

            for row in rows:
                th = row.find("th").text.strip()
                td = row.find("td").text.strip()

                if th == "エリア":
                    merchant_area = td
                elif th == "料理ジャンル":
                    merchant_type = td
                elif th == "電話番号":
                    merchant_tel = td
                elif th == "住所":
                    merchant_address = re.sub(r"^([\s\S]+)MAPを見る", r"\1", td).strip()

            print(merchant_name + " - " + merchant_address)
            findMerchants.append(merchant_name)

            if merchant_name in merchants["names"]:
                continue

            lat, lng = getLatLng(merchant_address)
            print(str(lat) + " " + str(lng))

            merchants["data"].append({
                "name": merchant_name,
                "type": merchant_type,
                "area": merchant_area,
                "address": merchant_address,
                "tel": merchant_tel,
                "lat": lat,
                "lng": lng
            })
            merchants["names"].append(merchant_name)

            with open(merchantFilePath, mode="w", encoding="utf8") as f:
                f.write(json.dumps(merchants, indent=4, ensure_ascii=False))
        if (soup.find("a", {"class": "nextpostslink"}) == None):
            break
        else:
            time.sleep(1)

    merchants = checkRemovedMerchant(merchants, findMerchants)

    with open(merchantFilePath, mode="w", encoding="utf8") as f:
        f.write(json.dumps(merchants, indent=4, ensure_ascii=False))


main()
