
from rest_framework import serializers
from .models import Survivor, Item, Inventory
from django.db.models import fields

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = Inventory
        fields = ('item', 'quantity')

class SurvivorSerializer(serializers.ModelSerializer):
    items = InventorySerializer(source='survivor_inventory', many=True, read_only=True)
    
    class Meta:
        model = Survivor
        fields = ['id', 'items', 'name', 'age', 'gender', 'last_location_latitude', 'last_location_longitude', 'infected']
        #fields = '__all__'


