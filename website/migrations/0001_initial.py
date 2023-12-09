# Generated by Django 4.2.7 on 2023-12-09 09:03

from django.db import migrations, models
import django.utils.timezone
import website.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentHistory',
            fields=[
                ('tanggal_pembayaran', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('id', models.CharField(max_length=10)),
                ('bulan', models.CharField(max_length=10)),
                ('kubikasi_awal', models.IntegerField()),
                ('kubikasi_akhir', models.IntegerField()),
                ('kubikasi_total', models.IntegerField()),
                ('tagihan_total', models.IntegerField()),
                ('tagihan_dibayar', models.IntegerField()),
                ('status_pembayaran', models.CharField(max_length=10)),
                ('sisa_pembayaran', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(blank=True, default='', max_length=10, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(blank=True, default='', max_length=255)),
                ('pictures', models.CharField(blank=True, default='', max_length=10)),
                ('status_bayar', models.CharField(blank=True, default='', max_length=10)),
                ('status_mesin', models.CharField(blank=True, default='', max_length=10)),
                ('status_kependudukan', models.CharField(blank=True, default='', max_length=10)),
                ('pemakaian_kubik_bulanan', models.IntegerField(blank=True, default='')),
                ('biaya_pemakaian_bulanan', models.IntegerField(blank=True, default='')),
                ('biaya_total_bulanan', models.IntegerField(blank=True, default='')),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', website.models.CustomUserManager()),
            ],
        ),
    ]
