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
            "https://gotoeat-saga.jp/consumer/shop.php?page={page}&name=#search_result2".format(page=page))
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.content, "html.parser")
        lists = soup.findChildren("div", {"class": "shop_detail"})
        if (len(lists) == 0):
            break
        for merchant in lists:
            merchant_name = merchant.find("div", {"class": "ttl"}).text.strip()
            merchant_type = merchant.find("div", {"class": "genre"}).text.strip()

            dts = merchant.find("dl").findChildren("dt", recursive=False)
            dds = merchant.find("dl").findChildren("dd", recursive=False)

            merchant_regular_holiday = None
            merchant_time = None
            merchant_tel = None
            for key in range(len(dts)):
                dt = dts[key].text.strip()
                dd = dds[key].text.strip()

                if dt == "住所":
                    merchant_address = re.sub(r"^(.+)MAP$", r"\1", dd).strip()
                elif dt == "定休日":
                    merchant_regular_holiday = dd
                elif dt == "営業時間":
                    merchant_time = dd
                elif dt == "電話番号":
                    merchant_tel = dd

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
                "lat": lat,
                "lng": lng
            })
            merchants["names"].append(merchant_name)

            with open(merchantFilePath, mode="w", encoding="utf8") as f:
                f.write(json.dumps(merchants, indent=4, ensure_ascii=False))
        if (soup.find("li", {"class": "next"}) == None):
            break
        else:
            time.sleep(1)

    merchants = checkRemovedMerchant(merchants, findMerchants)

    with open(merchantFilePath, mode="w", encoding="utf8") as f:
        f.write(json.dumps(merchants, indent=4, ensure_ascii=False))


main()
