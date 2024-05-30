# Generated by Django 4.2.9 on 2024-02-25 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_paymenthistory_tahun'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenthistory',
            name='kubikasi_akhir',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='kubikasi_awal',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='kubikasi_total',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='sisa_pembayaran',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='tagihan_dibayar',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='tagihan_total',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='unique_id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]