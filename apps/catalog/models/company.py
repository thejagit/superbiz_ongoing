from django.db import models


class Company(models.Model):
    company_code = models.CharField(max_length=10, blank=True, null=True)
    company_bpcode = models.CharField(max_length=10, blank=True, null=True)
    company_name = models.CharField(max_length=255)
    address1 = models.TextField(blank=True, null=True)
    address2 = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    fax= models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    country_code = models.CharField(max_length=20, blank=True, null=True)
    currency_type = models.CharField(max_length=20, blank=True, null=True)
    currency_deci = models.SmallIntegerField(blank=True, null=True)
    company_active=models.BooleanField(default=True)
    defcompany = models.BooleanField(default=False)
    image=models.ImageField(upload_to="company",blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        
    def __str__(self):
        return self.company_name