import requests
import os
from xml.etree import ElementTree
import json
import time

def getLatLng(address):
    lat, lng = getLatLngFromYahooAPI(address)
    if lat is None or lng is None:
        lat, lng = getLatLngFromGeocodingAPI(address)

    return lat, lng


def getLatLngFromYahooAPI(address):
    config = os.environ
    if os.path.exists(os.path.dirname(os.path.abspath(__file__)) + "/config.json"):
        config = json.load(open(os.path.dirname(
            os.path.abspath(__file__)) + "/config.json"))

    responseJson = requests.get(
        "https://map.yahooapis.jp/geocode/V1/geoCoder?appid={appid}&output=json&results=1&recursive=true&query={query}".format(appid=config.get("YAHOO_APPID"), query=address))
    responseJson = responseJson.json()

    ################################### time.sleep(1)

    if not "Feature" in responseJson:
        return None, None

    return responseJson["Feature"][0]["Geometry"]["Coordinates"].split(",")[1], responseJson["Feature"][0]["Geometry"]["Coordinates"].split(",")[0]


def getLatLngFromGeocodingAPI(address):
    xml = requests.get(
        "https://www.geocoding.jp/api/?q=" + address)
    try:
        obj = ElementTree.fromstring(xml.text)
        if obj.find("coordinate") != None:
            lat = obj.find("coordinate").find("lat").text
            lng = obj.find("coordinate").find("lng").text
        else:
            lat = None
            lng = None
    except Exception as e:
        lat = None
        lng = None
    time.sleep(10)

    return lat, lng


def checkRemovedMerchant(merchants, findMerchants):
    print("----- Removed merchant check -----")

    removeMerchants = set(merchants["names"]) ^ set(findMerchants)
    print("removeMerchants size: " + str(len(removeMerchants)))

    for merchant in merchants["data"]:
        if merchant["name"] in removeMerchants:
            print("{name} removed".format(name=merchant["name"]))
            merchants["data"].remove(merchant)
            merchants["names"].remove(merchant["name"])

    print("merchant size: " + str(len(merchants["names"])))

    return merchants
