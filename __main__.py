import importlib
import os
import datetime
import math
import traceback
from github import Github


def createOrCommentIssue(title, content):
    g = Github(os.environ.get("TOKEN"))
    repo = g.get_repo(os.environ.get("GITHUB_REPOSITORY"))

    open_issues = repo.get_issues(state="open")
    for issue in open_issues:
        if issue.title == title:
            issue.create_comment(content)
            return

    repo.create_issue(title=title, body=content, assignee="book000")


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
    try:
        build = importlib.import_module(
            "gotoeat_map." + prefecture + ".__main__")
        build.main()
    except Exception as e:
        trace = traceback.format_exc()
        print(trace)
        traceLast = [x for x in trace.split("\n") if x][-1]
        createOrCommentIssue(
            "[" + prefecture + "] " + traceLast,
            "GitHub Run ID: `{github_run_id}`\nGitHub Run Number: `{github_run_number}`\nGitHub Action ID: `{github_action_id}`\nTrace: \n```\n{trace}\n```".format(
                github_run_id=os.environ.get("GITHUB_RUN_ID"),
                github_run_number=os.environ.get("GITHUB_RUN_NUMBER"),
                github_action_id=os.environ.get("GITHUB_ACTION"),
                trace=trace.strip()
            )
        )
