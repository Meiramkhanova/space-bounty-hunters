from rest_framework import serializers

from .models import HuntLog, WantedCriminal


class WantedCriminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = WantedCriminal
        fields = [
            "id",
            "name",
            "nickname",
            "reward",
            "latitude",
            "longitude",
            "location_note",
            "difficulty",
            "armed",
            "has_crew",
            "escape_master",
        ]


class HuntLogSerializer(serializers.ModelSerializer):
    criminal_id = serializers.PrimaryKeyRelatedField(
        source="criminal",
        queryset=WantedCriminal.objects.all(),
    )

    class Meta:
        model = HuntLog
        fields = ["id", "criminal_id", "success", "notes", "created_at"]
        read_only_fields = ["id", "created_at"]
