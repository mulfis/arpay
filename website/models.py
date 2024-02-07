from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils import timezone

from .encryption import derive_key, encrypt_data, decrypt_data
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
    ## jangan tampilkan data penting secara mentah
    pemakaian_kubik_bulanan = models.IntegerField(blank=True, null=True)
    biaya_pemakaian_bulanan = models.IntegerField(blank=True, null=True)
    biaya_total_bulanan = models.IntegerField(blank=True, null=True)

    # encrypted here
    encrypted_pemakaian_kubik_bulanan = models.CharField(max_length=500, blank=True, null=True)
    encrypted_biaya_pemakaian_bulanan = models.CharField(max_length=500, blank=True, null=True)
    encrypted_biaya_total_bulanan = models.CharField(max_length=500, blank=True, null=True)

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

    def save(self, *args, **kwargs):
        self.hitung_pemakaian_bulanan()
        self.hitung_total_bulanan()
        self.encrypt_pemakaian_kubik_bulanan()
        # print(f"Encrypted data: {self.encrypted_pemakaian_kubik_bulanan}")
        self.encrypt_biaya_pemakaian_bulanan()
        # print(f"Encrypted data: {self.encrypted_biaya_pemakaian_bulanan}")
        self.encrypt_biaya_total_bulanan()
        # print(f"Encrypted data: {self.encrypted_biaya_total_bulanan}")
        super().save(*args, **kwargs)

    # DATA PEMAKAIAN KUBIK BULANAN
    def hitung_pemakaian_bulanan(self):
        if self.pemakaian_kubik_bulanan is not None:
            self.biaya_pemakaian_bulanan = int(self.pemakaian_kubik_bulanan) * 5500

    def hitung_total_bulanan(self):
        if self.pemakaian_kubik_bulanan is not None:
            if self.pemakaian_kubik_bulanan < 0 or self.pemakaian_kubik_bulanan > 15:
                self.biaya_total_bulanan = self.biaya_pemakaian_bulanan
            else:
                self.biaya_total_bulanan = int(self.biaya_pemakaian_bulanan) + 20000

    def encrypt_pemakaian_kubik_bulanan(self):
        # Check if the field is not already encrypted to avoid re-encryption
        if self.pemakaian_kubik_bulanan is not None and self.encrypted_pemakaian_kubik_bulanan is None:
            key = derive_key(self.password)
            encrypted_data = encrypt_data(str(self.pemakaian_kubik_bulanan), key)
            self.encrypted_pemakaian_kubik_bulanan = encrypted_data
        elif self.pemakaian_kubik_bulanan is not None and self.encrypted_pemakaian_kubik_bulanan is not None:
            key = derive_key(self.password)
            encrypted_data = encrypt_data(str(self.pemakaian_kubik_bulanan), key)
            self.encrypted_pemakaian_kubik_bulanan = encrypted_data

    def get_decrypted_pemakaian_kubik_bulanan(self):
        # Decrypt the data only if it's encrypted
        if self.encrypted_pemakaian_kubik_bulanan is not None:
            key = derive_key(self.password)
            decrypted_data = decrypt_data(self.encrypted_pemakaian_kubik_bulanan, key)
            return int(decrypted_data)
        else:
            # If not encrypted, return the original data
            return self.pemakaian_kubik_bulanan
    
    # DATA BIAYA PEMAKAIAN BULANAN
    def encrypt_biaya_pemakaian_bulanan(self):
        # Check if the field is not already encrypted to avoid re-encryption
        if self.biaya_pemakaian_bulanan is not None and self.encrypted_biaya_pemakaian_bulanan is None:
            key = derive_key(self.password)
            encrypted_data = encrypt_data(str(self.biaya_pemakaian_bulanan), key)
            self.encrypted_biaya_pemakaian_bulanan = encrypted_data
        elif self.biaya_pemakaian_bulanan is not None and self.encrypted_biaya_pemakaian_bulanan is not None:
            key = derive_key(self.password)
            encrypted_data = encrypt_data(str(self.biaya_pemakaian_bulanan), key)
            self.encrypted_biaya_pemakaian_bulanan = encrypted_data

    def get_decrypted_biaya_pemakaian_bulanan(self):
        # Decrypt the data only if it's encrypted
        if self.encrypted_biaya_pemakaian_bulanan is not None:
            key = derive_key(self.password)
            decrypted_data = decrypt_data(self.encrypted_biaya_pemakaian_bulanan, key)
            return int(decrypted_data)
        else:
            # If not encrypted, return the original data
            return self.pemakaian_kubik_bulanan

    # DATA BIAYA TOTAL BULANAN
    def encrypt_biaya_total_bulanan(self):
        # Check if the field is not already encrypted to avoid re-encryption
        if self.biaya_total_bulanan is not None and self.encrypted_biaya_total_bulanan is None:
            key = derive_key(self.password)
            encrypted_data = encrypt_data(str(self.biaya_total_bulanan), key)
            self.encrypted_biaya_total_bulanan = encrypted_data
        elif self.biaya_total_bulanan is not None and self.encrypted_biaya_total_bulanan is not None:
            key = derive_key(self.password)
            encrypted_data = encrypt_data(str(self.biaya_total_bulanan), key)
            self.encrypted_biaya_total_bulanan = encrypted_data

    def get_decrypted_biaya_total_bulanan(self):
        # Decrypt the data only if it's encrypted
        if self.encrypted_biaya_total_bulanan is not None:
            key = derive_key(self.password)
            decrypted_data = decrypt_data(self.encrypted_biaya_total_bulanan, key)
            return int(decrypted_data)
        else:
            # If not encrypted, return the original data
            return self.pemakaian_kubik_bulanan

class PaymentHistory(models.Model):
    waktu_pencatatan = models.DateTimeField(default=timezone.now, primary_key=True)
    tanggal_pembayaran = models.CharField(max_length=50)
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

class AboutInformation(models.Model):
    judul = models.CharField(max_length=20)
    deskripsi = models.CharField(max_length=500, blank=True, null=True)
    pertanyaan = models.CharField(max_length=500, blank=True, null=True)
    jawaban = models.CharField(max_length=500, blank=True, null=True)
    is_view = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)