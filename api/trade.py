from api.models import Survivor, Inventory, Item

def trade_items(survivor1_id, survivor1_items, survivor2_id, survivor2_items):
    # Verificar se os IDs dos sobreviventes são válidos e se eles não estão infectados
    try:
        survivor1 = Survivor.objects.get(id=survivor1_id, infected=False)
        survivor2 = Survivor.objects.get(id=survivor2_id, infected=False)
    except Survivor.DoesNotExist:
        return False

    # Calcular a soma dos pontos dos itens para cada sobrevivente
    total_points_survivor1 = sum(item["item"]["points"] * item["quantity"] for item in survivor1_items)
    total_points_survivor2 = sum(item["item"]["points"] * item["quantity"] for item in survivor2_items)

    # Verificar se a troca é justa (os pontos são iguais)
    if total_points_survivor1 != total_points_survivor2:
        return False

    # Verificar se os sobreviventes têm itens suficientes em seus inventários
    for item_data in survivor1_items:
        try:
            inventory_item = Inventory.objects.get(survivor=survivor1, item__id=item_data["item"]["id"])
            if inventory_item.quantity < item_data["quantity"]:
                return False
        except Inventory.DoesNotExist:
            return False

    for item_data in survivor2_items:
        try:
            inventory_item = Inventory.objects.get(survivor=survivor2, item__id=item_data["item"]["id"])
            if inventory_item.quantity < item_data["quantity"]:
                return False
        except Inventory.DoesNotExist:
            return False

    # Realizar a troca de itens
    for item_data in survivor1_items:
        # Remover itens do survivor1 e adicionar ao survivor2
        survivor1_inventory_item = Inventory.objects.get(survivor=survivor1, item__id=item_data["item"]["id"])
        survivor1_inventory_item.quantity -= item_data["quantity"]
        survivor1_inventory_item.save()

        survivor2_inventory_item, _ = Inventory.objects.get_or_create(survivor=survivor2, item__id=item_data["item"]["id"])
        survivor2_inventory_item.quantity += item_data["quantity"]
        survivor2_inventory_item.save()

    for item_data in survivor2_items:
        # Remover itens do survivor2 e adicionar ao survivor1
        survivor2_inventory_item = Inventory.objects.get(survivor=survivor2, item__id=item_data["item"]["id"])
        survivor2_inventory_item.quantity -= item_data["quantity"]
        survivor2_inventory_item.save()

        survivor1_inventory_item, _ = Inventory.objects.get_or_create(survivor=survivor1, item__id=item_data["item"]["id"])
        survivor1_inventory_item.quantity += item_data["quantity"]
        survivor1_inventory_item.save()

    return True
