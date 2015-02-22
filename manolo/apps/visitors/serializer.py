from rest_framework import serializers
from rest_framework import pagination

from visitors.models import Visitor


class VisitorSerializer(serializers.ModelSerializer):
    """
    Serializes querysets.
    """
    class Meta:
        model = Visitor
        fields = ('full_name', 'entity', 'meeting_place', 'office', 'host_name',
                  'reason', 'institution', 'location', 'id_number', 'id_document',
                  'date', 'time_start', 'time_end',
                  )


class PaginatedBasicSearchSerializer(pagination.PaginationSerializer):
    """
    Serializes page objects of querysets.
    """
    class Meta:
        object_serializer_class = VisitorSerializer
