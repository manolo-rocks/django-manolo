from rest_framework import serializers
from rest_framework import pagination

from visitors.models import Visitor


class VisitorSerializer(serializers.ModelSerializer):
    """
    Serializes querysets.
    """
    class Meta:
        model = Visitor


class PaginatedVisitorSerializer(pagination.PaginationSerializer):
    """
    Serializes page objects of querysets.
    """
    class Meta:
        object_serializer_class = VisitorSerializer
