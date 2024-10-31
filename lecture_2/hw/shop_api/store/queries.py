from typing import Iterable, Union
from ..store.models import (
    CartEntity,
    CartInfo,
    ItemEntity,
    ItemInCartInfo,
    ItemInfo,
    PatchedItemInfo,
)

_items = dict[int, ItemInfo]()
_carts = dict[int, CartInfo]()


def int_l_id_generator() -> Iterable[int]:
    l_id = 0
    while True:
        yield l_id
        l_id += 1


_items_l_id_generator = int_l_id_generator()
_carts_l_id_generator = int_l_id_generator()


def add_item(info: ItemInfo) -> ItemEntity:
    l_id = next(_items_l_id_generator)
    _items[l_id] = info
    return ItemEntity(id=l_id, info=info)


def delete_item(l_id: int) -> None:
    if l_id in _items:
        _items[l_id].deleted = True


def get_item(l_id: int) -> Union[ItemEntity, None]:
    if l_id not in _items or _items[l_id].deleted:
        return None
    return ItemEntity(id=l_id, info=_items[l_id])


def get_items_list(
        offset: int = 0,
        limit: int = 10,
        min_price: Union[float, None] = None,
        max_price: Union[float, None] = None,
        show_deleted: bool = False,
) -> Iterable[ItemEntity]:
    curr = 0
    for l_id, info in _items.items():
        if (
                (offset <= curr < offset + limit)
                and (show_deleted or not info.deleted)
                and (min_price is None or info.price >= min_price)
                and (max_price is None or info.price <= max_price)
        ):
            yield ItemEntity(id=l_id, info=info)

        curr += 1


def put_item(l_id: int, info: ItemInfo) -> Union[ItemEntity, None]:
    if l_id not in _items:
        return None
    _items[l_id] = info
    return ItemEntity(id=l_id, info=info)


def patch_item(l_id: int, info: PatchedItemInfo) -> Union[ItemEntity, None]:
    if l_id not in _items or _items[l_id].deleted:
        return None

    if info.name is not None:
        _items[l_id].name = info.name

    if info.price is not None:
        _items[l_id].price = info.price

    return ItemEntity(id=l_id, info=_items[l_id])


def create_cart() -> int:
    l_id = next(_carts_l_id_generator)
    _carts[l_id] = CartInfo()
    return l_id


def get_cart(l_id: int) -> Union[CartEntity, None]:
    if l_id not in _carts:
        return None
    return CartEntity(id=l_id, info=_carts[l_id])


def get_carts_list(
        offset: int = 0,
        limit: int = 10,
        min_price: Union[float, None] = None,
        max_price: Union[float, None] = None,
        min_quantity: Union[float, None] = None,
        max_quantity: Union[float, None] = None,
) -> Iterable[CartEntity]:
    curr = 0
    for l_id, info in _carts.items():
        if (
                (offset <= curr < offset + limit)
                and (min_price is None or info.total_price >= min_price)
                and (max_price is None or info.total_price <= max_price)
                and (min_quantity is None or info.total_quantity >= min_quantity)
                and (max_quantity is None or info.total_quantity <= max_quantity)
        ):
            yield CartEntity(id=l_id, info=info)

        curr += 1


def add_item_in_cart(cart_l_id: int, item_l_id: int) -> Union[CartEntity, None]:
    if not (cart_l_id in _carts and item_l_id in _items):
        return None

    if item_l_id not in _carts[cart_l_id].items:
        _carts[cart_l_id].items[item_l_id] = ItemInCartInfo(
            info=_items[item_l_id], quantity=1
        )
    else:
        _carts[cart_l_id].items[item_l_id].quantity += 1

    return CartEntity(id=cart_l_id, info=_carts[cart_l_id])
