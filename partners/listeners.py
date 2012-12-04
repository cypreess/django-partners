from datetime import date
from decimal import Decimal
from django.dispatch import receiver
from partners.signals import partner_income_signal

@receiver(partner_income_signal)
def partner_income_listener(sender, user, amount, currency, description="", period=None, **kwargs):
    from partners.models import PartnerIncome, PartnerAccount
    for partner_account in PartnerAccount.valid_objects.filter(user=user).select_related():
        PartnerIncome.objects.create(
            account=partner_account,
            created = date.today(),
            amount = (Decimal(amount) * (partner_account.rate/100)).quantize(Decimal('.01')),
            currency = currency.upper(),
            description = description,
            period = period,
        )
        if period and not partner_account.days_left is None:
            if partner_account.days_left - period > 0 :
                partner_account.days_left = partner_account.days_left - period
            else:
                partner_account.days_left = 0
            partner_account.save()
