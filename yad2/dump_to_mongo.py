from bson.json_util import loads
from pymongo import MongoClient


def init_server(db_name, col):
    client = MongoClient()
    db = client[db_name]
    collection = db[col]
    return db, collection


def load_feeds_from_json(f_name):
    with open(f_name, "r") as f:
        res = loads(f.read())

    return res['feeds']


if __name__ == '__main__':
    db, collection = init_server(db_name="yad2_test_1", col="col1")
    ids = []

    docs = [
        "/Users/barzrihan/OneDrive/Documents/yad2/feeds_{}.json".format(i) for i in range(1, 23)
    ]

    for doc in docs:
        res = load_feeds_from_json(doc)
        # format all results into list of ids
        # ids.extend([str(_id['link_token']) + "\n" for _id in res])

        for item in res:
            collection.insert_one(item)

    # dump all ids into file
    # with open("all_ids.txt", "w") as f:
    #     f.writelines(ids)
