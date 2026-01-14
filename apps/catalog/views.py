from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView  #

from apps.catalog.models.company import Company  #

from .forms import CompanyForm


# Create your views here.
class CompanyListView(ListView):
    model = Company
    template_name = "finance/company_list.html"
    context_object_name = "companies"

class CompanyCreateView(CreateView):
    
    model = Company
    form_class = CompanyForm
    template_name = "finance/company_create.html" # Path  HTML file
    success_url = reverse_lazy("catalog:company_list") # Where to go after saving

    def form_valid(self, form):
       # is_active = request.POST.get("company_active") == "on"  # Checkboxes send 'on' if checked
        # This part runs if the data is valid
        # You can add custom logic here (like setting the user)
        return super().form_valid(form)


class CompanyUpdateView(UpdateView):

    model = Company
    form_class = CompanyForm
    template_name = "finance/company_edit.html"  # Reuse your existing HTML
    success_url = reverse_lazy("catalog:company_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class CompanyDeleteView(DeleteView):
    model = Company
    # Redirect back to the list after deleting
    success_url = reverse_lazy("catalog:company_list")