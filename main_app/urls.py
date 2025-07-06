from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('babies/<int:baby_id>/', views.baby_detail, name='baby_detail'),
    path('babies/add/', views.add_baby, name='add_baby'),
    path('babies/<int:baby_id>/edit/', views.edit_baby, name='edit_baby'),
    path('babies/<int:baby_id>/delete/', views.delete_baby, name='delete_baby'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.update_user_profile, name='update_user_profile'),
    path('diapers/', views.diapers, name='diapers'),
    path('babies/<int:baby_id>/diapers/', views.diapers, name='diapers'),
    path('babies/<int:baby_id>/diapers/add/', views.add_diaper, name='add_diaper'),
    path('diapers/<int:diaper_id>/edit/', views.edit_diaper, name='edit_diaper'),
    path('diapers/<int:diaper_id>/delete/', views.delete_diaper, name='delete_diaper'),
    path('appointments/', views.appointments, name='appointments'),
    path('appointments/<int:baby_id>/', views.appointments, name='appointments'),
    path('appointments/<int:baby_id>/add/', views.add_appointment, name='add_appointment'),
    path('appointments/<int:appointment_id>/edit/', views.edit_appointment, name='edit_appointment'),
    path('appointments/<int:appointment_id>/delete/', views.delete_appointment, name='delete_appointment'),
    path('appointments/<int:appointment_id>/detail/', views.appointment_detail, name='appointment_detail'),
    path('medicines/', views.medicines, name='medicines'),
    path('medicines/<int:baby_id>/', views.medicines, name='medicines'),
    path('medicines/<int:baby_id>/add/', views.add_medicine, name='add_medicine'),
    path('medicines/<int:medicine_id>/edit/', views.edit_medicine, name='edit_medicine'),
    path('medicines/<int:medicine_id>/delete/', views.delete_medicine, name='delete_medicine'),
    path('feedings/', views.feedings, name='feedings'),
    path('feedings/<int:baby_id>/', views.feedings, name='feedings'),
    path('feedings/<int:baby_id>/add/', views.add_feeding, name='add_feeding'),
    path('feedings/<int:feeding_id>/edit/', views.edit_feeding, name='edit_feeding'),
    path('feedings/<int:feeding_id>/delete/', views.delete_feeding, name='delete_feeding'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])