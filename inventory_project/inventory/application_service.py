from .models import InventoryItem

def add_item_service(item_name, quantity):
    item, created = InventoryItem.objects.get_or_create(name=item_name)
    item.quantity += quantity
    item.save()
    return item

def remove_item_service(item_name, quantity):
    try:
        item = InventoryItem.objects.get(name=item_name)
        if item.quantity >= quantity:
            item.quantity -= quantity
            item.save()
            return item
        else:
            raise ValueError("Insufficient quantity")
    except InventoryItem.DoesNotExist:
        raise ValueError("Item not found")

def get_stock_level_service(item_name):
    try:
        item = InventoryItem.objects.get(name=item_name)
        return item
    except InventoryItem.DoesNotExist:
        raise ValueError("Item not found")

def get_all_stock_levels_service():
    return InventoryItem.objects.all()

def get_critical_notifications_service():
    return InventoryItem.objects.filter(quantity__lte=20)

def export_history_service():
    items = InventoryItem.objects.all()
    history_data = [{'Item': item.name, 'Quantity': item.quantity} for item in items]
    return history_data