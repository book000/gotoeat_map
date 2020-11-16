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
            "https://goto-eat.weare.osaka-info.jp/gotoeat/page/{page}/?search_element_0_0=2&search_element_0_1=3&search_element_0_2=4&search_element_0_3=5&search_element_0_4=6&search_element_0_5=7&search_element_0_6=8&search_element_0_7=9&search_element_0_8=10&search_element_0_9=11&search_element_0_cnt=10&search_element_1_cnt=17&search_element_2_cnt=1&s_keyword_3&cf_specify_key_3_0=gotoeat_shop_address01&cf_specify_key_3_1=gotoeat_shop_address02&cf_specify_key_3_2=gotoeat_shop_address03&cf_specify_key_length_3=2&csp=search_add&feadvns_max_line_0=4&fe_form_no=0".format(page=page))
        soup = BeautifulSoup(html.content, "html.parser")
        lists = soup.find("div", {"class": "search_result_box"}).find(
            "ul").findChildren("li", recursive=False)
        if (len(lists) == 0):
            break
        for merchant in lists:
            merchant_name = merchant.find(
                "p", {"class": "name"}).text.strip()
            if merchant_name == "":
                print("Merchant nane is empty...?")
                continue

            rows = merchant.find("table").findChildren("tr")

            merchant_tel = None
            merchant_time = None
            merchant_regular_holiday = None
            for row in rows:
                th = row.find("th").text.strip()
                td = row.find("td").text.replace(u"\xa0", " ").strip()

                if th == "住所":
                    merchant_postal_code = td.split("\r\n")[0].strip()
                    merchant_address = td.split("\r\n")[1].replace(" ", "").strip()
                elif th == "TEL":
                    merchant_tel = td
                elif th == "営業時間" and td != "":
                    merchant_time = td
                elif th == "定休日" and td != "":
                    merchant_regular_holiday = td

            merchant_type = []
            tag_list = merchant.find("ul", {"class": "tag_list"}).findChildren("li", recursive=False)
            for tag in tag_list:
                merchant_type.append(tag.text.strip())

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
                "postal_code": merchant_postal_code,
                "time": merchant_time,
                "regular_holiday": merchant_regular_holiday,
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
