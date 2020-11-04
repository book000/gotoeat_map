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
            "https://premium-gift.jp/gotoeatmiyazaki/use_store?events=page&id={page}".format(page=page))
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.content, "html.parser")
        if soup.find("nav", {"class": "pagenation"}).find("span", {"class": "is-current"}).text != str(page):
            break
        lists = soup.find("div", {"class": "store-card"}).findChildren(
            "div", {"class": "store-card__item"}, recursive=False)
        if (len(lists) == 0):
            break

        for merchant in lists:
            merchant_name = merchant.find(
                "h3", {"class": "store-card__title"}).text.replace(u"\xa0", " ").strip()
            merchant_type = merchant.find(
                "p", {"class": "store-card__tag"}).text.strip()
            rows = merchant.find("table", {"class": "store-card__table"}).findChildren(
                "tr")

            for row in rows:
                th = row.find("th").text.strip()
                td = row.find("td").text.replace(u"\xa0", " ").strip()

                if th == "住所：":
                    merchant_postal_code = re.sub(
                        r"〒([0-9\-]+) (.+)", r"\1", td)
                    merchant_address = re.sub(
                        r"〒([0-9\-]+) (.+)", r"\2", td)
                elif th == "電話番号：":
                    merchant_tel = td

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
                "postal_code": merchant_postal_code,
                "tel": merchant_tel,
                "lat": lat,
                "lng": lng
            })
            merchants["names"].append(merchant_name)

            with open(merchantFilePath, mode="w", encoding="utf8") as f:
                f.write(json.dumps(merchants, indent=4, ensure_ascii=False))
        time.sleep(1)

    merchants = checkRemovedMerchant(merchants, findMerchants)

    with open(merchantFilePath, mode="w", encoding="utf8") as f:
        f.write(json.dumps(merchants, indent=4, ensure_ascii=False))


main()
