from typing import Iterable, Optional

from app_store.domains import Cart, Item
from app_item.contrs import ItemRequestPost, ItemRequestPatch

_data_cart: dict[int, Cart] = {}
_data_item: dict[int, Item] = {}

def int_id_generator() -> Iterable[int]:
    i = 0
    while True:
        yield i
        i += 1

_id_cart_generator = int_id_generator()
_id_item_generator = int_id_generator()

def add_cart() -> int:
    _id = next(_id_cart_generator)
    _data_cart[_id] = Cart(id=_id)
    return _id

def add_item(info: ItemRequestPost) -> Item:
    _id = next(_id_item_generator)
    item_info = info.as_item_info(_id)
    _data_item[_id] = item_info
    return item_info

def get_one_cart(cart_id: int) -> Optional[Cart]:
    return _data_cart.get(cart_id)

def get_many_carts(offset: int = 0, limit: int = 10, 
                   min_price: Optional[float] = None, 
                   max_price: Optional[float] = None,
                   min_quantity: Optional[int] = None, 
                   max_quantity: Optional[int] = None) -> Iterable[Cart]:
    fit_carts = [
        cart for cart in _data_cart.values()
        if (min_price is None or cart.price >= min_price) and
           (max_price is None or cart.price <= max_price)
    ]
    
    # Пагинация
    fit_carts = fit_carts[offset: offset + limit]
    
    total_quantity = sum(item['quantity'] for cart in fit_carts for item in cart.items)
    
    if (min_quantity is not None and total_quantity < min_quantity) or \
       (max_quantity is not None and total_quantity > max_quantity):
        return []

    return fit_carts

def get_one_item(item_id: int) -> Optional[Item]:
    item = _data_item.get(item_id)
    return item if item and not item.deleted else None

def get_many_items(offset: int = 0, limit: int = 10,
                   min_price: Optional[float] = None, 
                   max_price: Optional[float] = None,
                   show_deleted: bool = False) -> Iterable[Item]:
    for item_id in range(offset, offset + limit):
        item = _data_item.get(item_id)
        if item and (show_deleted or not item.deleted) and \
           (min_price is None or item.price >= min_price) and \
           (max_price is None or item.price <= max_price):
            yield item

def put_item(item_id: int, info: ItemRequestPatch) -> Optional[Item]:
    if item_id not in _data_item:
        return None
    updated_item = info.as_item_info(item_id)
    _data_item[item_id] = updated_item
    return updated_item

def delete_item(item_id: int) -> Optional[Item]:
    item = _data_item.get(item_id)
    if item:
        item.deleted = True
    return item

def patch_item(item_id: int, info: ItemRequestPatch) -> Optional[Item]:
    item = _data_item.get(item_id)
    if item and not item.deleted:
        updated_item = info.as_item_info(item_id, deleted=item.deleted)
        _data_item[item_id] = updated_item
        return updated_item
    return None

def add_items_to_cart(cart_id: int, item_id: int) -> Optional[Cart]:
    cart = _data_cart.get(cart_id)
    item = _data_item.get(item_id)

    if cart is None or item is None:
        return None

    for cart_item in cart.items:
        if cart_item['id'] == item_id:
            cart_item['quantity'] += 1
            cart.price += item.price
            return cart
    
    cart.items.append({
        'id': item_id,
        'name': item.name,
        'quantity': 1,
        'available': not item.deleted
    })
    cart.price += item.price
    return cart
