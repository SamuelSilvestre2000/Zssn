from rest_framework import generics
from .models import Survivor, Item
from .serializers import SurvivorSerializer, ItemSerializer

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

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


