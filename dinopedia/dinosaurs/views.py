from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Dinosaur, Favourite
from .serializers import DinosaurSerializer


class ReadDinosaurViewSet(
    viewsets.ReadOnlyModelViewSet, viewsets.GenericViewSet
):
    queryset = Dinosaur.objects.all()
    serializer_class = DinosaurSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "name",
        "eating_classification",
        "colour",
        "period",
        "size",
    ]

    def get_queryset(self):
        user = self.request.user
        if qs := super().get_queryset():
            if query_params := self.request.query_params:
                if favourite := query_params.get("favourite"):
                    if favourite == "true":
                        return qs.filter(favourite=user.favourite)
        return qs

    @action(detail=True, methods=["post", "delete"])
    def update_dino_favourite(self, request, pk=None):
        user = self.request.user
        dinosaur = self.get_object()
        if self.request.method == "POST":
            favourite, _ = Favourite.objects.get_or_create(user=user)
            favourite.dinosaur_set.add(dinosaur)
            favourite.save()
            return Response(status=status.HTTP_201_CREATED)
        favourite = get_object_or_404(Favourite, user=user)
        if not dinosaur.favourite:
            return Response(status=status.HTTP_404_NOT_FOUND)
        favourite.dinosaur_set.remove(dinosaur)
        favourite.save()
        dinosaur.favourite = None
        dinosaur.save(update_fields=["favourite"])
        return Response(status=status.HTTP_204_NO_CONTENT)
