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
            "https://www.gotoeat-tochigi.jp/merchant/index.php?word=&sort=2&page={page}".format(page=page))
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.content, "html.parser")
        lists = soup.find("ul", {"class": "serch_result"}
                          ).findChildren("li", recursive=False)
        if (len(lists) == 0):
            break
        for merchant in lists:
            merchant_name = merchant.find("p", {"class": "name"}).text
            merchant_type = merchant.find(
                "p", {"class": "name"}).find("span").text
            merchant_name = re.sub(r"{merchant_type}$".format(
                merchant_type=merchant_type), "", merchant_name)
            _merchant_address = merchant.find(
                "div", {"class": "add"}).findAll("p")[0].text
            merchant_postal_code = re.sub(
                r"所在地〒([0-9\-]+) (.+)", r"\1", _merchant_address)
            merchant_address = re.sub(
                r"所在地〒([0-9\-]+) (.+)", r"\2", _merchant_address)
            if len(merchant.find("div", {"class": "add"}).findAll("p")) >= 2:
                merchant_tel = merchant.find(
                    "div", {"class": "add"}).findAll("p")[1].text
                merchant_tel = re.sub(r"TEL(.+)", r"\1", merchant_tel)

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
        if (soup.find("li", {"class": "next"}) == None):
            break
        else:
            time.sleep(1)

    merchants = checkRemovedMerchant(merchants, findMerchants)

    with open(merchantFilePath, mode="w", encoding="utf8") as f:
        f.write(json.dumps(merchants, indent=4, ensure_ascii=False))


main()
