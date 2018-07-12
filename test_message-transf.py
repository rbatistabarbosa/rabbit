import pytest
import json
from message_transf import Out

@pytest.fixture
def order():
    return {'id': 1, 'side': 'buy', 'price': 2.1, 'quantity': 2, 'symbol': 'USD'}


def to_out(dict_obj):
    return Out(json.dumps(dict_obj))


def test_empty_message():
    out_obj = Out('')
    assert out_obj.to_dict() == {'id': -1, 'status': False, 'msgs': ['invalid json']}


def test_not_in_schema():
    msg = '["foo", {"bar":["baz", null, 1.0, 2]}]'
    out_obj = Out(msg)
    assert out_obj.to_dict() == {'id': -1, 'status': False, 'msgs': ['invalid schema']}


def test_is_OK(order):
    out_obj = to_out(order)
    assert out_obj.to_dict() == {'id': 1, 'status': True, 'msgs': []}

def test_side_BuY(order):
    order['side'] = 'bUy'
    out_obj = to_out(order)
    assert out_obj.to_dict() == {'id': 1, 'status': True, 'msgs': []}

def test_side_wrong(order):
    order['side'] = 'a'
    out_obj = to_out(order)
    assert out_obj.to_dict() == {'id': 1, 'status': False, 'msgs': ['invalid side']}


def test_price_negative(order):
    order['price'] = -1
    out_obj = to_out(order)
    assert out_obj.to_dict() == {'id': 1, 'status': False, 'msgs': ['price must be positive']}


def test_quantitiy_negative(order):
    order['quantity'] = -1
    out_obj = to_out(order)
    assert out_obj.to_dict() == {'id': 1, 'status': False, 'msgs': ['quantity must be positive']}


def test_price_quantity_negative(order):
    order['price'] = 0
    order['quantity'] = 0
    out_obj = to_out(order)
    assert out_obj.to_dict() == {'id': 1, 'status': False, 
        'msgs': ['price must be positive', 'quantity must be positive']}

def test_to_str(order):
    out_obj = to_out(order)
    str_obj = out_obj.to_str()
    assert str_obj == '{"id": 1, "status": true, "msgs": []}'