from django.urls import path
from finance.views import IncomeListCreateAPIView, IncomeRetrieveUpdateDestroyAPIView, ExpenditureListCreateAPIView, ExpenditureRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('income/', IncomeListCreateAPIView.as_view(), name='income-list'),
    path('income/<int:pk>/', IncomeRetrieveUpdateDestroyAPIView.as_view(), name='income-detail'),
    path('expenditure/', ExpenditureListCreateAPIView.as_view(), name='expenditure-list'),
    path('expenditure/<int:pk>/', ExpenditureRetrieveUpdateDestroyAPIView.as_view(), name='expenditure-detail'),
]
