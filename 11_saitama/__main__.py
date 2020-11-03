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

    # Get Municipalities
    municipalitys = []
    html = requests.get("https://saitama-goto-eat.com/store.html")
    soup = BeautifulSoup(html.content, "html.parser")
    municipalitys_tag = soup.find(
        "select", {"id": "round"}).findChildren("option")
    for municipality in municipalitys_tag:
        if municipality.text == "選択してください。":
            continue
        if municipality.get("value") != None:
            municipalitys.append(municipality.get("value"))
        else:
            municipalitys.append(municipality.text)

    print(municipalitys)

    for municipality in municipalitys:
        time.sleep(1)
        html = requests.get(
            "https://saitama-goto-eat.com/store/{municipality}.html".format(municipality=municipality))
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.content, "html.parser")

        lists = soup.findAll("div", {"class": "storebox"})

        for merchant in lists:
            spans = merchant.findChildren("span", recursive=False)

            merchant_name = spans[0].text
            merchant_postal_code = spans[2].text
            merchant_address = spans[3].text
            merchant_tel = spans[4].text

            print(merchant_name + " - " + merchant_address)
            findMerchants.append(merchant_name)

            if merchant_name in merchants["names"]:
                continue

            lat, lng = getLatLng(merchant_address)
            print(str(lat) + " " + str(lng))

            merchants["data"].append({
                "name": merchant_name,
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


main()
