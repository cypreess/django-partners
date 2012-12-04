# Create your views here.
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import Http404, HttpResponseRedirect
from django.views.generic import ListView, MonthArchiveView, TemplateView
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



class LastIncomeView(TemplateView):
    template_name = "partners/no_income.html"

    def get(self, request, *args, **kwargs):
        try:
            last_income = PartnerIncome.objects.filter(account__partner__user=self.request.user).order_by('-created')[0]
            return HttpResponseRedirect(reverse('partner_income', kwargs={'year': last_income.created.strftime('%Y') , 'month': last_income.created.strftime('%m')}))
        except IndexError:

            return super(LastIncomeView, self).get(request, *args, **kwargs)
