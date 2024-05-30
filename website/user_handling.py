from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import check_password

from .models import User, PaymentHistory, AboutInformation
from .encryption import derive_key, encrypt_data, decrypt_data

@login_required
def user_change_picture(request, pk):
    user = User.objects.get(pk=pk)
    alert = ""

    if request.method == 'POST':
        new_picture = request.FILES.get('new-picture')

        if new_picture:
            # Validate the uploaded image
            if not new_picture.content_type.startswith('image'):
                alert = "File harus berupa gambar."
            elif new_picture.size > 10 * 1024 * 1024:  # Example limit: 10MB
                alert = "Ukuran file tidak boleh lebih dari 10MB."
            else:
                # Save the new picture
                user.pictures = new_picture
                user.save()
                alert = "Gambar berhasil diperbaharui"
                return redirect('admin-account-detail', pk=pk)
        else:
            alert = "Gambar baru tidak ada"

    context = {
        'user': user,
        'alert': alert,
    }

    return redirect('admin-account-detail', context)

@login_required
def user_change_status(request, pk):
  if request.method == 'POST':
    user = User.objects.get(pk=pk)

    new_mesin = request.POST.get('status-mesin')
    new_kependudukan = request.POST.get('status-kependudukan')

    if new_mesin is not None and new_kependudukan is not None:
      user.status_mesin = new_mesin
      user.status_kependudukan = new_kependudukan
      user.save()
      alert = "Data status telah diperbaharui"
      return redirect('admin-account-detail', pk=pk)
    else:     
      alert = "Data status tidak valid"

    context = {
      'user': user,
      'alert': alert,
    }

  return redirect('admin-account-detail', context)

@login_required
def user_change_jabatan(request, pk):
  if request.method == 'POST':
    user = User.objects.get(pk=pk)

    new_is_active = request.POST.get('status-aktif')
    new_is_superuser = request.POST.get('status-superuser')

    user.is_active = new_is_active
    user.is_superuser = new_is_superuser
    user.save()

    return redirect('admin-account-detail', pk=pk)

  return redirect('admin-account-detail')


@login_required
def user_change_password(request, pk):
  if request.method == 'POST':
    user = User.objects.get(pk=pk)

    old_password = request.POST['old-password']
    new_password = request.POST['new-password']
    valid_password = request.POST['new-password-validation']

    if new_password != valid_password:
      alert = "Password dan Verifikasi Password tidak sama"

    if check_password(old_password, user.password):
      user.set_password(new_password)
      user.save()
      alert = "Password berhasil diperbaharui"
      return redirect('admin-account-detail', pk=pk)
    else:
      alert = "Password lama anda sepertinya salah"
    
  return redirect('admin-account-detail', alert)

@login_required
def user_change_data_bulan_ini(request, pk):
  if request.method == 'POST':
    user = User.objects.get(pk=pk)

    new_bulan_tagihan = request.POST.get('bulan-tagihan')
    new_tahun_tagihan = request.POST.get('tahun-tagihan')
    new_status_bayar = request.POST.get('status-bayar')
    new_pemakaian_kubik_bulanan = request.POST.get('pemakaian-kubik-bulanan')

    if new_bulan_tagihan != "" and new_tahun_tagihan != "" and new_status_bayar != "" and new_pemakaian_kubik_bulanan != "":
      user.bulan_tagihan = new_bulan_tagihan
      user.tahun_tagihan = new_tahun_tagihan
      user.status_bayar = new_status_bayar
      user.pemakaian_kubik_bulanan = int(new_pemakaian_kubik_bulanan)
      user.save()
      alert = "Data bulan ini berhasil diperbaharui"
      return redirect('admin-account-detail', pk=pk)
    else:
      alert = "Data tidak valid"

    context = {
      'alert': alert,
      'user': user,
    }

  return redirect('admin-account-detail', context)

@login_required
def user_change_data_riwayat(request, pk):
  if request.method == 'POST':
    history = PaymentHistory.objects.get(id=pk)

    u_id = request.POST.get('u-id')
    id = request.POST.get('id')
    bulan = request.POST.get('bulan')
    tahun = request.POST.get('tahun')
    tanggal_pembayaran = request.POST.get('tanggal-pembayaran')
    kubikasi_awal = request.POST.get('kubikasi-awal')
    kubikasi_akhir = request.POST.get('kubikasi-akhir')
    kubikasi_total = request.POST.get('kubikasi-total')
    tagihan_total = request.POST.get('tagihan-total')
    tagihan_dibayar = request.POST.get('tagihan-dibayar')
    status_pembayaran = request.POST.get('status-pembayaran')
    sisa_pembayaran = request.POST.get('sisa-pembayaran')

    if u_id == history.unique_id and u_id is not None:
      history.unique_id = u_id
      history.id = id
      history.bulan = bulan
      history.tahun = tahun
      history.tanggal_pembayaran = tanggal_pembayaran
      history.kubikasi_awal = kubikasi_awal
      history.kubikasi_akhir = kubikasi_akhir
      history.kubikasi_total = kubikasi_total
      history.tagihan_total = tagihan_total
      history.tagihan_dibayar = tagihan_dibayar
      history.status_pembayaran = status_pembayaran
      history.sisa_pembayaran = sisa_pembayaran
      history.save()
      alert = "Data Riwayat berhasil diperbaharui"
      return redirect('admin-account-detail', pk=pk)
    else:
      alert = "Unique id tidak valid, data gagal diperbaharui"

    context = {
      'alert': alert,
      'history': history,
    }

    return redirect('admin-account-detail', context)

@login_required
def user_add_data_riwayat(request, pk):
  if request.method == 'POST':
    history, created = PaymentHistory.objects.get_or_create(pk=pk)

    history.unique_id = request.POST.get('u-id')
    history.id  = request.POST.get('new-id')
    history.bulan = request.POST.get('new-bulan')
    history.tahun = request.POST.get('new-tahun')
    history.tanggal_pembayaran = request.POST.get('new-tanggal-pembayaran')
    history.kubikasi_awal = request.POST.get('new-kubikasi-awal')
    history.kubikasi_akhir = request.POST.get('new-kubikasi-akhir')
    history.kubikasi_total = request.POST.get('new-kubikasi-total')
    history.tagihan_total = request.POST.get('new-tagihan-total')
    history.tagihan_dibayar = request.POST.get('new-tagihan-dibayar')
    history.status_pembayaran = request.POST.get('new-status-pembayaran')
    history.sisa_pembayaran = request.POST.get('new-sisa-pembayaran')

    history.save()

    if created:
      alert = "Data Riwayat berhasil ditambahkan"
      return redirect('admin-account-detail', pk=pk)
    else:
      alert = "Unique id tidak valid, data gagal ditambahkan"

    context = {
      'alert': alert,
      'history': history,
    }

    return redirect('admin-account-detail', context)
  
@login_required
def delete_history_user(request, pk):
  if request.method == 'POST':
    item = PaymentHistory.objects.get(pk=pk)
    item.delete()

    relocate = item.id
    
    return redirect('admin-account-detail', pk=relocate)

  return redirect('admin-account-detail')