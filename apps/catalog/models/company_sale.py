from django.db import models

from .company import Company


class CompanySale(models.Model):
   
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="sales")
    sales_code=models.CharField(max_length=10)
    sales_id_name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)

    class Meta:
        verbose_name = "CompanySale"
        verbose_name_plural = "CompanySales"
        
    def __str__(self):
        return f"{self.company.company_code}-{self.company.company_name} - {self.sales_id_name}" #name diplay in admin side db table
