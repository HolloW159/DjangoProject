import sys
import os
from django.core.exceptions import ObjectDoesNotExist
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import pytest
from inventory.models import InventoryItem
from inventory.application_service import (
    add_item_service,
    remove_item_service,
    get_stock_level_service,
    get_all_stock_levels_service,
    get_critical_notifications_service,
    export_history_service
)

@pytest.fixture
def inventory_item():
    return InventoryItem.objects.create(name='Test Item', quantity=10)

@pytest.fixture
def inventory_items():
    item1 = InventoryItem.objects.create(name='Item 1', quantity=10)
    item2 = InventoryItem.objects.create(name='Item 2', quantity=5)
    item3 = InventoryItem.objects.create(name='Item 3', quantity=25)
    return [item1, item2, item3]

@pytest.mark.django_db
def test_add_item_service(inventory_item):
    item_name = 'Test Item'
    quantity = 5
    updated_item = add_item_service(item_name, quantity)
    assert updated_item.quantity == 15

@pytest.mark.django_db
def test_remove_item_service(inventory_item):
    item_name = 'Test Item'
    quantity = 5
    updated_item = remove_item_service(item_name, quantity)
    assert updated_item.quantity == 5

@pytest.mark.django_db
def test_remove_item_service_insufficient_quantity(inventory_item):
    item_name = 'Test Item'
    quantity = 15
    with pytest.raises(ValueError, match='Insufficient quantity'):
        remove_item_service(item_name, quantity)

@pytest.mark.django_db
def test_remove_item_service_item_not_found():
    item_name = 'Non-existent Item'
    quantity = 5
    with pytest.raises(ValueError, match='Item not found'):
        remove_item_service(item_name, quantity)

@pytest.mark.django_db
def test_get_stock_level_service(inventory_item):
    item_name = 'Test Item'
    item = get_stock_level_service(item_name)
    assert item.name == 'Test Item'
    assert item.quantity == 10

@pytest.mark.django_db
def test_get_stock_level_service_item_not_found():
    item_name = 'Non-existent Item'
    with pytest.raises(ValueError, match='Item not found'):
        get_stock_level_service(item_name)

@pytest.mark.django_db
def test_get_all_stock_levels_service(inventory_items):
    items = get_all_stock_levels_service()
    assert len(items) == 3

@pytest.mark.django_db
def test_get_critical_notifications_service(inventory_items):
    critical_items = get_critical_notifications_service()
    assert len(critical_items) == 2

@pytest.mark.django_db
def test_export_history_service(inventory_items):
    history = export_history_service()
    assert len(history) == 3
    assert history[0]['Item'] == 'Item 1'
    assert history[1]['Item'] == 'Item 2'
    assert history[2]['Item'] == 'Item 3'
