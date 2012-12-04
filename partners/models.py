from datetime import date
from django.db import models
from django.db.models import Q

# Create your models here.

class Partner(models.Model):
    user = models.OneToOneField('auth.User')

    def __unicode__(self):
        return unicode(self.user)

    @classmethod
    def exist(cls, user):
        """
        Checks if user is a partner. Return Partner object on success (which validate to True),
        or False if not.
        """
        try:
            return cls.objects.get(user=user)
        except cls.DoesNotExist:
            return False


class ValidAccountManager(models.Manager):
    """
    Selects only accounts that are valid, i.e.:

    * are not expired due to a given time
    * are not expired due to days of account validity
    """

    def get_query_set(self):
        return super(ValidAccountManager, self).get_query_set().filter(
            (Q(expire=None) | Q(expire__gte=date.today())) & (Q(days_left=None) | Q(days_left__gt=0))
        )


class PartnerAccount(models.Model):
    partner = models.ForeignKey(Partner)
    user = models.ForeignKey('auth.User')
    rate = models.DecimalField(max_digits=3, decimal_places=1, default='10.00')
    expire = models.DateField(blank=True, null=True, db_index=True)
    days_left = models.IntegerField(blank=True, null=True, db_index=True)

    objects = models.Manager()
    valid_objects = ValidAccountManager()

    def __unicode__(self):
        return unicode(self.user)




class PartnerIncome(models.Model):
    account = models.ForeignKey(PartnerAccount)
    created = models.DateField(db_index=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=3, default='EUR')
    description = models.CharField(max_length=250, blank=True, null=True)
    period = models.IntegerField(blank=True, null=True)


#noinspection PyUnresolvedReferences
import partners.listeners