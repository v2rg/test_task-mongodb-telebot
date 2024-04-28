import pymongo


def get_documents(dt_from, dt_upto):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.test_task
    wages = db.dump_for_test_task

    pipeline = [{'dt': {'$gte': dt_from, '$lte': dt_upto}}, {'_id': False}]  # диапазон

    return wages.find(*pipeline)
