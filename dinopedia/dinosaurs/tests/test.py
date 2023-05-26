from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from dinosaurs.models import Dinosaur, Favourite
from django.contrib.auth.models import User
from io import BytesIO


class TestCase(APITestCase):
    def test_list_dinosaurs(self):
        Dinosaur.objects.create(
            name="Random",
            eating_classification="Herbivore",
            colour="Green",
            period="Paleogene",
            size="XL",
        )
        dinosaurs = Dinosaur.objects.all()
        url = reverse("dinosaur-list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(dinosaurs.count(), len(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_dinosaur(self):
        Dinosaur.objects.create(
            name="Random",
            eating_classification="Herbivore",
            colour="Green",
            period="Paleogene",
            size="XL",
        )
        dinosaurs = Dinosaur.objects.all()
        url = reverse("dinosaur-list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(dinosaurs.count(), len(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_favourite_dinos(self):
        user = User.objects.create(
            username="oji",
            email="a@b.com",
            password="ADMIN789",
            is_superuser=True,
        )
        self.client.force_authenticate(user=user)
        for n in range(6):
            Dinosaur.objects.create(
                name=f"Random_{n}",
                eating_classification="Herbivore",
                colour="Green",
                period="Paleogene",
                size="XL",
            )
        url = reverse("dinosaur-list")
        fav = Favourite.objects.create(user=user)
        fav_dino = Dinosaur.objects.get(name="Random_5")
        fav.dinosaur_set.add(fav_dino)
        response = self.client.get(url, {"favourite": "true"})
        data = response.json()
        self.assertEqual(1, len(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for k, v in data[0].items():
            self.assertEqual(data[0][k], getattr(fav_dino, k))

    def test_search_dino_by_attr(self):
        dino_brown = Dinosaur.objects.create(
            name="Brown One",
            eating_classification="Herbivore",
            colour="Brown",
            period="Paleogene",
            size="XL",
        )
        Dinosaur.objects.create(
            name="Random_0",
            eating_classification="Herbivore",
            colour="Green",
            period="Paleogene",
            size="XL",
        )
        dino_omni = Dinosaur.objects.create(
            name="Omnivore_one",
            eating_classification="Omnivore",
            colour="Green",
            period="Paleogene",
            size="XL",
        )
        url = reverse("dinosaur-list")
        response = self.client.get(url, {"colour": "Brown"})
        data = response.json()
        self.assertEqual(1, len(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]["name"], dino_brown.name)
        response = self.client.get(url, {"eating_classification": "Omnivore"})
        data = response.json()
        self.assertEqual(1, len(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data[0]["eating_classification"], dino_omni.eating_classification
        )

    def test_create_like(self):
        user = User.objects.create(
            username="oji",
            email="a@b.com",
            password="ADMIN789",
            is_superuser=True,
        )
        dino = Dinosaur.objects.create(
            name="Brown One",
            eating_classification="Herbivore",
            colour="Brown",
            period="Paleogene",
            size="XL",
        )
        assert not hasattr(user, "favourite")
        self.client.force_authenticate(user=user)
        url = reverse("dinosaur-update-dino-favourite", args=f"{dino.id}")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(getattr(user, "favourite"))
        self.assertIn(dino, user.favourite.dinosaur_set.all())

    def test_upload_image(self):
        # I haven't managed to successfully assert that file is saved to /media/
        # images and couldn't find anything related to it in documentation or
        # somewhere else.
        user = User.objects.create(
            username="oji",
            email="a@b.com",
            password="ADMIN789",
            is_superuser=True,
        )
        dino = Dinosaur.objects.create(
            name="Brown One",
            eating_classification="Herbivore",
            colour="Brown",
            period="Paleogene",
            size="XL",
        )
        self.client.force_authenticate(user=user)
        url = reverse("admin:dinosaurs_picture_add")
        f = BytesIO(b"Some mock jpg file")
        response = self.client.post(
            url, {"dinosaur": dino.name, "image": f}, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
