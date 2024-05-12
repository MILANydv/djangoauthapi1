from django.urls import path
from account.views import ExpenditureListView, IncomeListView, SendPasswordResetEmailView, UserChangePasswordView, UserLoginView, UserProfileView, UserRegistrationView, UserPasswordResetView,account_verify,VerifyPage,UserProfileUpdateView,UserDeleteView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('account-verify/<slug:token>/', account_verify, name='account_verify'),
    path('verifypage/', VerifyPage.as_view(), name='page'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('account/delete/', UserDeleteView.as_view(), name='account-delete'),
    path('income/', IncomeListView.as_view(), name='income-list'),
    path('expenditure/', ExpenditureListView.as_view(), name='expenditure-list'),
]
