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
            "https://www.gotoeat-nagasaki.jp/merchant-list/page/{page}/".format(page=page))
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.content, "html.parser")
        lists = soup.findChildren("div", {"class": "shop-list-content"})
        if (len(lists) == 0):
            break
        for merchant in lists:
            merchant_name = merchant.find(
                "div", {"class": "shop-list-content-name"}).text.strip()
            merchant_type = merchant.find(
                "div", {"class": "shop-list-content-cat"}).text.strip()
            merchant_area = merchant.find(
                "div", {"class": "shop-list-content-area"}).text.strip()
            merchant_address = merchant.find(
                "div", {"class": "shop-list-content-add-002"}).text.strip()
            merchant_tel = merchant.find(
                "div", {"class": "shop-list-content-tel-002"}).text.strip()

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
        if (soup.find("a", {"class": "next"}) == None):
            break
        else:
            time.sleep(1)

    merchants = checkRemovedMerchant(merchants, findMerchants)

    with open(merchantFilePath, mode="w", encoding="utf8") as f:
        f.write(json.dumps(merchants, indent=4, ensure_ascii=False))


main()
