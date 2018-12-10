from bson.json_util import loads


def load_feeds_from_json(f_name):
    with open(f_name, "r") as f:
        res = loads(f.read())

    return res['feeds']


if __name__ == '__main__':
    ids = []
    num_of_files = 23

    docs = [
        "feeds_{}.json".format(i) for i in range(1, num_of_files)
    ]
    for doc in docs:
        res = load_feeds_from_json(doc)
        # format all results into list of ids
        ids.extend([str(_id['link_token']) + "\n" for _id in res])

    # dump all ids into file
    with open("all_ids.txt", "w") as f:
        f.writelines(ids)
