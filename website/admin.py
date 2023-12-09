from django.contrib import admin
from .models import User, PaymentHistory

# Register your models here.

admin.site.register(User)
admin.site.register(PaymentHistory)