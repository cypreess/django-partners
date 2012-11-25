# Create your views here.
from django.db.models import Sum
from django.http import Http404
from django.views.generic import ListView, MonthArchiveView
from partners.models import PartnerAccount, PartnerIncome, Partner

class PartnerAccountsView(ListView):
    model = PartnerAccount
    template_name = "partners/accounts.html"

    def get_queryset(self):
        if not Partner.exist(self.request.user):
            raise Http404
        return super(PartnerAccountsView, self).get_queryset().filter(partner__user = self.request.user).select_related()

class PartnerIncomeView(MonthArchiveView):
    model = PartnerIncome
    date_field = 'created'
    month_format = '%m'
    template_name = 'partners/income.html'


    def get_dated_queryset(self, **lookup):
        if not Partner.exist(self.request.user):
            raise Http404
        return super(PartnerIncomeView, self).get_dated_queryset(**lookup).filter(
            account__partner__user=self.request.user).select_related()

    def get_context_data(self, **kwargs):
        context = super(PartnerIncomeView, self).get_context_data(**kwargs)
        context['total'] = self.get_dated_items()[1].values('currency').annotate(total=Sum('amount'))
        return context



