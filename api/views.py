from rest_framework import generics
from .models import Survivor, Item
from .serializers import SurvivorSerializer, ItemSerializer

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Survivor, Item, Inventory
#from .serializers import SurvivorSerializer
from .utils import create_survivor_with_items

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .trade import trade_items
import json


""" @api_view(['POST'])
def create_survivor(request):
    if request.method == 'POST':
        data = request.data

        item_data = [(item['name'], item['points'], item['quantity']) for item in data['items']]

        survivor = create_survivor_with_items(data['name'], data['age'], data['gender'], data['last_location_latitude'], data['last_location_longitude'], item_data)
        serializer = SurvivorSerializer(survivor)
        return JsonResponse(serializer.data, status=201)
 """

@api_view(['POST'])
def create_survivor(request):
    survivor_data = {
        "name": request.data["name"],
        "age": request.data["age"],
        "gender": request.data["gender"],
        "last_location_latitude": request.data["last_location_latitude"],
        "last_location_longitude": request.data["last_location_longitude"],
        "infected": False,
    }

    items_data = request.data.get("items", [])

    new_survivor = create_survivor_with_items(survivor_data=survivor_data, items_data=items_data)
    serializer = SurvivorSerializer(new_survivor)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


class SurvivorList(generics.ListCreateAPIView):
    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer

class SurvivorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer

class TradeItems(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        trader1_data = request.data.get("trader1")
        trader2_data = request.data.get("trader2")

        if not trader1_data or not trader2_data:
            return Response({"error": "Traders' data not provided"}, status=status.HTTP_400_BAD_REQUEST)

        trader1 = get_object_or_404(Survivor, pk=trader1_data["id"])
        trader2 = get_object_or_404(Survivor, pk=trader2_data["id"])

        if trader1.infected or trader2.infected:
            return Response({"error": "Infected survivors cannot trade"}, status=status.HTTP_400_BAD_REQUEST)

        trader1_items = trader1_data["items"]
        trader2_items = trader2_data["items"]

        """if not self.validate_items(trader1_items) or not self.validate_items(trader2_items):
            return Response({"error": "Invalid items provided"}, status=status.HTTP_400_BAD_REQUEST)"""
        #_______________________________________________________________
        trader1_items_valid = self.validate_items(trader1_items)
        trader2_items_valid = self.validate_items(trader2_items)

        if trader1_items_valid is not True or trader2_items_valid is not True:
            error_message = trader1_items_valid if trader1_items_valid is not True else trader2_items_valid
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        #_______________________________________________________________
        trade_value1 = self.calculate_trade_value(trader1_items)
        trade_value2 = self.calculate_trade_value(trader2_items)

        if trade_value1 != trade_value2:
            return Response({"error": "The trade value must be equal for both traders"}, status=status.HTTP_400_BAD_REQUEST)

        if not self.can_trade(trader1, trader1_items) or not self.can_trade(trader2, trader2_items):
            return Response({"error": "One or both traders don't have the required items"}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_trade(trader1, trader2, trader1_items, trader2_items)

        return Response({"success": "Items traded successfully"}, status=status.HTTP_200_OK)
    
    def validate_items(self, items):
        valid_item_names = {"Água", "Alimentação", "Medicação", "Munição"}
        for item in items:
            if "name" not in item:
                return "Item missing 'name' key"
            if item["name"] not in valid_item_names:
                return f"Invalid item name: {item['name']}"
        return True


    def calculate_trade_value(self, items):
        item_values = {
            "Água": 4,
            "Alimentação": 3,
            "Medicação": 2,
            "Munição": 1
        }
        total_value = 0
        for item in items:
            total_value += item_values[item["name"]] * item["quantity"]
        return total_value

    def can_trade(self, trader, items):
        # Acessando o inventário do sobrevivente
        trader_inventory = trader.inventory.all()

        # Criando um dicionário para armazenar a quantidade de cada item no inventário do sobrevivente
        trader_items_count = {}
        for inventory_item in trader_inventory:
            trader_items_count[inventory_item.item_id] = inventory_item.quantity

        # Verificando se o sobrevivente possui os itens necessários para a troca
        for item, quantity in items.items():
            if item not in trader_items_count or trader_items_count[item] < quantity:
                return False

        return True

    def perform_trade(self, trader1, trader2, items1, items2):
        trader1_items = trader1.item_set.all()
        trader2_items = trader2.item_set.all()
        trader1_inventory = {item.name: item for item in trader1_items}
        trader2_inventory = {item.name: item for item in trader2_items}

        for item in items1:
            item_name = item["name"]
            quantity = item["quantity"]
            trader1_inventory[item_name].quantity -= quantity
            trader2_inventory[item_name].quantity += quantity

        for item in items2:
            item_name = item["name"]
            quantity = item["quantity"]
            trader2_inventory[item_name].quantity -= quantity
            trader1_inventory[item_name].quantity += quantity

        for item in trader1_items:
            item.save()

        for item in trader2_items:
            item.save()

class ItemList(generics.ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = Item.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .trade import trade_items
import json


@csrf_exempt
def trade(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        survivor1_id = data.get('survivor1_id')
        survivor1_items = data.get('survivor1_items')
        survivor2_id = data.get('survivor2_id')
        survivor2_items = data.get('survivor2_items')

        if not survivor1_id or not survivor1_items or not survivor2_id or not survivor2_items:
            return JsonResponse({'error': 'Invalid data'}, status=400)

        success = trade_items(survivor1_id, survivor1_items, survivor2_id, survivor2_items)

        if success:
            return JsonResponse({'message': 'Trade successful'}, status=200)
        else:
            return JsonResponse({'error': 'Trade not successful'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


