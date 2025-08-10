from rest_framework import serializers

from visitors.models import Visitor


class ManoloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = (
            "full_name",
            "entity",
            "meeting_place",
            "office",
            "host_name",
            "reason",
            "institution",
            "location",
            "id_number",
            "id_document",
            "date",
            "time_start",
            "time_end",
        )
