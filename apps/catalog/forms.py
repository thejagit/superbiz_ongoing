from django import forms

from .models.company import Company
from .models.company_sale import CompanySale


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company #name of the model this should be same to model folder model name
        fields = [
            "company_code",
            "company_bpcode",
            "company_name",
            "address1",
            "address2",
            "email",
            "fax",
            "phone",
            "country_code",
            "currency_type",
            "currency_deci",
            "company_active",
            "defcompany",
        ]

class CompanySaleForm(forms.ModelForm):
    class Meta:
        model = CompanySale
        fields = ["company", "sales_code", "sales_id_name", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make these optional so the form saves even if you only use the grid
        self.fields["sales_code"].required = False
        self.fields["sales_id_name"].required = False