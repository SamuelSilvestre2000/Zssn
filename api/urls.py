from django.urls import path
from .views import ItemList, SurvivorList, SurvivorDetail, TradeItems
from . import views


urlpatterns = [
    path('survivors/', SurvivorList.as_view(), name='survivors'),
    path('survivors/<int:pk>/', SurvivorDetail.as_view(), name='survivor_detail'),
    path('survivors/trade/', TradeItems.as_view(), name='trade_items'),
    path('items/', ItemList.as_view(), name='item_list'),

]


