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
            "https://www.toyamagotoeat.jp/shop/page/{page}/".format(page=page))
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.content, "html.parser")
        lists = soup.find("ul", {"class": "list"}).findChildren(
            "li", {"class": "item"}, recursive=False)
        if (len(lists) == 0):
            break
        for merchant in lists:
            merchant_name = merchant.find(
                "div", {"class": "item_body_name"}).text.strip()
            merchant_type = merchant.find(
                "div", {"class": "item_header"}).text.strip()
            merchant_address = merchant.find(
                "div", {"class": "place"}).find("div", {"class": "rig"}).text.strip()
            if merchant.find("div", {"class": "phone"}) != None:
                merchant_tel = merchant.find(
                    "div", {"class": "phone"}).find("div", {"class": "rig"}).text.strip()
            else:
                merchant_tel = None

            if merchant.find("div", {"class": "work"}) != None:
                merchant_time = merchant.find(
                    "div", {"class": "work"}).find("div", {"class": "rig"}).text.strip()
            else:
                merchant_time = None

            if merchant.find("div", {"class": "off_day"}) != None:
                merchant_regular_holiday = merchant.find(
                    "div", {"class": "off_day"}).find("div", {"class": "rig"}).text.strip()
            else:
                merchant_regular_holiday = None

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
                "time": merchant_time,
                "regular_holiday": merchant_regular_holiday,
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
