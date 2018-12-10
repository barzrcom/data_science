from pymongo import MongoClient

from yad2.yad2_utils import load_feeds_from_json


def init_server(db_name, col):
    client = MongoClient()
    db = client[db_name]
    collection = db[col]
    return db, collection


if __name__ == '__main__':
    db, collection = init_server(db_name="yad2_test_1", col="col1")
    num_of_files = 23

    docs = [
        "/Users/barzrihan/OneDrive/Documents/yad2/feeds_{}.json".format(i) for i in range(1, num_of_files)
    ]

    for doc in docs:
        res = load_feeds_from_json(doc)

        for item in res:
            collection.insert_one(item)
