from elasticsearch import Elasticsearch

def search(name):
    es = Elasticsearch()
    res = es.search(index="great_db", q=name)

    records = []

    for i in res['hits']['hits']:
        if i['_score'] >= 2.0:
            record = [i['_score'], i['_source']['source'], name, i['_source']['raw_data']]
            records.append(record)

    return records


def search_list(input_filename):
    with open(input_filename, "r") as handle:
        names = handle.readlines()

    for name in names:
        name = name.strip()
        search(name)