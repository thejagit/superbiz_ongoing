from django.contrib import messages
from django.db import transaction
from django.db.models import Q
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
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        queryset = Company.objects.all().order_by("-id")  #

        if query:
            # logic to handle 'active' string search
            is_active_search = None
            if query.lower() == "active":
                is_active_search = True
            elif query.lower() == "inactive":
                is_active_search = False

            search_filter = (
                Q(company_code__icontains=query)
                | Q(company_name__icontains=query)
                | Q(company_bpcode__icontains=query)
            )

            if is_active_search is not None:
                search_filter |= Q(company_active=is_active_search)

            queryset = queryset.filter(search_filter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the current search query to the template for pagination links
        context["q"] = self.request.GET.get("q", "")
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        # If HTMX request, return the partial which now includes the pagination
        if request.headers.get("HX-Request"):
            return render(request, "finance/partials/ptbcompany.html", context)

        return self.render_to_response(context)
    
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
    model = CompanySale
    template_name = "finance/sales_list.html"
    context_object_name = "sales"

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        # Use select_related if 'company' is a foreign key to optimize queries
        queryset = CompanySale.objects.all().order_by("-created_at")
        #filtering status
        if query:
            is_active_search = None
            if query.lower() == "active":
                is_active_search = True
            elif query.lower() == "inactive":
                is_active_search = False

            search_filter = (
                Q(sales_code__icontains=query)
                | Q(sales_id_name__icontains=query)
                | Q(created_at__icontains=query)
            )

            if is_active_search is not None:
                search_filter |= Q(is_active=is_active_search)

            queryset = queryset.filter(search_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        return context

    def get(self, request, *args, **kwargs):
        # Let ListView handle the queryset and context generation
        self.object_list = self.get_queryset()

        # Check if it's an HTMX request
        if request.headers.get("HX-Request"):
            context = self.get_context_data()
            return render(request, "finance/partials/ptbsales.html", context)

        return super().get(request, *args, **kwargs)
    

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
