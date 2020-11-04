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
            "https://gotoeat.hiroshima.jp/page/{page}/?s".format(page=page))
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.content, "html.parser")
        lists = soup.find(
            "div", {"class": "result"}).findChildren("div", {"class": "result__row"}, recursive=False)
        if (len(lists) == 0):
            break
        for merchant in lists:
            merchant_name = merchant.find(
                "h3", {"class": "result__name"}).text.strip()
            merchant_address = merchant.find(
                "p", {"class": "result__address"}).text.strip()
            merchant_type = []

            categories = merchant.find("ul", {"class": "result__cate"}).findChildren("li")
            for category in categories:
                merchant_type.append(category.text.strip())

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
                "lat": lat,
                "lng": lng
            })
            merchants["names"].append(merchant_name)

            try:
                with open(merchantFilePath, mode="w", encoding="utf8") as f:
                    f.write(json.dumps(merchants, indent=4, ensure_ascii=False))
            except Exception as e:
                print(e)
        if (soup.find("a", {"class": "nextpostslink"}) == None):
            break
        else:
            time.sleep(1)

    merchants = checkRemovedMerchant(merchants, findMerchants)

    with open(merchantFilePath, mode="w", encoding="utf8") as f:
        f.write(json.dumps(merchants, indent=4, ensure_ascii=False))


main()
