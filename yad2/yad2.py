import json
from time import sleep

import requests
import os

headers = {
    "Host": "www.yad2.co.il",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9,he;q=0.8",
    # TODO: the Cookie value should be replaced?
    "Cookie": "SPSI=89f1fae15fd8de3044179dfe94a1b9fd; y2018-2-cohort=96; y2018-2-access=true; sp_lit=jn1mJzoJeTdv5hNysPoohg==; PRLST=NP; UTGv2=h489a7611d9e761238303427d96105850f27; spcsrf=bea0962e9a40b823b61709188955c52f; use_elastic_search=1; _ga=GA1.3.52581383.1541233485; _gid=GA1.3.1194649072.1541233485; PHPSESSID=517aacde70e43abe3a2df5916715e342; yad2_session=CJY0FqHe3WuYHESG6oKqNuQ9RWMyOrHAjLh56pwi; yad2upload=520093706.38005.0000; favorites_userid=bgg2220263791; fitracking_12=no; fi_utm=direct%7Cdirect%7C%7C%7C%7C; __gads=ID=1bd39dfec2bf8349:T=1541233485:S=ALNI_MapEHD2DZUMzfmH8GvB6c7oJBrsaA; adOtr=fK9G81f5edf",
}
url = "http://www.yad2.co.il/api/pre-load/getFeedIndex/realestate/forsale?page={}"


def gen_file(feeds):
    f_name = "feeds.json"
    i = 1
    while os.path.exists(f_name):
        pre, suf = os.path.splitext(f_name)
        f_name = f"{pre}_{i}{suf}"
        i += 1

    with open(f_name, "a") as f:
        json.dump({"feeds": feeds}, f, ensure_ascii=False)


if __name__ == '__main__':
    feed = []

    NUMBER_OF_FILES = 10
    NUMBER_OF_PAGES_PER_FILE = 100
    DELAY_BETWEEN_GET = 5

    for i in range(1, NUMBER_OF_PAGES_PER_FILE * NUMBER_OF_FILES + 1):
        res = requests.get(url.format(i), headers=headers)
        try:
            items = res.json()['feed']['feed_items']
        except json.JSONDecodeError as e:
            raise ValueError("Error while parsing result, check if site have blocked the IP.")
        # slice items and retrieve only the values with an 'id' value
        items = [item for item in items if item.get('id')]
        feed.extend(items)
        print("New Items Retrieved:", len(items), "From page:", i)
        sleep(DELAY_BETWEEN_GET)

        if i % NUMBER_OF_PAGES_PER_FILE == 0:
            # when gets to the number of page that the user wants, dump current feed to file
            gen_file(feed)
            feed = []
