from django.urls import path

from .views import CompanyCreateView, CompanyDeleteView, CompanyListView, CompanyUpdateView

app_name = "catalog"

urlpatterns = [
    path("companies/", CompanyListView.as_view(), name="company_list"),
    path("companies/add/", CompanyCreateView.as_view(), name="company_create"),
    path("companies/edit/<int:pk>/", CompanyUpdateView.as_view(), name="company_edit"),
    path("companies/delete/<int:pk>/", CompanyDeleteView.as_view(), name="company_delete"),
]