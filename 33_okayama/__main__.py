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
            "names": [],
            "categories": []
        }
    findMerchants = []

    html = requests.get("https://platinumaps.jp/maps/gotoeat-okayama", headers={
        "Accept-Language": "ja"
    })
    soup = BeautifulSoup(html.content, "html.parser")
    li_categories = soup.find("div", {"class": "map__categoryselect"}).find(
        "ul").findChildren("li", recursive=False)
    categories = {}

    for category in li_categories:
        category_key = category.get("data-category")
        category_value = category.find(
            "div", {"class": "category__name"}).text.strip()

        categories[category_key] = category_value

    merchants["categories"] = categories

    with open(merchantFilePath, mode="w", encoding="utf8") as f:
        f.write(json.dumps(merchants, indent=4, ensure_ascii=False))

    response = requests.get("https://platinumaps.jp/maps/88/spots", headers={
        "Accept-Language": "ja"
    })

    try:
        jsondata = response.json()
    except Exception as e:
        print(e)
        print(response.text)
        exit(1)

    for merchant in jsondata["spots"]:
        merchant_name = merchant["title"]
        merchant_address = merchant["address"]
        merchant_type = merchant["categories"]
        merchant_tel = merchant["phoneNumber"]
        merchant_regular_holiday = merchant["holiday"]
        lat = merchant["lat"]
        lng = merchant["lng"]

        print(merchant_name + " - " + merchant_address)
        findMerchants.append(merchant_name)

        if merchant_name in merchants["names"]:
            continue

        print(str(lat) + " " + str(lng))

        merchants["data"].append({
            "name": merchant_name,
            "type": merchant_type,
            "address": merchant_address,
            "tel": merchant_tel,
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
