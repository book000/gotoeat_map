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

    response = requests.get(
        "https://gotoeat-fukuoka.jp/csv/fk_gotoeat_UTF-8.csv")
    response.encoding = response.apparent_encoding
    reader = pd.read_csv(io.BytesIO(response.content),
                         names=("merchant_id", "merchant_name", "merchant_name_kana", "merchant_type", "merchant_postal_code", "merchant_prefecture", "merchant_area", "merchant_address", "merchant_building_name", "merchant_tel", "merchant_url", "merchant_addedDate"))

    for row in reader.iterrows():
        if row[1]["merchant_id"] == "id":
            continue

        merchant_name = str(row[1]["merchant_name"])
        merchant_type = str(row[1]["merchant_type"])
        merchant_postal_code = str(row[1]["merchant_postal_code"])
        merchant_area = str(row[1]["merchant_area"])
        merchant_address = str(row[1]["merchant_prefecture"]) + \
            str(row[1]["merchant_area"]) + \
            str(row[1]["merchant_address"])
        if type(row[1]["merchant_building_name"]) is str:
            merchant_address += row[1]["merchant_building_name"]
        merchant_tel = str(row[1]["merchant_tel"])

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
            "postal_code": merchant_postal_code,
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
