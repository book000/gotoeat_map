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

    response = requests.get("https://static.batchgeo.com/map/json/bb0346d09d7761e1888e982c45c09cc9/1603655201")
    startIndex = str(response.text).find("{")
    if startIndex == -1:
        print("Invalid JSON")
        return

    responseJson = str(response.text[startIndex:-1])
    responseJson = json.loads(responseJson)

    for key in range(len(responseJson["mapRS"])):
        merchant_address = responseJson["mapRS"][key]["addr"]
        merchant_address = re.sub(r"^([0-9\-]+) (.+)$", r"\2", merchant_address)
        lat = responseJson["mapRS"][key]["lt"]
        lng = responseJson["mapRS"][key]["ln"]
        merchant_name = responseJson["mapRS"][key]["t"]
        merchant_name = responseJson["dataRS"][key][0]
        merchant_postal_code = responseJson["dataRS"][key][1]
        merchant_tel = responseJson["dataRS"][key][5]
        merchant_time = responseJson["dataRS"][key][7]
        merchant_regular_holiday = responseJson["dataRS"][key][8]
        merchant_type = responseJson["dataRS"][key][9]

        print(merchant_name + " " + merchant_address)
        findMerchants.append(merchant_name)
        if merchant_name in merchants["names"]:
            continue

        print(str(lat) + " " + str(lng))

        merchants["data"].append({
            "name": merchant_name,
            "type": merchant_type,
            "address": merchant_address,
            "postal_code": merchant_postal_code,
            "tel": merchant_tel,
            "time": merchant_time,
            "lat": lat,
            "lng": lng
        })
        merchants["names"].append(merchant_name)

    merchants = checkRemovedMerchant(merchants, findMerchants)

    with open(merchantFilePath, mode="w", encoding="utf8") as f:
            f.write(json.dumps(merchants, indent=4, ensure_ascii=False))

main()
