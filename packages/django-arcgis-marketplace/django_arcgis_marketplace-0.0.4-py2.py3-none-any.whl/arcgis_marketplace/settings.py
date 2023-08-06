from django.conf import settings


ARCGIS_UPLOAD_ITEM_TO = getattr(
    settings,
    'ARCGIS_UPLOAD_ITEM_TO',
    'arcgis/items/%Y/%m/'
)

ARCGIS_REVERSE_EXTRA_KWARGS = getattr(
    settings,
    'ARCGIS_REVERSE_EXTRA_KWARGS',
    {}
)
