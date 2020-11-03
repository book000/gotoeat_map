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
            "https://www.gotoeat-aichi-shop.jp/shop/page/{page}/".format(page=page))
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.content, "html.parser")
        lists = soup.find("ul", {"class": "lcl-shop"}).findChildren(
            "li", {"class": "lcl-shop__item"}, recursive=False)
        if (len(lists) == 0):
            break
        for merchant in lists:
            merchant_name = merchant.find(
                "h2", {"class": "lcl-shop__name"}).text.strip()

            merchant_type = None
            if merchant.find("li", {"class": "lcl-shop-tag__item--cat"}) != None:
                merchant_type = merchant.find(
                    "li", {"class": "lcl-shop-tag__item--cat"}).text.strip()

            merchant_area = None
            if merchant.find("li", {"class": "lcl-shop-tag__item--area"}) != None:
                merchant_area = merchant.find(
                    "li", {"class": "lcl-shop-tag__item--area"}).text.strip()
            _merchant_address = merchant.find(
                "p", {"class": "lcl-shop__address"}).text.strip()
            merchant_postal_code = re.sub(
                r"〒([0-9\-]+) (.+)", r"\1", _merchant_address)
            merchant_address = re.sub(
                r"〒([0-9\-]+) (.+)", r"\2", _merchant_address)

            merchant_tel = None
            if merchant.find(
                    "a", {"class": "lcl-shop__link--tel"}) != None:
                merchant_tel = merchant.find(
                    "a", {"class": "lcl-shop__link--tel"}).text.strip()

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
        if (soup.find("a", {"class": "pagination-btn--next"}) == None):
            break
        else:
            time.sleep(1)

    merchants = checkRemovedMerchant(merchants, findMerchants)

    with open(merchantFilePath, mode="w", encoding="utf8") as f:
        f.write(json.dumps(merchants, indent=4, ensure_ascii=False))


main()
