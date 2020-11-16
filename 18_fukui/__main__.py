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

    html = requests.post(
        "https://gotoeat-fukui.com/shop/search.php", {"Keyword": "", "Action": "text_search"})
    soup = BeautifulSoup(html.content, "html.parser")
    lists = soup.find("div", {"class": "result"}).find("ul").findChildren(
        "li", recursive=False)

    merchant_ids = []
    for merchant in lists:
        merchant_id = re.sub(
            r"^\.\/\?id=([0-9]+)$", r"\1", merchant.find("a").get("href"))
        if merchant_id == merchant.find("a").get("href"):
            print("Failed to get ID: {href}".format(href=merchant.find("a").get("href")))
            exit(1)

        if merchant.find("a").find("strong").text.strip() != None:
            if merchant.find("a").find("strong").text.strip() in merchants["names"]:
                continue

        merchant_ids.append(merchant_id)

    print(merchant_ids)

    for merchant_id in merchant_ids:
        time.sleep(1)
        html = requests.get(
            "https://gotoeat-fukui.com/shop/?id={merchant_id}".format(merchant_id=merchant_id))
        soup = BeautifulSoup(html.content, "html.parser")

        merchant_name = soup.find("h3").text.strip()
        merchant_area = soup.find("span", {"class": "area"}).text.strip()

        dds = soup.find("dl").findChildren("dd", recursive=False)
        merchant_type = dds[0].text
        merchant_tel = dds[1].text
        merchant_address_gmap = str(dds[2])
        merchant_address = re.sub(r"^<dd>(.+)<br/><a class=\"gmap\" href=\"(.+?)\".+$", r"\1", merchant_address_gmap)
        merchant_gmap_url = re.sub(r"^<dd>(.+)<br/><a class=\"gmap\" href=\"(.+?)\".+$", r"\2", merchant_address_gmap)
        lat = re.sub(
            r"^.*q=([0-9\.]+),([0-9\.]+)$",
                r"\1",
                merchant_gmap_url)
        if lat == merchant_gmap_url:
            lat = None
        lng = re.sub(
            r"^.*q=([0-9\.]+),([0-9\.]+)$",
            r"\2",
            merchant_gmap_url)
        if lng == merchant_gmap_url:
            lng = None

        print(merchant_name + " - " + merchant_address)
        findMerchants.append(merchant_name)

        if lat == None or lng == None:
            print(merchant_gmap_url)

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
