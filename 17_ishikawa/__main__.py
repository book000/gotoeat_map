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
            "https://ishikawa-gotoeat-cpn.com/?cities&type&s&post_type=member_store&paged={page}".format(page=page))
        soup = BeautifulSoup(html.content, "html.parser")
        lists = soup.find("ul", {"class": "member_list"}).findChildren(
            "li", {"class": "member_item"}, recursive=False)
        if (len(lists) == 0):
            break
        for merchant in lists:
            merchant_name = merchant.find(
                "h4", {"class": "name"}).text.strip()
            merchant_type = merchant.find(
                "div", {"class": "type"}).text.strip()
            merchant_address = merchant.find(
                "div", {"class": "address"}).find("div", {"class": "content"}).text.strip()
            merchant_postal_code = merchant.find(
                "div", {"class": "address"}).find("div", {"class": "post"}).text.strip()
            merchant_tel = None
            if merchant.find(
                    "div", {"class": "tel"}) != None:
                merchant_tel = merchant.find(
                    "div", {"class": "tel"}).text.strip()

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
        if (soup.find("div", {"class": "page_nation"}).find("span", {"class": "page_next"}) == None):
            break
        else:
            time.sleep(1)

    merchants = checkRemovedMerchant(merchants, findMerchants)

    with open(merchantFilePath, mode="w", encoding="utf8") as f:
        f.write(json.dumps(merchants, indent=4, ensure_ascii=False))


main()
