import re


def search(name):
    es = None
    # TODO: implement django queryset search here
    if not es:
        return []
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


def shrink_url_in_string(my_string):
    """Identify URL and shrink it. Note that this will not be a short_url."""
    res = re.search("(https?://.+)$", my_string)
    if res:
        long_link = res.groups()[0]
        short_link = long_link[0:23]
        my_string_less_link = my_string.replace(long_link, "")
        my_new_string = "{0} <a href='{1}'>{2}...</a>".format(
            my_string_less_link,
            long_link,
            short_link,
        )
        return my_new_string
    else:
        return my_string
