from django.urls import path, include
from .views.account import GetToken, Account
from .views.wallet import WalletApiView
from .views.group import GroupApiView
from .views.transactions import IncomeTransactionApiView

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
    path('income/', IncomeTransactionApiView, name='income_api_view'),
    path('income/<int:pk>/',
         IncomeTransactionApiView, name='income_api_view_pk'),
]

# Main urls #
urlpatterns = [
    path('account/', include(account)),
    path('wallet/', include(wallet)),
    path('group/', include(group)),
    path('transaction/', include(transaction)),
]
