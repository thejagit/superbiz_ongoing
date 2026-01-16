from django.db import models


class Sale(models.Model):
    sales_code = models.CharField(max_length=25)
    sales_id_name=models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Sale"
        verbose_name_plural = "Sales"

    def __str__(self):
        return self.sales_id_name