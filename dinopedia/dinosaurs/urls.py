from rest_framework import routers
from .views import ReadDinosaurViewSet
from django.conf import settings
from django.conf.urls.static import static


router = routers.SimpleRouter(trailing_slash=False)
router.register("dinosaurs", ReadDinosaurViewSet)

urlpatterns = router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
