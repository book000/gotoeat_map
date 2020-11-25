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
    municipalitys = {}
    html = requests.get("https://gte-miyagi.jp/available.html")
    soup = BeautifulSoup(html.content, "html.parser")
    municipality_tags = soup.find(
        "ul", {"class": "sendai"}).findChildren("li", recursive=False)
    for municipality in municipality_tags:
        municipalitys[municipality.find("a").text.strip()] = re.sub(
            r"\.\/", "", municipality.find("a").get("href"))

    print(municipalitys)

    for merchant_area, municipality in municipalitys.items():
        print(municipality)
        html = requests.get(
            "https://gte-miyagi.jp/{municipality}".format(municipality=municipality))
        soup = BeautifulSoup(html.content, "html.parser")

        lists = soup.find("div", {"class": "SLCont"}).findChildren(
            "dl", {"class": "shopList"}, recursive=False)
        if (len(lists) == 0):
            break
        for merchant in lists:
            merchant_name = merchant.find("dt").text.strip()
            dds = merchant.findChildren("dd", recursive=False)

            merchant_type = None
            merchant_address = None
            merchant_postal_code = None
            merchant_tel = None
            for dd in dds:
                spans = dd.findChildren("span", recursive=False)
                if (len(spans) != 2):
                    continue
                if spans[0].text.strip() == "カテゴリ:":
                    merchant_type = spans[1].text.strip()
                elif spans[0].text.strip() == "住所:":
                    merchant_postal_code = re.sub(
                        r"〒([0-9\-]+)(.+)", r"\1", spans[1].text.strip())
                    merchant_address = re.sub(
                        r"〒([0-9\-]+)(.+)", r"\2", spans[1].text.strip())
                elif spans[0].text.strip() == "電話番号:":
                    merchant_tel = spans[1].text.strip()

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
