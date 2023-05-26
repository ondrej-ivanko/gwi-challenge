from rest_framework import serializers

from .models import Dinosaur


class DinosaurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dinosaur
        fields = (
            "id",
            "name",
            "eating_classification",
            "colour",
            "period",
            "size",
        )
        read_only_fields = ("id",)
