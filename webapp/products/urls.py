from django.conf.urls import include, url

from rest_framework import routers

from .views import ProductViewSet

router = routers.DefaultRouter()
router.register(r"products", ProductViewSet, basename="products_view_set")

urlpatterns = [
    url(r"^", include(router.urls)),
]
