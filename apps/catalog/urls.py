from django.urls import path

from .views import CompanyListView

app_name = "catalog"

urlpatterns = [
    path('companies/', CompanyListView.as_view(), name='company_list'), 
]