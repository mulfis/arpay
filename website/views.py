from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import User, PaymentHistory

# Create your views here.

def home(request):
    return render(request, 'base.html')

def items_list(request):
    #excluding me 'roneks' as admin because im count as user too
    forbidden_user = User.objects.get(id='roneks')

    lists = User.objects.exclude(id=forbidden_user.id).order_by('id')
    return render(request, 'items_list.html', {'lists': lists})

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

    #check logged in user pk
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