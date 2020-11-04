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
    html = requests.get("https://www.iwate-gotoeat.jp/stores/")
    soup = BeautifulSoup(html.content, "html.parser")
    municipalitys_tag = soup.find(
        "select", {"name": "area"}).findChildren("option")
    for municipality in municipalitys_tag:
        if municipality.text == "市町村を選択してください":
            continue
        if municipality.get("value") != None:
            municipalitys.append(municipality.get("value"))
        else:
            municipalitys.append(municipality.text)

    print(municipalitys)

    for municipality in municipalitys:
        time.sleep(1)
        html = requests.post(
            "https://www.iwate-gotoeat.jp/stores/", data={"area": municipality})
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.content, "html.parser")

        lists = soup.findAll("div", {"class": "stores_box"})

        for merchant in lists:
            merchant_name = merchant.find("h2", {"class": "stores_box_name"}).text.strip()
            merchant_address = merchant.find("p", {"class": "stores_box_add"}).text.strip()
            merchant_tel = merchant.find("p", {"class": "stores_box_tel"}).text.strip()
            merchant_tel = re.sub(r"TEL：([0-9\-]+)", r"\1", merchant_tel)
            merchant_type = merchant.find(
                "p", {"class": "stores_box_genre"}).text.strip()
            merchant_type = merchant_type.split("・")

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
