""" from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import SurvivorViewSet, ItemViewSet, InventoryViewSet
from .views import SurvivorViewSet, trade_items


router = DefaultRouter()
router.register(r'survivors', SurvivorViewSet, basename='survivors')
router.register(r'items', ItemViewSet, basename='items')
router.register(r'inventories', InventoryViewSet, basename='inventories')
urlpatterns = router.urls


urlpatterns = [
    path('api/survivors/', SurvivorViewSet.as_view({'get': 'list', 'post': 'create'}), name='survivors'),
    path('api/survivors/<int:pk>/', SurvivorViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='survivor_detail'),
    path('api/survivors/trade/', trade_items, name='trade_items'),
] """

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'survivors', views.SurvivorViewSet)
router.register(r'items', views.ItemViewSet)
router.register(r'inventories', views.InventoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('trade/', views.trade_items, name='trade_items'),
]