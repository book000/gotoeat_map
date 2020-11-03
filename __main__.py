import importlib
import os
import datetime
import math

prefectures = [
    [
        "1_hokkaido",
        "2_aomori",
        "3_iwate",
        "4_miyagi",
        "5_akita",
        "6_yamagata"
    ], [
        "7_fukushima",
        "8_ibaraki",
        "9_tochigi",
        "10_gunma",
        "11_saitama",
        "12_chiba"
    ], [
        "13_tokyo",
        "14_kanagawa",
        "15_niigata",
        "16_toyama",
        "17_ishikawa",
        "18_fukui"
    ], [
        "19_yamanashi",
        "20_nagano",
        "21_gifu",
        "22_shizuoka",
        "23_aichi",
        "24_mie"
    ], [
        "25_shiga",
        "26_kyoto",
        "27_osaka",
        "28_hyogo",
        "29_nara",
        "30_wakayama"
    ], [
        "31_tottori",
        "32_shimane",
        "33_okayama",
        "34_hiroshima",
        "35_yamaguchi",
        "36_tokushima"
    ], [
        "37_kagawa",
        "38_ehime",
        "39_kochi",
        "40_fukuoka",
        "41_saga",
        "42_nagasaki"
    ], [
        "43_kumamoto",
        "44_oita",
        "45_miyazaki",
        "46_kagoshima",
        "47_okinawa"
    ]
]

dt = datetime.datetime.now()
print("Now datetime: {}".format(str(dt)))
print("Select prefecture group id: {}".format(str(math.floor(dt.hour / 3))))
print("Select prefectures: {}".format(
    ", ".join(prefectures[math.floor(dt.hour / 3)])))

for prefecture in prefectures[math.floor(dt.hour / 3)]:
    print(prefecture)
    prefecture_dir = os.path.dirname(
        os.path.abspath(__file__)) + "/" + prefecture
    if not os.path.exists(prefecture_dir):
        print("Not found")
        continue
    if not os.path.isdir(prefecture_dir):
        print("Not a directory")
    build = importlib.import_module("gotoeat_map." + prefecture + ".__main__")
    build.main()
