import arcgis_sdk

from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.contrib.postgres import fields as pg_fields
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from core_flavor import models as core_models
from core_flavor.shortcuts import camel_to_dashed

from model_utils import Choices
from polymorphic.models import PolymorphicModel
from taggit import models as taggit_models
from taggit.managers import TaggableManager

from . import fields
from . import managers
from . import settings as arcgis_settings


class Account(core_models.SoftDeletableModel,
              core_models.TimeStampedUUIDModel):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_('user'))

    expired = models.DateTimeField(null=True)
    data = pg_fields.JSONField()

    def __str__(self):
        return self.user.email

    def __dir__(self):
        return super().__dir__() + list(self.data.keys())

    def __getattribute__(self, attr):
        try:
            return super().__getattribute__(attr)
        except AttributeError:
            if not attr.startswith('_') and attr in self.data:
                return self.data[attr]
            raise

    def get_absolute_url(self):
        return reverse(
            'arcgis-marketplace-api:v1:account-detail', args=(self.id.hex,)
        )

    @property
    def social_auth(self):
        return self.user.social_auth.get(provider='arcgis')

    def client(self):
        return arcgis_sdk.ArcgisAPI(self.access_token)

    @property
    def api(self):
        if not hasattr(self, '_api'):
            if self.is_expired:
                self.refresh_expired_token()
            self._api = self.client()
        return self._api

    def refresh_expired_token(self):
        assert hasattr(settings, 'SOCIAL_AUTH_ARCGIS_KEY'), (
            'Settings var SOCIAL_AUTH_ARCGIS_KEY missing'
        )

        result = self.client().refresh_token(
            client_id=settings.SOCIAL_AUTH_ARCGIS_KEY,
            refresh_token=self.refresh_token
        )
        self.data['access_token'] = result['access_token']
        self.set_expiration(result['expires_in'])
        self.save()

    @property
    def is_expired(self):
        return self.expired + relativedelta(seconds=5) < timezone.now()

    def set_expiration(self, expires_in):
        self.expired = timezone.now() + relativedelta(seconds=expires_in)

    def me(self):
        data = self.api.user_detail(self.username)
        self.data.update(camel_to_dashed(data))
        self.save()
        return data

    def self(self):
        return self.api.self()

    @property
    def groups(self):
        return self.me()['groups']

    @property
    def featured_groups(self):
        return self.self()['featuredGroups']

    @property
    def subscription_type(self):
        return self.self()['subscriptionInfo']['type']


class GenericUUIDTaggedItem(taggit_models.CommonGenericTaggedItemBase,
                            taggit_models.TaggedItemBase):

    object_id = models.UUIDField(editable=False)


class Item(PolymorphicModel,
           core_models.SoftDeletableModel,
           core_models.TimeStampedUUIDModel):

    owner = models.ForeignKey(
        'Account',
        on_delete=models.CASCADE,
        verbose_name=_('owner'))

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    price = models.FloatField(_('price'), validators=[MinValueValidator(0)])

    objects = managers.ItemManager()
    tags = TaggableManager(blank=True, through=GenericUUIDTaggedItem)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'arcgis-marketplace-api:v1:product-detail', args=(self.id.hex,)
        )


class PurposeItem(Item):
    PURPOSES = Choices(
        ('ready_to_use', _('Ready to use')),
        ('configurable', _('Configurable')),
        ('self_configurable', _('Self configurable')),
        ('code_sample', _('Code sample')))

    purpose = models.CharField(_('purpose'), choices=PURPOSES, max_length=32)

    class Meta:
        abstract = True


class WebMapingApp(PurposeItem):
    APIS = Choices(
        ('javascript', _('Javascript')),
        ('flex', _('Flex')),
        ('silverlight', _('Silverlight')),
        ('web_adf', _('Web ADF')),
        ('other', _('Other')))

    api = models.CharField(_('api'), choices=APIS, max_length=32)
    file = fields.CompressField(
        upload_to=core_models.UUIDUploadTo(
            arcgis_settings.ARCGIS_UPLOAD_ITEM_TO
        )
    )
