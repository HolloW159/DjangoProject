import requests
from datetime import datetime

base_url = 'http://localhost:8000'

def test_add_item_success():
    json_data = {
        'item': 'TestItem',
        'quantity': 10,
    }
    response = requests.post(f'{base_url}/add/', json=json_data)
    assert response.status_code == 200
    assert response.json() == {'status': 'item added'}

def test_remove_item_success():
    json_data = {
        'item': 'TestItem',
        'quantity': 5,
    }
    response = requests.post(f'{base_url}/remove/', json=json_data)
    assert response.status_code == 200
    assert response.json() == {'status': 'item removed'}

def test_remove_item_insufficient_quantity():
    json_data = {
        'item': 'TestItem',
        'quantity': 100,
    }
    response = requests.post(f'{base_url}/remove/', json=json_data)
    assert response.status_code == 400
    assert response.json() == {"error": "Insufficient quantity"}

def test_get_stock_level_success():
    item_name = 'TestItem'
    response = requests.get(f'{base_url}/stock_level/{item_name}')
    assert response.status_code == 200
    data = response.json()
    assert 'item' in data
    assert 'quantity' in data
    assert data['item'] == 'TestItem'

def test_get_stock_level_not_found():
    item_name = 'NonExistentItem'
    response = requests.get(f'{base_url}/stock_level/{item_name}')
    assert response.status_code == 404
    assert response.json() == {"error": "Item not found"}

def test_get_all_stock_levels():
    response = requests.get(f'{base_url}/all_stock_levels/')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for item in data:
        assert 'item' in item
        assert 'quantity' in item

def test_get_critical_notifications():
    response = requests.get(f'{base_url}/critical_notifications/')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for item in data:
        assert 'item' in item
        assert 'quantity' in item
        assert item['quantity'] <= 20

def test_export_history():
    response = requests.get(f'{base_url}/history/export/')
    filename = f"history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == f'attachment; filename="{filename}"'
    assert response.headers['Content-Type'] == 'text/csv'
    content = response.text
    assert 'Item,Quantity' in content