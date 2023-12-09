from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list-rumah/', views.items_list, name='items-list'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('accounts/logout/', views.logout, name='logout'),
    path('accounts/<pk>/details', views.account_detail, name='account-detail')

]