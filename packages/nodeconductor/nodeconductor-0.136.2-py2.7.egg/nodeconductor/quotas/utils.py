from django.apps import apps
from nodeconductor.quotas import models


def get_models_with_quotas():
    return [m for m in apps.get_models() if issubclass(m, models.QuotaModelMixin)]
