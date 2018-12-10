import json
import os
import re

import requests

headers = {
    "Host": "www.yad2.co.il",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9,he;q=0.8",
    "Cookie": "y2018-2-cohort=90; y2018-2-access=true; use_elastic_search=1; _ga=GA1.3.238762837.1544441703; _gid=GA1.3.1497888994.1544441703; PHPSESSID=3a4daf84ad73028868fc36a651c74c46; fitracking_12=no; __gads=ID=9839c78fc20ffef1:T=1544441656:S=ALNI_MYXGPpuyPojVD4RM4_G4GyrK1bk4w; TS011ed9fa=01cdef7ca22ba61476b4cd131f1629d7d806861c1ffddf352a867b0f521ca618f633a58786bec7bbca11f81b0692a0cbf3dad33405054d9206da74d43c06de954c028b892311864321aa9b6ca652700da35b0177d3; SPSI=146c1ae28ca53f4374aaeaccef952d90; sbtsck=jav; UTGv2=h4bc5bcf4bdd24a24ccdf8ffc82301382c29; yad2_session=3HqzL7EtMaR8Khl49Xn39DSsHc9KO3Bm8mpV3u6P; fi_utm=direct%7Cdirect%7C%7C%7C%7C; PRLST=PL; favorites_userid=chi6410618182; adOtr=1c4a126Beac; historyprimaryarea=sharon_area; historysecondaryarea=raanana_kfar_saba; yad2upload=520093706.38005.0000; BetterJsPop0=1; y1-site=_in_x1_b_285_s_nad_pop_1rashy_rotemshany; spcsrf=ed41e68e84df220c7c617231be6e46df"
}

url = "http://www.yad2.co.il/api/item/{id}"
url1 = "http://www.yad2.co.il/api/item/{id}/additionalinfo"


def gen_file(feeds):
    f_name = "feeds_add_1.json"
    while os.path.exists(f_name):
        num = re.match(r".+_([\d]+).+", f_name).group(1)
        f_name = f_name.replace(num, str(int(num) + 1))

    with open(f_name, "a") as f:
        json.dump({"feeds": feeds}, f, ensure_ascii=False)


if __name__ == '__main__':
    feed = []

    NUMBER_OF_FILES = 50
    NUMBER_OF_PAGES_PER_FILE = 100

    ids = []
    with open("all_ids.txt", "r") as f:
        ids.extend(f.read().splitlines())

    for i, _id in enumerate(ids, 1):
        res = requests.get(url.format(id=_id), headers=headers)
        res1 = requests.get(url1.format(id=_id), headers=headers)
        try:
            items = res.json()
            items1 = res1.json()
            if isinstance(items, dict) and items.get("status_code") == 400:
                # in case it is an ad.. e.g. status code for id: 0rucxs, for item:
                #   {'api_version': 1, 'data': {'codeError': 5,
                #   'redirectLink': '//www.yad2.co.il/realestate/brokerage-sales/apartment-lev-motzkin,-bne-beitcha-in-kiryat-motskin?location_type=2&city=8200&neighborhood=366&HomeTypeID=1&price=500000--1',
                #   'otherData': {'catID': 2, 'subCatID': 5}}, 'status_code': 400,
                #   'error_message': 'UN_ACTIVE_STATUS', 'server_number': 98,
                #   'categoryDic': {'catEn': None, 'subCatEn': None}, 'yad1Ads': [],
                #   'agency_more_items': [], 'educational_info': [], 'pricelist_articles': [],
                #   'rating_area': []}
                print(f"status code for id: {_id}, for item: {items}")
                continue
        except json.JSONDecodeError as e:
            err = "Whoops, looks like something went wrong"
            print(res.text)
            print(res1.text)
            if err in res.text or err in res1.text:
                continue
            raise ValueError(f"Error while parsing result for id {_id}, check if site have blocked the IP.")
        feed.append({
            _id: {
                "info": items,
                "additional_info": items1
            }
        })
        print("New Items Retrieved:", f"{i}/{len(ids)}")

        if i % NUMBER_OF_PAGES_PER_FILE == 0:
            # when gets to the number of page that the user wants, dump current feed to file
            gen_file(feed)
            feed = []
