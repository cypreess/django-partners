from django.contrib import admin
from partners.models import Partner, PartnerAccount, PartnerIncome

class PartnerAccountAdmin(admin.ModelAdmin):
    list_display = ('partner', 'user', 'rate', 'expire', 'days_left')


class PartnerIncomeAdmin(admin.ModelAdmin):
   list_display = ('partner', 'account', 'created', 'amount', 'currency', 'days_left')

admin.site.register(Partner)
admin.site.register(PartnerAccount)#, PartnerAccountAdmin)
admin.site.register(PartnerIncome)#, PartnerIncomeAdmin)

