from django.contrib import admin

from finance.models import Expenditure, Income

# Register your models here.
admin.site.register(Income)
admin.site.register(Expenditure)
