from django.conf.urls import include
from django.conf.urls import url

urlpatterns = [
    url(r'^', include(
        'arcgis_marketplace.urls',
        namespace='arcgis-marketplace')),

    url(r'^', include(
        'arcgis_marketplace.api.urls',
        namespace='arcgis-marketplace-api')),

    url(r'^paypal/', include('paypal.standard.ipn.urls'))
]
