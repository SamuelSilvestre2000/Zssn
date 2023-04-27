from django.urls import path
from .views import SurvivorList, SurvivorDetail, TradeItems

urlpatterns = [
    path('survivors/', SurvivorList.as_view(), name='survivors'),
    path('survivors/<int:pk>/', SurvivorDetail.as_view(), name='survivor_detail'),
    path('survivors/trade/', TradeItems.as_view(), name='trade_items'),
]
