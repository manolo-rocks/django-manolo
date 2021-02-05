from django import template

register = template.Library()


SORT_DIRECTIONS = {
    "asc": {"icon": "&uarr;", "inverse": "desc"},
    "desc": {"icon": "&darr;", "inverse": ""},
    "": {"icon": "", "inverse": "asc"},
}


@register.inclusion_tag("visitors/pagination.html", takes_context=True)
def show_pagination(context):
    """
    Note: Most of this custom template tag tag has been taken from repository
          https://github.com/ericflo/django-pagination

    Render the ``visitors/pagination.html`` template.

    Requires one argument, ``context``, which should be a dictionary-like data
    structure and must contain the following keys:

    ``paginator``
        A ``Paginator`` object.

    ``page``
        This should be the result of calling the page method on the
        previous Paginator object, given the current page.

    ``request``
        The current `HttpRequest` object. This is done by including
        the context processor `django.template.context_processors.request`

    """
    paginator = context['paginator']
    page = context['page']
    getvars = context['request'].GET.copy()
    if 'page' in getvars:
        del getvars['page']
    if len(getvars.keys()) > 0:
        getvars = '&%s' % getvars.urlencode()
    else:
        getvars = ''

    return {
        'paginator': paginator,
        'page': page,
        'getvars': getvars
    }


@register.inclusion_tag("visitors/sort_anchor.html", takes_context=True)
def sort_anchor(context, field, title):
    """
    Note: Most of this custom template tag tag has been taken from repository
          https://github.com/webstack/webstack-django-sorting

    Renders an <a> HTML tag with a link which href attribute
    includes the field on which we sort and the direction.
    and adds an up or down arrow if the field is the one
    currently being sorted on.

    Eg.
        {% anchor name Name %} generates
        <a href="?sort=name" title="Name">Name</a>

    """
    getvars = context['request'].GET.copy()
    if "sort" in getvars:
        sortby = getvars["sort"]
        del getvars["sort"]
    else:
        sortby = ""

    if "dir" in getvars:
        sortdir = SORT_DIRECTIONS.get(getvars["dir"], SORT_DIRECTIONS[""])
        del getvars["dir"]
    else:
        sortdir = SORT_DIRECTIONS[""]

    if sortby == field:
        getvars["dir"] = sortdir["inverse"]
        icon = sortdir["icon"]
    else:
        getvars["dir"] = "asc"
        icon = ""

    if getvars["dir"] == "":
        getvars.pop("dir", None)

    if len(getvars.keys()) > 0:
        urlappend = f"&{getvars.urlencode()}"
    else:
        urlappend = ""

    if icon:
        anchor_label = f"{title}&nbsp;{icon}"
    else:
        anchor_label = title

    if "dir" in getvars:
        anchor_href = f"?sort={field}{urlappend}"
    else:
        anchor_href = f"{'?' if urlappend else ''}{urlappend}"
    return {
        'anchor_title': title,
        'anchor_label': anchor_label,
        'anchor_href': anchor_href
    }
