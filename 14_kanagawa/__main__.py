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

    response = requests.get(
        "https://gotoeat-kanagawa.liny.jp/map/api/data.json?x1=33&x2=36&y1=137&y2=141")
    response.encoding = response.apparent_encoding

    try:
        jsondata = response.json()
    except Exception as e:
        print(e)
        print(response.text)
        exit(1)

    for merchant in jsondata["data"]:
        merchant_name = merchant["name"]
        merchant_address = merchant["address"]
        merchant_tel = merchant["tel"]
        lat = merchant["latlng"]["lat"]
        lng = merchant["latlng"]["lng"]

        print(merchant_name + " - " + merchant_address)
        findMerchants.append(merchant_name)

        if merchant_name in merchants["names"]:
            continue

        print(str(lat) + " " + str(lng))

        merchants["data"].append({
            "name": merchant_name,
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
