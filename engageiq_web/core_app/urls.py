from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('register/', views.register_user, name='register'),
    path('verify-auth/', views.verify_otp, name='verify_otp'), # 🎯 THE OTP PORTAL LINK
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('features/', views.features_page, name='features'),
    path('analytics/', views.analytics_page, name='analytics'),
    path('pricing/', views.pricing_page, name='pricing'),
]