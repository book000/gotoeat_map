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

    response = requests.get("https://www.gotoeat-kochi.com/js/shop_list.php")

    try:
        jsondata = response.json()
    except Exception as e:
        print(e)
        print(response.text)
        exit(1)

    for merchant in jsondata:
        merchant_name = merchant[5]
        merchant_area = merchant[1]
        merchant_address = merchant[7]
        merchant_type = merchant[3]
        merchant_tel = merchant[8]

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

    merchants = checkRemovedMerchant(merchants, findMerchants)

    with open(merchantFilePath, mode="w", encoding="utf8") as f:
        f.write(json.dumps(merchants, indent=4, ensure_ascii=False))


main()
