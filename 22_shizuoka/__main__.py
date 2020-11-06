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

    ret = get_fujinokuni(merchants, findMerchants)
    merchants = ret["merchants"]
    findMerchants = ret["findMerchants"]

    ret = get_fujinokuni(merchants, findMerchants)
    merchants = ret["merchants"]
    findMerchants = ret["findMerchants"]

    merchants = checkRemovedMerchant(merchants, findMerchants)

    with open(merchantFilePath, mode="w", encoding="utf8") as f:
        f.write(json.dumps(merchants, indent=4, ensure_ascii=False))

def get_fujinokuni(merchants, findMerchants):
    page = 0
    while True:
        page += 1
        print("----- Page {page} -----".format(page=page))
        html = requests.get(
            "https://premium-gift.jp/fujinokunigotoeat/use_store?events=page&id={page}".format(page=page))
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.content, "html.parser")
        if soup.find("nav", {"class": "pagenation"}).find("span", {"class": "is-current"}).text != str(page):
            break
        lists = soup.find("div", {"class": "store-card"}).findChildren(
            "div", {"class": "store-card__item"}, recursive=False)
        if (len(lists) == 0):
            break
        for merchant in lists:
            merchant_name = merchant.find(
                "h3", {"class": "store-card__title"}).text.replace(u"\xa0", " ").strip()
            merchant_type = merchant.find(
                "p", {"class": "store-card__tag"}).text.strip()
            rows = merchant.find("table", {"class": "store-card__table"}).findChildren(
                "tr")

            for row in rows:
                th = row.find("th").text.strip()
                td = row.find("td").text.replace(u"\xa0", " ").strip()

                if th == "住所：":
                    merchant_postal_code = re.sub(
                        r"〒([0-9\-]+) (.+)", r"\1", td)
                    merchant_address = re.sub(
                        r"〒([0-9\-]+) (.+)", r"\2", td)
                elif th == "電話番号：":
                    merchant_tel = td

            print(merchant_name + " - " + merchant_address)
            findMerchants.append(merchant_name)

            if merchant_name in merchants["names"]:
                continue

            lat, lng = getLatLng(merchant_address)
            print(str(lat) + " " + str(lng))

            merchants["data"].append({
                "source": "premium-gift.jp",
                "name": merchant_name,
                "type": merchant_type,
                "address": merchant_address,
                "postal_code": merchant_postal_code,
                "tel": merchant_tel,
                "lat": lat,
                "lng": lng
            })
            merchants["names"].append(merchant_name)
        time.sleep(1)
    return {"merchants": merchants, "findMerchants": findMerchants}


def get_shizuoka(merchants, findMerchants):
    page = 0
    while True:
        page += 1
        print("----- Page {page} -----".format(page=page))
        html = requests.get(
            "https://gotoeat-shizuoka.com/shop/page/{page}/".format(page=page))
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.content, "html.parser")
        lists = soup.find("ul", {"id": "shop_list"}).findChildren(
            "li", {"class": "shop_box"}, recursive=False)
        if (len(lists) == 0):
            break
        for merchant in lists:
            merchant_name = merchant.find(
                "h2", {"class": "shop_name"}).text.strip()
            merchant_type = []
            for genre in merchant.findAll("span", {"class": "shop_genre"}):
                merchant_type.append(genre.text.strip())
            merchant_area = merchant.find(
                "span", {"class": "shop_area"}).text.strip()
            merchant_area = re.sub(r"^【(.+)】$", r"\1", merchant_area)

            rows = merchant.find("div", {"class": "shop_detail"}).find(
                "table").findChildren("tr")

            merchant_tel = None
            merchant_time = None
            merchant_regular_holiday = None
            for row in rows:
                th = row.find("th").text.strip()
                td = row.find("td").text.replace(u"\xa0", " ").strip()

                if th == "住所":
                    merchant_postal_code = re.sub(
                        r"〒([0-9\-]+)(.+)", r"\1", td)
                    merchant_address = re.sub(
                        r"〒([0-9\-]+)(.+)", r"\2", td)
                elif th == "電話番号":
                    merchant_tel = td
                elif th == "営業時間":
                    merchant_time = td
                elif th == "定休日":
                    merchant_regular_holiday = td

            print(merchant_name + " - " + merchant_address)
            findMerchants.append(merchant_name)

            if merchant_name in merchants["names"]:
                continue

            lat, lng = getLatLng(merchant_address)

            merchants["data"].append({
                "source": "gotoeat-shizuoka.com",
                "name": merchant_name,
                "type": merchant_type,
                "postal_code": merchant_postal_code,
                "address": merchant_address,
                "tel": merchant_tel,
                "time": merchant_time,
                "regular_holiday": merchant_regular_holiday,
                "lat": lat,
                "lng": lng
            })
            merchants["names"].append(merchant_name)

    return {"merchants": merchants, "findMerchants": findMerchants}

main()
