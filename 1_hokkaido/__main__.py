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
    html = requests.get("https://gotoeat-hokkaido.jp/general/particStores")
    soup = BeautifulSoup(html.content, "html.parser")
    municipalitys_tag = soup.find("form").find(
        "select", {"class": "wide02"}).findChildren("option")
    for municipality in municipalitys_tag:
        if municipality.text == "選択してください":
            continue
        if municipality.get("value") != None:
            municipalitys.append(municipality.get("value"))
        else:
            municipalitys.append(municipality.text)

    print(municipalitys)

    for municipality in municipalitys:
        time.sleep(1)
        session = requests.Session()
        html = session.get("https://gotoeat-hokkaido.jp/general/particStores")
        soup = BeautifulSoup(html.content, "html.parser")
        _token = soup.find("form").find(
            "input", {"name": "_token"}).get("value").strip()
        html = session.post("https://gotoeat-hokkaido.jp/general/particStores/search", data={
            "store_area": municipality,
            "store_address1": "",
            "division1_id": "",
            "store_name": "",
            "_token": _token
        })

        page = 0
        while True:
            page += 1

            html = session.get(
                "https://gotoeat-hokkaido.jp/general/particStores?page={page}".format(page=page))
            soup = BeautifulSoup(html.content, "html.parser")

            lists = soup.find("div", {"class": "results"}).find("ul").findChildren("li", recursive=False)
            if (len(lists) == 0):
                break
            for merchant in lists:
                merchant_name = merchant.find(
                    "h4", {"class": "results-tit"}).text.strip()
                merchant_address = merchant.find(
                    "p", {"class": "results-txt01"}).text.strip()
                merchant_type = merchant.find(
                    "p", {"class": "results-txt02"}).text.strip()
                merchant_tel = merchant.find(
                    "p", {"class": "results-txt03"}).text.strip()
                merchant_tel = re.sub(r"TEL\.([0-9\-]+)", r"\1", merchant_tel)

                print(merchant_name + " - " + merchant_address)
                findMerchants.append(merchant_name)

                if merchant_name in merchants["names"]:
                    continue

                lat, lng = getLatLng(merchant_address)
                print(str(lat) + " " + str(lng))

                merchants["data"].append({
                    "name": merchant_name,
                    "type": merchant_type,
                    "area": municipality,
                    "address": merchant_address,
                    "tel": merchant_tel,
                    "lat": lat,
                    "lng": lng
                })
                merchants["names"].append(merchant_name)

                with open(merchantFilePath, mode="w", encoding="utf8") as f:
                    f.write(json.dumps(merchants, indent=4, ensure_ascii=False))
            if (soup.find("a", {"class": "nextpostslink"}) == None):
                break
            else:
                time.sleep(1)

    merchants = checkRemovedMerchant(merchants, findMerchants)

    with open(merchantFilePath, mode="w", encoding="utf8") as f:
        f.write(json.dumps(merchants, indent=4, ensure_ascii=False))


main()
