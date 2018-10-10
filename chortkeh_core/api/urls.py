from django.urls import path, include
from .views.account import GetToken, Account

# Account urls #
account = [
    path('', Account.as_view(), name='account'),
    path('get_token/', GetToken.as_view(), name='get_token'),
]

# Main urls #
urlpatterns = [
    path('account/', include(account)),
]
