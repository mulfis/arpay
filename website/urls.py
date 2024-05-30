from django.urls import path
from . import views, user_handling

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', views.admin, name='admin'),
    path('list-rumah/', views.items_list, name='items-list'),
    path('list-rumah/extends/', views.list, name='list'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('accounts/logout/', views.logout, name='logout'),
    path('accounts/<pk>/details/', views.account_detail, name='account-detail'),

    # admin page
    path('admin/download_csv/', views.download_csv, name='download-csv'),
    path('admin/extends/', views.admin_list, name='admin-list'),
    path('admin/<pk>/details/', views.admin_account_detail, name='admin-account-detail'),

    path('admin/<pk>/change-picture/', user_handling.user_change_picture, name='user-change-picture'),
    path('admin/<pk>/change-status/', user_handling.user_change_status, name='user-change-status'),
    path('admin/<pk>/change-jabatan/', user_handling.user_change_jabatan, name='user-change-jabatan'),
    path('admin/<pk>/change-password/', user_handling.user_change_password, name='user-change-password'),
    path('admin/<pk>/change-data-now/', user_handling.user_change_data_bulan_ini, name='user-change-data-bulan-ini'),
    path('admin/<pk>/change-data-riwayat/', user_handling.user_change_data_riwayat, name='user-change-data-riwayat'),
    path('admin/<pk>/add-data-riwayat/', user_handling.user_add_data_riwayat, name='user-add-data-riwayat'),

    path('admin/<pk>/details/delete', user_handling.delete_history_user, name='delete-history-user'),
]