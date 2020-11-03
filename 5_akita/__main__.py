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
import math
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

    response = requests.get("https://gotoeat-akita.com/csv/list.csv")
    response.encoding = response.apparent_encoding
    reader = pd.read_csv(io.BytesIO(response.content),
                         names=("merchant_name", "merchant_area", "merchant_address", "merchant_tel", "merchant_url"))

    for row in reader.iterrows():
        merchant_name = row[1]["merchant_name"]
        merchant_name = str(re.sub(r"<!--.+-->", "", merchant_name)).strip()
        merchant_area = str(row[1]["merchant_area"]).strip()
        merchant_address = str(row[1]["merchant_address"]).strip()
        if type(row[1]["merchant_tel"]) is str:
             merchant_tel = str(row[1]["merchant_tel"]).strip()
        else:
            merchant_tel = None
        if type(row[1]["merchant_url"]) is str:
             merchant_url = str(row[1]["merchant_url"]).strip()
        else:
            merchant_url = None

        print(merchant_name + " - " + merchant_address)
        findMerchants.append(merchant_name)

        if merchant_name in merchants["names"]:
            continue

        lat, lng = getLatLng(merchant_address)
        print(str(lat) + " " + str(lng))

        merchants["data"].append({
            "name": merchant_name,
            "area": merchant_area,
            "address": merchant_address,
            "tel": merchant_tel,
            "url": merchant_url,
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
