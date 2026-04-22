"""
URL configuration for quanlydangvien project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from qldv import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('chibo/', views.chibo, name='chibo'),
    path('chibo/them-moi/', views.chibo_add, name='chibo_add'),
    path('chibo/du-lieu/', views.chibo_data, name='chibo_data'),
    path('chibo/<int:chibo_id>/edit/', views.chibo_edit, name='chibo_edit'),
    path('chibo/<int:chibo_id>/delete/', views.chibo_delete, name='chibo_delete'),
    path('dangvien/', views.dangvien, name='dangvien'),
    path('dangvien/theo-doi-bien-dong/', views.dangvien_structure, name='dangvien_structure'),
    path('dangvien/them-moi/', views.dangvien_add, name='dangvien_add'),
    path('dangvien/du-lieu/', views.dangvien_data, name='dangvien_data'),
    path('dangvien/<int:dangvien_id>/update-dien/', views.dangvien_update_dien, name='dangvien_update_dien'),
    path('dangvien/<int:dangvien_id>/edit/', views.dangvien_edit, name='dangvien_edit'),
    path('dangvien/<int:dangvien_id>/delete/', views.dangvien_delete, name='dangvien_delete'),
    path('huyhieu/', views.huyhieu, name='huyhieu'),
    path('huyhieu/them-moi/', views.huyhieu_add, name='huyhieu_add'),
    path('huyhieu/du-lieu/', views.huyhieu_data, name='huyhieu_data'),
    path('huyhieu/<int:huyhieu_id>/edit/', views.huyhieu_edit, name='huyhieu_edit'),
    path('huyhieu/<int:huyhieu_id>/delete/', views.huyhieu_delete, name='huyhieu_delete'),
    path('user/', views.user, name='user'),
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password_view, name='change_password'),
]
