from django.urls import path

from .views import (
    CompanyCreateView,
    CompanyDeleteView,
    CompanyListView,
    CompanySaleCreateView,
    CompanySaleDeleteView,
    CompanySaleUpdateView,
    CompanyUpdateView,
    SaleListView,
    get_company_sales_rows,
)

app_name = "catalog"

urlpatterns = [
    path("companies/", CompanyListView.as_view(), name="company_list"),
    path("companies/add/", CompanyCreateView.as_view(), name="company_create"),
    path("companies/edit/<int:pk>/", CompanyUpdateView.as_view(), name="company_edit"),
    path("companies/delete/<int:pk>/", CompanyDeleteView.as_view(), name="company_delete"),
    path("sales/", SaleListView.as_view(), name="sale_list"),
    path("sales/add/", CompanySaleCreateView.as_view(), name="company_sales_create"),
    path("ajax/get-sales-rows/", get_company_sales_rows, name="get_company_sales_rows"),
    path("sales/edit/<int:pk>/", CompanySaleUpdateView.as_view(), name="sales_edit"),
    path("sales/delete/<int:pk>/", CompanySaleDeleteView.as_view(), name="sales_delete"),
]