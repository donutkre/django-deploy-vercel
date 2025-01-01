from django.urls import path
from .views import (
    TransactionList, 
    TransactionDetail, 
    FilterTransactionsView, 
    AggregateByUserView, 
    GroupedTransactionsView, 
    ExportTransactionsView
)

urlpatterns = [
    path('transactions/', TransactionList.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', TransactionDetail.as_view(), name='transaction-detail'),
    path('transactions/query/', FilterTransactionsView.as_view(), name='filter-transactions'),
    path('transactions/aggregate-by-user/', AggregateByUserView.as_view(), name='aggregate-by-user'),
    path('transactions/grouped/', GroupedTransactionsView.as_view(), name='grouped-transactions'),
    path('transactions/export/', ExportTransactionsView.as_view(), name='export-transactions'),
]
