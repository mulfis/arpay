from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils import timezone

# Create your models here.

class CustomUserManager(UserManager):
    def _create_user(self, id, password, **extra_fields):
        if not id:
            raise ValueError('The ID field must be set')
        user = self.model(id=id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, id=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(id, password, **extra_fields)
    
    def create_superuser(self, id=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(id, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=10, primary_key=True, blank=True, default='', unique=True)
    password = models.CharField(max_length=255, blank=True, default='')

    # personal data
    pictures = models.ImageField(upload_to='website/static/image/', blank=True, null=True)
    status_bayar = models.CharField(max_length=20, blank=True, default='')
    status_mesin = models.CharField(max_length=20, blank=True, default='')
    status_kependudukan = models.CharField(max_length=20, blank=True, default='')

    # payment status
    bulan_tagihan = models.CharField(max_length=20, blank=True, default='')
    tahun_tagihan = models.CharField(max_length=20, blank=True, default='')
    pemakaian_kubik_bulanan = models.IntegerField(blank=True, null=True)
    biaya_pemakaian_bulanan = models.IntegerField(blank=True, null=True)
    biaya_total_bulanan = models.IntegerField(blank=True, null=True)

    # permissions and staff status
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.id

    def get_short_name(self):
        return self.id

class PaymentHistory(models.Model):
    tanggal_pembayaran = models.CharField(max_length=255, primary_key=True, unique=True)
    id = models.CharField(max_length=10)
    bulan = models.CharField(max_length=20)
    kubikasi_awal = models.IntegerField()
    kubikasi_akhir = models.IntegerField()
    kubikasi_total = models.IntegerField()

    #payment_status
    tagihan_total = models.IntegerField()
    tagihan_dibayar = models.IntegerField()
    status_pembayaran = models.CharField(max_length=20)
    sisa_pembayaran = models.IntegerField()