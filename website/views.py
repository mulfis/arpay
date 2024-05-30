import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from .models import User, PaymentHistory, AboutInformation
from .encryption import derive_key, encrypt_data, decrypt_data


def home(request):
    return render(request, 'home.html')
    
def items_list(request):
    # excluding me as superuser because im count as user too
    lists = User.objects.exclude(is_superuser=True).order_by('id')
    return render(request, 'items_list.html', {'lists': lists})

def list(request):
    # excluding me as superuser because im count as user too
    lists = User.objects.exclude(is_superuser=True).order_by('id')

    query = request.GET.get('q', '')
    status_bayar = request.GET.get('status-bayar', '')
    status_mesin = request.GET.get('status-mesin', '')
    status_rumah = request.GET.get('status-rumah', '')

    if query:
        lists = lists.filter(id__icontains=query)

    if status_bayar == 'bayar-lunas':
        lists = lists.filter(status_bayar='LUNAS')
    elif status_bayar == 'bayar-belum-lunas':
        lists = lists.filter(status_bayar='BELUM LUNAS')
    elif status_bayar == 'bayar-nunggak':
        lists = lists.filter(status_bayar='DITANGGUHKAN')

    if status_mesin == 'mesin-bagus':
        lists = lists.filter(status_mesin='BAIK')
    elif status_mesin == 'mesin-rusak':
        lists = lists.filter(status_mesin='RUSAK')

    if status_rumah == 'rumah-diisi':
        lists = lists.filter(status_kependudukan='DIISI')
    elif status_rumah == 'rumah-kosong':
        lists = lists.filter(status_kependudukan='KOSONG')

    return render(request, 'list_partial.html', {'lists': lists})

def about(request):
    about_information = AboutInformation.objects.order_by('date_created')
    return render(request, 'about.html', {'about_information': about_information})

def login(request):
    if request.method == 'POST':
        id = request.POST['house_id']
        password = request.POST['house_pass']

        user = authenticate(request, username=id, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('account-detail', pk=user.pk)
        else:
            # Handle invalid login (display an error message, redirect, etc.)
            return render(request, 'login.html')
        
    if request.user.is_authenticated:
        return redirect('account-detail', pk=request.user.pk)

    return render(request, 'login.html')

@login_required    
def account_detail(request, pk):
    logged_in_user_pk = request.user.pk
    sha_pass = derive_key(request.user.password)

    # change pk to logged in user pk if system didnt in test
    # if logged_in_user_pk == pk:
    user_account = get_object_or_404(User, pk=pk)
    key = derive_key(user_account.password)

    decrypted_pemakaian_kubik_bulanan = user_account.get_decrypted_pemakaian_kubik_bulanan(key, sha_pass)
    decrypted_biaya_pemakaian_bulanan = user_account.get_decrypted_biaya_pemakaian_bulanan(key, sha_pass)
    decrypted_biaya_total_bulanan = user_account.get_decrypted_biaya_total_bulanan(key, sha_pass)
        # Kalau hacker mencoba backdoor dengan menghapus logged_in_user_pk atau menembus @login_required, maka kode dibawahnya akan hilang dan sama sekali tidak akan menjalankan get_decrypted, sedangkan kalau membobol langsung database maka hacker hanya akan mendapati encrypted_pemakaian sesuai yang ada di database berbentuk kode hash karena get_decrypted hanya ada di sini.

    payment_history = PaymentHistory.objects.filter(id=pk).order_by('tanggal_pembayaran')

    context = {
            'user_account': user_account, 
            'payment_history': payment_history, 
            'decrypted_pemakaian_kubik_bulanan': decrypted_pemakaian_kubik_bulanan, 
            'decrypted_biaya_pemakaian_bulanan': decrypted_biaya_pemakaian_bulanan, 
            'decrypted_biaya_total_bulanan': decrypted_biaya_total_bulanan
        }

    return render(request, 'account_details.html', context)
    # else:
    #     raise PermissionDenied("You don't have permission to access this account detail.")
    
@login_required
def download_csv(request):
    if 'csv_download' in request.POST:
        payment_history = PaymentHistory.objects.order_by('id')

        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="paymenthistory_data.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['Nomor Rumah', 'Bulan', 'Tahun', 'Tanggal Pembayaran','Kubik Air Awal','Kubik Air Akhir','Kubik Air Total','Total Tagihan', 'Uang Dibayarkan', 'Status Pembayaran', 'Sisa Pembayaran'])

        for list in payment_history:
            writer.writerow([list.id, list.bulan, list.tahun, list.tanggal_pembayaran, list.kubikasi_awal, list.kubikasi_akhir, list.kubikasi_total, list.tagihan_total, list.tagihan_dibayar, list.status_pembayaran, list.sisa_pembayaran])
        return response
    else:
        pass

@login_required
def admin(request):
    if request.user.is_superuser:
        payment_history = PaymentHistory.objects.order_by('id')
        user_account = request.user

        return render(request, 'admin.html', {'payment_history': payment_history, 'user_account': user_account})
    else:
        raise PermissionDenied("You don't have permission to access this page.")

@login_required
def admin_list(request):
    if request.user.is_superuser:
        payment_history = PaymentHistory.objects.order_by('id')
        
        query = request.GET.get('q', '')
        status_bayar = request.GET.get('status-bayar', '')
        bulan = request.GET.get('bulan', '')
        tahun = request.GET.get('tahun', '')

        if query:
            payment_history = payment_history.filter(id__icontains=query)
        
        if status_bayar == 'lunas':
            payment_history = payment_history.filter(status_pembayaran='LUNAS')
        elif status_bayar == 'belum-lunas':
            payment_history = payment_history.filter(status_pembayaran='BELUM LUNAS')
        elif status_bayar == 'ditangguhkan':
            payment_history = payment_history.filter(status_pembayaran='DITANGGUHKAN')

        if bulan == 'januari': payment_history = payment_history.filter(bulan='Januari')
        elif bulan == 'februari': payment_history = payment_history.filter(bulan='Februari')
        elif bulan == 'maret': payment_history = payment_history.filter(bulan='Maret')
        elif bulan == 'april': payment_history = payment_history.filter(bulan='April')
        elif bulan == 'mei': payment_history = payment_history.filter(bulan='Mei')
        elif bulan == 'juni': payment_history = payment_history.filter(bulan='Juni')
        elif bulan == 'juli': payment_history = payment_history.filter(bulan='Juli')
        elif bulan == 'agustus': payment_history = payment_history.filter(bulan='Agustus')
        elif bulan == 'september': payment_history = payment_history.filter(bulan='September')
        elif bulan == 'oktober': payment_history = payment_history.filter(bulan='Oktober')
        elif bulan == 'november': payment_history = payment_history.filter(bulan='November')
        elif bulan == 'desember': payment_history = payment_history.filter(bulan='Desember')

        if tahun == '2023':
            payment_history = payment_history.filter(tahun='2023')
        elif tahun == '2024':
            payment_history = payment_history.filter(tahun='2024')

        user_account = request.user

        return render(request, 'admin_partial.html', {'payment_history': payment_history, 'user_account': user_account})
    else:
        raise PermissionDenied("You don't have permission to access this page.")

@login_required
def admin_account_detail(request, pk):
    user = User.objects.get(id=pk)
    data = PaymentHistory.objects.filter(id=pk).order_by('waktu_pencatatan')

    return render(request, 'admin_account_details.html', {'user': user, 'data': data})

@login_required
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('login')
    else:
        return redirect('login')