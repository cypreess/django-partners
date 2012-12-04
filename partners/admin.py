from django.contrib import admin
from django.core import urlresolvers
from partners.models import Partner, PartnerAccount, PartnerIncome

class UserLinkMixin(object):
    def user_link(self, obj):
        change_url = urlresolvers.reverse('admin:auth_user_change', args=(obj.user.id,))
        return '<a href="%s">%s</a>' % (change_url, obj.user.username)

    user_link.short_description = 'User'
    user_link.allow_tags = True

class PartnerAccountAdmin(UserLinkMixin, admin.ModelAdmin):
    def partner_link(self, obj):
        change_url = urlresolvers.reverse('admin:auth_user_change', args=(obj.partner.id,))
        return '<a href="%s">%s</a>' % (change_url, obj.partner)
    partner_link.short_description = 'Partner'
    partner_link.allow_tags = True
    readonly_fields = ('partner_link', 'user_link')
    list_display = ('user', 'rate', 'expire', 'days_left', 'partner')
#    fields = ('user_link', 'rate', 'expire', 'days_left', 'partner_link', 'partner')
#    exclude = ('partner', 'user')

class PartnerIncomeAdmin(admin.ModelAdmin):
    def partner(self, obj):
        return unicode(obj.account.partner)
    list_display = ( 'account', 'partner', 'created', 'amount', 'currency')
    readonly_fields = ('account', 'partner')
    def queryset(self, request):
        return super(PartnerIncomeAdmin, self).queryset(request).select_related()


class PartnerAdmin(UserLinkMixin, admin.ModelAdmin):
    readonly_fields = ('user_link',)
    exclude = ('user', )

admin.site.register(Partner, PartnerAdmin)
admin.site.register(PartnerAccount, PartnerAccountAdmin)
admin.site.register(PartnerIncome, PartnerIncomeAdmin)

