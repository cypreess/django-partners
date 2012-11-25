from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from partners.views import PartnerAccountsView, PartnerIncomeView


urlpatterns = patterns('',
    url(r'^accounts/$', login_required(PartnerAccountsView.as_view()), name='partner_accounts'),
    url(r'^income/(?P<year>\d{4})/(?P<month>\d{2})/$', login_required(PartnerIncomeView.as_view()), name='partner_income'),

)
