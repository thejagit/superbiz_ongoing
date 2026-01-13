from django.views.generic import ListView

from apps.catalog.models.company import Company


# Create your views here.
class CompanyListView(ListView):
    model = Company
    template_name = "finance/company_list.html"
    context_object_name = "companies"