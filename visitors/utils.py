# -*- coding: utf-8 -*-
# The Paginator class has lines from the repository "Amy".
# Copyright (c) 2014-2015 Software Carpentry and contributors
import base64
import hashlib
from typing import Union

from django.core.paginator import Paginator as DjangoPaginator
import requests

from visitors.models import Subscriber

PAGINATOR_DIVIDER_THRESHOLD = 10


class Paginator(DjangoPaginator):
    """Everything should work as in django.core.paginator.Paginator, except
    this class provides additional generator for nicer set of pages."""

    _page_number = None

    def page(self, number):
        """Overridden to store retrieved page number somewhere."""
        self._page_number = number
        return super().page(number)

    def paginate_sections(self):
        """Divide pagination range into 3 sections.
        Each section should contain approx. 5 links.  If sections are
        overlapping, they're merged.
        The results might be:
        * L…M…R
        * LM…R
        * L…MR
        * LMR
        where L - left section, M - middle section, R - right section, and "…"
        stands for a separator.
        """
        index = int(self._page_number) or 1
        items = self.page_range

        # The number of pages is low, so we don't need to divide them.
        if items and items[-1] <= PAGINATOR_DIVIDER_THRESHOLD:
            return list(items)

        L = items[0:5]
        M = items[index-3:index+4] or items[0:index+1]
        R = items[-5:]
        L_s = set(L)
        M_s = set(M)
        R_s = set(R)

        D1 = L_s.isdisjoint(M_s)
        D2 = M_s.isdisjoint(R_s)

        if D1 and D2:
            # L…M…R
            pagination = list(L) + [None] + list(M) + [None] + list(R)
        elif not D1 and D2:
            # LM…R
            pagination = sorted(L_s | M_s) + [None] + list(R)
        elif D1 and not D2:
            # L…MR
            pagination = list(L) + [None] + sorted(M_s | R_s)
        else:
            # LMR
            pagination = sorted(L_s | M_s | R_s)

        return pagination


def fetch_and_save_avatar(user):
    email = user.email.encode("utf-8")
    email_hash = hashlib.md5()
    email_hash.update(email)
    url = "https://www.gravatar.com/{}.json".format(email_hash.hexdigest())
    r = requests.get(url)
    if r.json() == "User not found":
        img = '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'  # noqa
    else:
        thumbnail_url = [
            i['thumbnailUrl']
            for i in r.json()['entry']
        ][0]
        r = requests.get(thumbnail_url)
        img = base64.b64encode(r.content)
    s = Subscriber.objects.get(user=user)
    s.avatar = img
    s.save()


def is_dni(value: Union[str, int]) -> bool:
    value = value.strip()
    try:
        int(value)
    except ValueError:
        return False

    if len(value) >= 7:
        return True

    return False


def get_sort_field(request):
    """
    Retrieve field used for sorting a queryset
    :param request: HTTP request
    :return: the sorted field name, prefixed with "-" if ordering is descending
    """
    allowed_sort_fields = [
        'id', '-id', 'date', '-date', 'full_name', '-full_name',
        'id_number', '-id_number', 'entity', '-entity', 'reason', '-reason',
        'host_name', '-host_name', 'office', '-office', 'institution', '-institution'
    ]
    sort_direction = request.GET.get("dir")
    sort_field = (request.GET.get("sort") or "") if sort_direction else ""

    if sort_field not in allowed_sort_fields:
        sort_field = 'id'  # Default sort field if not specified or invalid

    sort_sign = "-" if sort_direction == "desc" else ""
    result_field = "{sign}{field}".format(sign=sort_sign, field=sort_field)
    return result_field
