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
            "https://gotoeat-yamaguchi.com/use/page/{page}/?post_type=post&s".format(page=page))
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.content, "html.parser")
        lists = soup.find("ul", {"id": "shop-list"}
                          ).findChildren("li", recursive=False)
        if (len(lists) == 0):
            break
        for merchant in lists:
            merchant_name = merchant.find(
                "h3").text.strip()

            merchant_time = None
            merchant_regular_holiday = None
            merchant_tel = None
            merchant_data = merchant.find("div", {"class": "break"}).findChildren("p")
            for data in merchant_data:
                key = data.find("strong").text.strip()
                if key.strip() == "［住所］":
                    merchant_address = data.text.strip(
                    )[data.text.strip().find("］")+1:].strip()
                elif key.strip() == "［営業時間］":
                    merchant_time = data.text.strip(
                    )[data.text.strip().find("］")+1:].strip()
                elif key.strip() == "［定休日］":
                    merchant_regular_holiday = data.text.strip(
                    )[data.text.strip().find("］")+1:].strip()
                elif key.strip() == "［TEL］":
                    merchant_tel = data.text.strip(
                    )[data.text.strip().find("］")+1:].strip()

            merchant_type = []
            categories = merchant.find(
                "p", {"class": "type"}).findChildren("a")
            for category in categories:
                merchant_type.append(category.text[1:].strip())

            merchant_corona_measures = []
            corona_measures = merchant.find(
                "ul", {"class": "measures_icon"}).findChildren("li")
            for corona_measure in corona_measures:
                merchant_corona_measures.append(
                    corona_measure.find("img").get("alt"))

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
                "time": merchant_time,
                "regular_holiday": merchant_regular_holiday,
                "tel": merchant_tel,
                "corona_measures": merchant_corona_measures,
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
