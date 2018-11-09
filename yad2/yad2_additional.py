import json
import os
import random
import re
from time import sleep

import requests

headers = {
    "Host": "www.yad2.co.il",
    "Connection": "keep-alive",
    "X-MOD-SBB-CTYPE": "xhr",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "Referer": "http://www.yad2.co.il/realestate/forsale",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9,he;q=0.8",
    "Cookie": "y2018-2-cohort=73; y2018-2-access=false; PHPSESSID=nkk7eovjqffr1ocqg92j5jpo51; CLIENT_WIDTH_DIR=1440; MAIN_WIDTH_DIR=1440; __gads=ID=ff666bddbb1fbfb1:T=1541164288:S=ALNI_MYk3RiePydwS8hF__4-9hgK5j8m_w; _ga=GA1.3.929066615.1541164288; LPVID=MyOGUwNGEzZDMxNGY2ZDBl; LPSID-72457022=uin-CK9vTlOfyDZCKjpM2g; use_elastic_search=1; _gid=GA1.3.1937517107.1541755484; fitracking_12=no; historyprimaryarea=sharon_area; historysecondaryarea=raanana_kfar_saba; TS011ed9fa=01cdef7ca228548d7e39bc1277388f0b759dfe551586826876150faedec1d574aae8ff035b3d73c276db4d2501e53888ed6ef5ae273df8840b8d152832f9a17a689280e08d1fb4a0025e5893f4173f99de5891d1c5a7f4433aa6c2458d69683b5f8e3bb7779de22ce2d8768e4d2b8f92ce51676a4b; searchB144FromYad2=2_C_1971; SPSI=dd0b28999f2fb9f6a3c081304747be15; yad2_session=5ELnKmMPcot6cUAYeb2DD7Kj9A19NpIrpQ4hNSG4; fi_utm=direct%7Cdirect%7C%7C%7C%7C; UTGv2=h4bdf68b84301171aabd9ebf49717f118220; adOtr=2EdLd90992f; favorites_userid=bfa3370907863; _gat_UA-708051-1=1; spcsrf=9de63621f3dc03c85e765057ab5a1847; sp_lit=KFN4cLmrJ7h/aV6uBit0XA==; PRLST=; yad2upload=520093706.38005.0000; BetterJsPop0=1"
}
#
# "Host: www.yad2.co.il",
# "Connection: keep-alive",
# "X-MOD-SBB-CTYPE: xhr",
# "Accept: application/json, text/plain, */*",
# "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
# "Referer: http://www.yad2.co.il/realestate/forsale?city=8700&street=0407",
# "Accept-Encoding: gzip, deflate",
# "Accept-Language: en-US,en;q=0.9,he;q=0.8",
# "Cookie: y2018-2-cohort=73; y2018-2-access=false; PHPSESSID=nkk7eovjqffr1ocqg92j5jpo51; CLIENT_WIDTH_DIR=1440; MAIN_WIDTH_DIR=1440; __gads=ID=ff666bddbb1fbfb1:T=1541164288:S=ALNI_MYk3RiePydwS8hF__4-9hgK5j8m_w; _ga=GA1.3.929066615.1541164288; LPVID=MyOGUwNGEzZDMxNGY2ZDBl; LPSID-72457022=uin-CK9vTlOfyDZCKjpM2g; use_elastic_search=1; SPSI=33c1f81d5e695b1bcaa4b4d835a4797a; PRLST=YG; UTGv2=D-h4af1544dc3f17bd41e8bb0282625165f884; _gid=GA1.3.1937517107.1541755484; fitracking_12=no; fi_utm=direct%7Cdirect%7C%7C%7C%7C; favorites_userid=bfa3370907863; yad2_session=doD5ZDZCo3ELMWVp8DFaWsuhpMV66QlSzxOk4z7W; adOtr=fX38Xdc516e; spcsrf=ab57b7383f7e23ef54a3830e86eddea3; historyprimaryarea=sharon_area; historysecondaryarea=raanana_kfar_saba; yad2upload=536870922.38005.0000; BetterJsPop0=1; TS011ed9fa=01cdef7ca228548d7e39bc1277388f0b759dfe551586826876150faedec1d574aae8ff035b3d73c276db4d2501e53888ed6ef5ae273df8840b8d152832f9a17a689280e08d1fb4a0025e5893f4173f99de5891d1c5a7f4433aa6c2458d69683b5f8e3bb7779de22ce2d8768e4d2b8f92ce51676a4b",

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
    DELAY_BETWEEN_GET = (15, 30)

    ids = []
    with open("all_ids.txt", "r") as f:
        ids.extend(f.read().splitlines())

    for i, _id in enumerate(ids, 1):
        res = requests.get(url.format(id=_id), headers=headers)
        sleep(1)
        res1 = requests.get(url1.format(id=_id), headers=headers)
        try:
            items = res.json()
            items1 = res1.json()
            if items.get("status_code") == 400 or items1.get("status_code") == 400:
                print(f"status code for id: {_id}")
                sleep(random.randint(*DELAY_BETWEEN_GET))
                continue
        except json.JSONDecodeError as e:
            print(res.text)
            print(res1.text)
            raise ValueError(f"Error while parsing result for id {_id}, check if site have blocked the IP.")
        feed.append({
            _id: {
                "info": items,
                "additional_info": items1
            }
        })
        print("New Items Retrieved:", f"{i}/{len(ids)}")
        sleep(random.randint(*DELAY_BETWEEN_GET))

        if i % NUMBER_OF_PAGES_PER_FILE == 0:
            # when gets to the number of page that the user wants, dump current feed to file
            gen_file(feed)
            feed = []
