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
url = "http://www.yad2.co.il/api/pre-load/getFeedIndex/realestate/forsale?page={}"


def gen_file(feeds):
    f_name = "feeds_1.json"
    while os.path.exists(f_name):
        num = re.match(r".+_([\d]+).+", f_name).group(1)
        f_name = f_name.replace(num, str(int(num) + 1))

    with open(f_name, "a") as f:
        json.dump({"feeds": feeds}, f, ensure_ascii=False)


if __name__ == '__main__':
    feed = []

    NUMBER_OF_FILES = 50
    NUMBER_OF_PAGES_PER_FILE = 100

    for i in range(1, NUMBER_OF_PAGES_PER_FILE * NUMBER_OF_FILES + 1):
        res = requests.get(url.format(i), headers=headers)
        try:
            items = res.json()['feed']['feed_items']
        except json.JSONDecodeError as e:
            print(res.text)
            raise ValueError("Error while parsing result, check if site have blocked the IP.")
        # slice items and retrieve only the values with an 'id' value
        items = [item for item in items if item.get('id')]
        feed.extend(items)
        print("New Items Retrieved:", len(items), "From page:", i)

        if i % NUMBER_OF_PAGES_PER_FILE == 0:
            # when gets to the number of page that the user wants, dump current feed to file
            gen_file(feed)
            feed = []
