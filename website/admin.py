from django.contrib import admin
from .models import User, PaymentHistory, AboutInformation

# Register your models here.

admin.site.register(User)

@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
  list_display = ("id", "bulan", "tanggal_pembayaran")

@admin.register(AboutInformation)
class AboutInformationAdmin(admin.ModelAdmin):
  list_display = ("id", "judul", "is_view")