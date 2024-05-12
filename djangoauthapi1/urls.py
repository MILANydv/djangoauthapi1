from django.contrib import admin
from django.urls import path, include
from account.views import account_verify, VerifyPage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account-verify/<slug:token>/', account_verify, name='account_verify'),
    path('verifypage/', VerifyPage.as_view(), name='page'),
    path('api/user/', include('account.urls')),
]
