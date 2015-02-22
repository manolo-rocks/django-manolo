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
    start_index = serializers.SerializerMethodField('get_start_index')
    end_index = serializers.SerializerMethodField('get_end_index')
    num_pages = serializers.Field(source='paginator.num_pages')

    class Meta:
        object_serializer_class = VisitorSerializer

    def get_start_index(self, page):
        return page.start_index()

    def get_end_index(self, page):
        return page.end_index()

    def get_curr_index(self, page):
        return page.number
