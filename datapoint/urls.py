from django.conf.urls import url, include

from rest_framework import routers

from datapoint import views


router = routers.DefaultRouter()
router.register(r'datapoints', views.DatapointViewSet)

urlpatterns = [
    url(r'', include(router.urls))
]
