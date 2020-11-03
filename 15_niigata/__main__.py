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
            "https://niigata-gte.com/shop/page/{page}/".format(page=page))
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.content, "html.parser")
        if soup.find("div", {"id": "result"}) == None:
            break
        lists = soup.find("div", {"id": "result"}).findChildren(
            "div", {"class": "cont"}, recursive=False)
        if (len(lists) == 0):
            break
        for merchant in lists:
            merchant_name = merchant.find("h4").text.strip()
            merchant_area = merchant.find("div", {"class": "tag"}).findChildren(
                "span", recursive=False)[0].text.strip()
            merchant_type = merchant.find("div", {"class": "tag"}).findChildren(
                "span", recursive=False)[1].text.strip()
            _merchant_address = merchant.find("p", {"class": "add"}).text
            merchant_postal_code = re.sub(
                r"〒([0-9\-]+) (.+)MAP", r"\1", _merchant_address).strip()
            merchant_address = re.sub(
                r"〒([0-9\-]+) (.+)MAP", r"\2", _merchant_address).strip()
            if merchant.find("p", {"class": "tel"}) != None:
                merchant_tel = merchant.find(
                    "p", {"class": "tel"}).text.strip()

            latlng = merchant.find("p", {"class": "add"}).find("a").get("href")
            lat = re.sub(
                r"^.+maps\/(?:place|search)\/(.+)\/@([0-9\.]+),([0-9\.]+),([0-9\.]+)z.*$",
                r"\2",
                latlng)
            if lat == latlng:
                lat = None
            lng = re.sub(
                r"^.+maps\/(?:place|search)\/(.+)\/@([0-9\.]+),([0-9\.]+),([0-9\.]+)z.*$",
                r"\3",
                latlng)
            if lng == latlng:
                lng = None

            print(merchant_name + " - " + merchant_address)
            print(str(lat) + " " + str(lng))
            findMerchants.append(merchant_name)

            if lat == None or lng == None:
                print(latlng)

            if merchant_name in merchants["names"]:
                continue

            if lat == None or lng == None:
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
        if (soup.find("li", {"class": "next"}) == None):
            break
        else:
            time.sleep(1)

    merchants = checkRemovedMerchant(merchants, findMerchants)

    with open(merchantFilePath, mode="w", encoding="utf8") as f:
        f.write(json.dumps(merchants, indent=4, ensure_ascii=False))


main()
