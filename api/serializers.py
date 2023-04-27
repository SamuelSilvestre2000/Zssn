""" from rest_framework import serializers
from .models import Survivor, Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'points']

class SurvivorSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Survivor
        fields = ['id', 'name', 'age', 'gender', 'last_location_latitude', 'last_location_longitude', 'infected', 'items',]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        survivor = Survivor.objects.create(**validated_data)
        for item_data in items_data:
            Item.objects.create(survivor=survivor, **item_data)
        return survivor """

from rest_framework import serializers
from .models import Survivor, Item, Inventory

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
    items = InventorySerializer(many=True, read_only=True)

    class Meta:
        model = Survivor
        fields = '__all__'

