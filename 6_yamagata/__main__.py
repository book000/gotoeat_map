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
        result = requests.post(
            "https://yamagata-gotoeat.com/wp/wp-content/themes/gotoeat/search.php", data={"text": "", "page": page})
        result = result.json()
        if(result.get("html") == ""):
            break
        soup = BeautifulSoup(result.get("html"), "html.parser")

        lists = soup.findChildren("li", recursive=False)
        if (len(lists) == 0):
            break
        for merchant in lists:
            merchant_name = merchant.find("h2").text.strip()

            divs = merchant.findChildren("div", recursive=False)
            merchant_postal_code = re.sub(
                r"([0-9\-]+) (.+)", r"\1", divs[0].text.strip())
            merchant_address = re.sub(
                r"([0-9\-]+) (.+)", r"\2", divs[0].text.strip())
            merchant_tel = re.sub(
                r"TEL : ([0-9\-]+)", r"\1", divs[1].text.strip())

            tags = merchant.find("ul", {"class": "search__result__tag"}).findChildren(
                "li", recursive=False)
            merchant_area = tags[0].text.strip()
            merchant_type = tags[1].text.strip()

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
        time.sleep(1)

    merchants = checkRemovedMerchant(merchants, findMerchants)

    with open(merchantFilePath, mode="w", encoding="utf8") as f:
        f.write(json.dumps(merchants, indent=4, ensure_ascii=False))


main()
