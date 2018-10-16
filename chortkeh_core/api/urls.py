from django.urls import path, include
from .views.account import GetToken, Account
from .views.wallet import WalletApiView
from .views.group import GroupApiView
from .views.transactions import (
    IncomeTransactionApiView, ExpenseTransactionApiView,
    TransferTransactionApiView
)
from .views.report import ReportIncomeApiView

# Account urls #
account = [
    path('', Account.as_view(), name='account'),
    path('get_token/', GetToken.as_view(), name='get_token'),
]

# Wallet urls #
wallet = [
    path('', WalletApiView.as_view(), name='wallet_api_view'),
    path('<int:pk>/', WalletApiView.as_view(), name='wallet_api_view_pk'),
]

# Group urls #
group = [
    path('', GroupApiView.as_view(), name='group_api_view'),
    path('<int:pk>/', GroupApiView.as_view(), name='group_api_view_pk'),
]

# Transaction urls #
transaction = [
    path('income/', IncomeTransactionApiView.as_view(), name='income_api_view'),
    path('income/<int:pk>/', IncomeTransactionApiView.as_view(),
         name='income_api_view_pk'),
    path('expense/', ExpenseTransactionApiView.as_view(), name='expense_api_view'),
    path('expense/<int:pk>/', ExpenseTransactionApiView.as_view(),
         name='expense_api_view_pk'),
    path('transfer/', TransferTransactionApiView.as_view(),
         name='transfer_api_view'),
    path('transfer/<int:pk>/', TransferTransactionApiView.as_view(),
         name='transfer_api_view_pk'),
]

# Report urls #
report = [
    path('income/<int:year>/',
         ReportIncomeApiView.as_view(), name='report_income_y'),
    path('income/<int:year>/<int:month>/',
         ReportIncomeApiView.as_view(), name='report_income_ym'),
    path('income/<int:year>/<int:month>/<int:day>/',
         ReportIncomeApiView.as_view(), name='report_income_ymd'),
]

# Main urls #
urlpatterns = [
    path('account/', include(account)),
    path('wallet/', include(wallet)),
    path('group/', include(group)),
    path('transaction/', include(transaction)),
    path('report/', include(report)),
]
