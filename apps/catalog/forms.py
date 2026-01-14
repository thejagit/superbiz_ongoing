from django import forms

from .models.company import Company


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
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
