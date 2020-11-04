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
            "https://gotoeat-hyogo.com/search/result?page={page}".format(page=page))
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.content, "html.parser")
        lists = soup.find(
            "ul", {"class": "search-results-list"}).findChildren("li", recursive=False)
        if (len(lists) == 0):
            break
        for merchant in lists:
            merchant_name = merchant.find(
                "p", {"class": "search-results-list-name"}).text.strip()

            rows = merchant.findChildren(
                "p", {"class": "search-results-list-p01"})

            merchant_tel = None
            for row in rows:
                key = row.findChildren("span", recursive=False)[0].text.strip()
                value = row.findChildren("span", recursive=False)[
                    1].text.strip()

                if key == "住所：":
                    merchant_postal_code = re.sub(
                        r"〒([0-9\-]+)([\s\S]+)", r"\1", value)
                    merchant_address = re.sub(
                        r"〒([0-9\-]+)([\s\S]+)", r"\2", value).replace(
                        "\n", "").replace(" ", "").strip()
                elif key == "TEL：":
                    merchant_tel = value

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
        if (soup.find("p", {"class": "arrow-next"}).has_attr("disabled")):
            break
        else:
            time.sleep(1)

    merchants = checkRemovedMerchant(merchants, findMerchants)

    with open(merchantFilePath, mode="w", encoding="utf8") as f:
        f.write(json.dumps(merchants, indent=4, ensure_ascii=False))


main()
