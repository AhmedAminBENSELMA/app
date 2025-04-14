from django.urls import include, path
from rest_framework import routers
from .views import Annex6aViewSet , AnnexViewSet

router = routers.DefaultRouter()
router.register(r'annex6a', Annex6aViewSet)
router.register(r'annex', AnnexViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
