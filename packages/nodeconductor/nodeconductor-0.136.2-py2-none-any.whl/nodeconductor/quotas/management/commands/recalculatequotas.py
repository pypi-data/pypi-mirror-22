from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.db import transaction

from nodeconductor.quotas import models, fields, exceptions
from nodeconductor.quotas.utils import get_models_with_quotas


class Command(BaseCommand):
    """ Recalculate all quotas """

    def handle(self, *args, **options):
        # TODO: implement other quotas recalculation
        # TODO: implement global stale quotas deletion
        self.delete_stale_quotas()
        self.init_missing_quotas()
        self.recalculate_global_quotas()
        self.recalculate_counter_quotas()
        self.recalculate_aggregator_quotas()
        self.stdout.write('XXX: Second time to make sure that aggregators of aggregators where calculated properly.')
        self.recalculate_aggregator_quotas()
        self.recalculate_customers_user_count()

    def delete_stale_quotas(self):
        self.stdout.write('Deleting stale quotas')
        for model in get_models_with_quotas():
            for obj in model.objects.all():
                quotas_names = model.QUOTAS_NAMES + [f.name for f in model.get_quotas_fields()]
                obj.quotas.exclude(name__in=quotas_names).delete()
        self.stdout.write('...done')

    def init_missing_quotas(self):
        self.stdout.write('Initializing missing quotas')
        for model in get_models_with_quotas():
            for obj in model.objects.all():
                for field in obj.get_quotas_fields():
                    try:
                        field.get_or_create_quota(scope=obj)
                    except exceptions.CreationConditionFailedQuotaError:
                        pass
        self.stdout.write('...done')

    def recalculate_global_quotas(self):
        self.stdout.write('Recalculating global quotas')
        for model in get_models_with_quotas():
            if hasattr(model, 'GLOBAL_COUNT_QUOTA_NAME'):
                with transaction.atomic():
                    quota, _ = models.Quota.objects.get_or_create(name=model.GLOBAL_COUNT_QUOTA_NAME)
                    quota.usage = model.objects.count()
                    quota.save()
        self.stdout.write('...done')

    def recalculate_counter_quotas(self):
        self.stdout.write('Recalculating counter quotas')
        for model in get_models_with_quotas():
            for counter_field in model.get_quotas_fields(field_class=fields.CounterQuotaField):
                for instance in model.objects.all():
                    counter_field.recalculate(scope=instance)
        self.stdout.write('...done')

    def recalculate_aggregator_quotas(self):
        # TODO: recalculate child quotas first
        self.stdout.write('Recalculating aggregator quotas')
        for model in get_models_with_quotas():
            for aggregator_field in model.get_quotas_fields(field_class=fields.AggregatorQuotaField):
                for instance in model.objects.all():
                    aggregator_field.recalculate(scope=instance)
        self.stdout.write('...done')

    # XXX: With current permissions structure it easier to handle customer quota separately.
    def recalculate_customers_user_count(self):
        self.stdout.write('Recalculating customers user count')
        from nodeconductor.structure.models import Customer
        for customer in Customer.objects.all():
            usage = len(set(customer.get_users()))
            customer.set_quota_usage(Customer.Quotas.nc_user_count, usage)
        self.stdout.write('...done')
