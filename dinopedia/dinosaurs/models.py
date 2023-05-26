from django.db import models
from django.contrib.auth.models import User


def user_dinosaur_path(instance, filename):
    return "images/{0}/{1}".format(instance.dinosaur.name, filename)


class Favourite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Dinosaur(models.Model):
    class EatingClassification(models.TextChoices):
        HERBIVORE = "Herbivore"
        OMNIVORE = "Omnivore"
        CARNIVORE = "Carnivore"

    class Colour(models.TextChoices):
        BROWN = "Brown"
        GREEN = "Green"

    class Period(models.TextChoices):
        TRIASSIC = "Triassic"
        JURASIC = "Jurassic"
        CRETACEOUS = "Cretaceous"
        PALEOGENE = "Paleogene"
        NEOGENE = "Neogene"

    class AverageSize(models.TextChoices):
        TINY = "T"
        EXTRA_SMALL = "XS"
        SMALL = "S"
        MEDIUM = "M"
        LARGE = "L"
        VERY_LARGE = "XL"

    name = models.CharField(max_length=255, unique=True)
    eating_classification = models.CharField(
        max_length=255,
        choices=EatingClassification.choices,
        default=EatingClassification.HERBIVORE,
    )
    colour = models.CharField(
        max_length=255, choices=Colour.choices, default=Colour.BROWN
    )
    period = models.CharField(
        max_length=255, choices=Period.choices, default=Period.JURASIC
    )
    size = models.CharField(
        max_length=2, choices=AverageSize.choices, default=AverageSize.MEDIUM
    )
    favourite = models.ForeignKey(
        Favourite, on_delete=models.DO_NOTHING, null=True, blank=True
    )

    def __str__(self):
        return self.name


class Picture(models.Model):
    dinosaur = models.ForeignKey(
        Dinosaur, on_delete=models.CASCADE, to_field="name"
    )
    image = models.ImageField(
        upload_to=user_dinosaur_path,
        null=True,
    )
