from django.contrib import messages
from django.db import transaction
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView  #

from apps.catalog.models.company import Company  #
from apps.catalog.models.company_sale import CompanySale

from .forms import CompanyForm, CompanySaleForm


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
        return super().form_valid(form) # data save to the db


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

class SaleListView(ListView):
    model = "CompanySale"

    template_name = "finance/sales_list.html"
    context_object_name = "sales"
    # Set the number of items per page (e.g., 10)
    paginate_by = 10
    
    def get_queryset(self):
        # This optimizes the query for the foreign key
       # Returns unique companies that have at least one active sale
        return (
            CompanySale.objects.all()
            .order_by("company__company_name")
        )
class CompanySaleCreateView(CreateView):

    model = CompanySale
    form_class = CompanySaleForm
    template_name = "finance/sales_create.html"
    success_url = reverse_lazy("catalog:sale_list")

    #get data from company-table
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get all data from company
        context["companies"] = Company.objects.all()
        return context
    
    def form_valid(self, form):
        # use a transaction so if one row fails, nothing is saved
        with transaction.atomic():
            # Save the main form (top fields)
            self.object = form.save()

            #Get the lists from the Alpine.js grid
            codes = self.request.POST.getlist("grid_sales_code[]")
            names = self.request.POST.getlist("grid_sales_name[]")
            statuses = self.request.POST.getlist("grid_sales_status[]")

            #Loop and create CompanySale objects for each row
            sales_to_create = []
            for i in range(len(codes)):
                # Convert 'true'/'false' string from Alpine to Python Boolean
                is_active = statuses[i].lower() == "true"

                sales_to_create.append(
                    CompanySale(
                        company=self.object.company,  # Linking to the same company
                        sales_code=codes[i],
                        sales_id_name=names[i],
                        is_active=is_active,
                    )
                )

            # Bulk create for better performance
            if sales_to_create:
                CompanySale.objects.bulk_create(sales_to_create)

        messages.success(self.request, "Sales and grid entries saved successfully!")
        return super().form_valid(form)
    # model = CompanySale
    # fields = ("company", "sales_code", "sales_id_name", "is_active")
    # #form_class = CompanySaleForm
    # template_name = "finance/sales_create.html"
    # success_url = reverse_lazy("catalog:sale_list")

    # #get data from company-table
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # get all data from company
    #     context["companies"] = Company.objects.all()
    #     return context
    # # This part runs if the data is valid
    # def form_valid(self, form):
    #     # save data
    #     return super().form_valid(form)
    
def get_company_sales_rows(request):
    company_id = request.GET.get("company")
    # Fetch sales for the selected company
    sales = CompanySale.objects.filter(company_id=company_id) if company_id else []

    return render(request, "finance/partials/sale_company.html", {"com_sales": sales})

class CompanySaleUpdateView(UpdateView):
    model = CompanySale
    form_class = CompanySaleForm
    template_name = "finance/sales_edit.html"  # Reuse your existing HTML
    success_url = reverse_lazy("catalog:sale_list")

    # get data from company-table
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # This is required so the dropdown has options to show
        context["companies"] = Company.objects.all()
        return context
    
class CompanySaleDeleteView(DeleteView):
    model = CompanySale
    # Redirect back to the list after deleting
    success_url = reverse_lazy("catalog:sale_list")
