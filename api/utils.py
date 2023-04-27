from .models import Survivor, Item, Inventory

def create_survivor_with_items(survivor_data, items_data):
    survivor = Survivor.objects.create(**survivor_data)
    
    for item_data in items_data:
        item, created = Item.objects.get_or_create(name=item_data['name'], points=item_data['points'])
        Inventory.objects.create(survivor=survivor, item=item, quantity=item_data['quantity'])
    
    return survivor
