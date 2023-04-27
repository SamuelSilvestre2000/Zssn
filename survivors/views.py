from rest_framework import viewsets
from .models import Survivor, Item, Inventory
from .serializers import SurvivorSerializer, ItemSerializer, InventorySerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
#from .models import Survivor, Inventory
from .serializers import SurvivorSerializer, InventorySerializer

ITEM_POINTS = {
    'water': 4,
    'food': 3,
    'medication': 2,
    'ammunition': 1
} 

class SurvivorViewSet(viewsets.ModelViewSet):
    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

@api_view(['POST'])
@permission_classes([])
def trade_items(request):
    try:
        # Exemplo de dados esperados no corpo da solicitação:
        # {
        #     "trader1": 1,
        #     "trader2": 2,
        #     "trader1_offer": {"water": 2, "food": 1},
        #     "trader2_offer": {"ammunition": 8}
        # }
        trader1_id = request.data.get('trader1')
        trader2_id = request.data.get('trader2')
        trader1_offer = request.data.get('trader1_offer')
        trader2_offer = request.data.get('trader2_offer')

        if not (trader1_id and trader2_id and trader1_offer and trader2_offer):
            return Response("Missing data", status=status.HTTP_400_BAD_REQUEST)

        trader1 = Survivor.objects.get(pk=trader1_id)
        trader2 = Survivor.objects.get(pk=trader2_id)

        if trader1.infected or trader2.infected:
            return Response("Infected survivors cannot trade items.", status=status.HTTP_400_BAD_REQUEST)

        trader1_inventory = Inventory.objects.get(survivor=trader1)
        trader2_inventory = Inventory.objects.get(survivor=trader2)

        trader1_points = sum(ITEM_POINTS[item] * quantity for item, quantity in trader1_offer.items())
        trader2_points = sum(ITEM_POINTS[item] * quantity for item, quantity in trader2_offer.items())

        if trader1_points != trader2_points:
            return Response("Trade not balanced. Points must be equal on both sides.", status=status.HTTP_400_BAD_REQUEST)

        for item, quantity in trader1_offer.items():
            if getattr(trader1_inventory, item) < quantity:
                return Response(f"Trader 1 does not have enough {item}.", status=status.HTTP_400_BAD_REQUEST)

        for item, quantity in trader2_offer.items():
            if getattr(trader2_inventory, item) < quantity:
                return Response(f"Trader 2 does not have enough {item}.", status=status.HTTP_400_BAD_REQUEST)

        for item, quantity in trader1_offer.items():
            setattr(trader1_inventory, item, getattr(trader1_inventory, item) - quantity)
            setattr(trader2_inventory, item, getattr(trader2_inventory, item) + quantity)

        for item, quantity in trader2_offer.items():
            setattr(trader1_inventory, item, getattr(trader1_inventory, item) + quantity)
            setattr(trader2_inventory, item, getattr(trader2_inventory, item) - quantity)

        trader1_inventory.save()
        trader2_inventory.save()

        return Response("Trade completed successfully.", status=status.HTTP_200_OK)
    except Survivor.DoesNotExist:
        return Response("Survivor not found.", status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
