import json

from django.core.management.base import BaseCommand
from django.db.models import Count
from visitors.models import Visitor, Statistic, Statistic_detail


class Command(BaseCommand):
    help = 'calculates the five people that visited the most'

    def handle(self, *args, **options):

        print("Doing calculations")
        run_statistics()


def run_statistics():
    all_visitor_names = Visitor.objects.all().values_list(
        "full_name", flat=True,
    )
    all_visitor_names_unique = set(all_visitor_names)
    print(len(all_visitor_names_unique))

    visitors = Visitor.objects.all().values_list(
        "full_name",
    ).annotate(
        the_count=Count("full_name"),
    ).order_by(
        '-the_count',
    )[:50]

    Statistic_detail.objects.all().delete()
    names_and_visits = []
    for visitor in visitors:
        visit = Statistic_detail(name=visitor[0], number_of_visits=visitor[1])
        names_and_visits.append(visit)
    Statistic_detail.objects.bulk_create(names_and_visits)

    ls = []
    data_dict = {"name": "Statistics", "children": ls}

    for i in visitors:
        dic = {"name": i[0], "children": []}
        ls.append(dic)
        institution = Visitor.objects.filter(
            full_name=i[0],
        ).values_list("institution").annotate(the_count=Count("institution"))
        for j in institution:
            dic_2 = {"name": j[0], "children": []}
            dic["children"].append(dic_2)

        nombre = [d for d in ls if d['name'] == i[0]]

        cuenta = 0
        while cuenta < len(institution):
            reason = Visitor.objects.filter(
                full_name=i[0],
                institution=institution[cuenta][0],
            ).values_list("reason").annotate(the_count=Count("reason"))
            for l in reason:
                dic_3 = {"name": l[0], "size": l[1]}
                nombre[0]['children'][cuenta]['children'].append(dic_3)
            cuenta += 1
    print(data_dict)
    print("Deleting data in Statistics")
    Statistic.objects.all().delete()

    print("Saving data to Statistics")
    Statistic.objects.create(data=json.dumps(data_dict))

    number_of_rows = Statistic.objects.all().count()
    print("Currently have {} rows in Statistics".format(number_of_rows))
