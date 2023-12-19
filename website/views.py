from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import User, PaymentHistory

# Create your views here.

def home(request):
    return render(request, 'home.html')
    
def items_list(request):
    # excluding me 'roneks' as superuser because im count as user too
    lists = User.objects.exclude(is_superuser=True).order_by('id')
    return render(request, 'items_list.html', {'lists': lists})

def list(request):
    # excluding me 'roneks' as superuser because im count as user too
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
    return render(request, 'about.html')

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

    # check logged in user pk
    if logged_in_user_pk == pk:
        user_account = get_object_or_404(User, pk=pk)
        payment_history = PaymentHistory.objects.filter(id=pk).order_by('tanggal_pembayaran')
        return render(request, 'account_details.html', {'user_account': user_account, 'payment_history': payment_history})
    else:
        # Raise a PermissionDenied exception if the user doesn't have permission
        raise PermissionDenied("You don't have permission to access this account detail.")

@login_required
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('login')
    else:
        return redirect('login')