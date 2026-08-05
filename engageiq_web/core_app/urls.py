from django.urls import path
from . import views
from django.urls import path
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
    path('api/predict-satisfaction/', views.predict_satisfaction_api, name='api_predict_satisfaction'),
    path('resend-code/', views.resend_verification_code, name='resend_verification_code'),
]