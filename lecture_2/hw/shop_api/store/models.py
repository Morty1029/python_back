from pydantic import BaseModel, NonNegativeFloat, PositiveInt
from typing import Union


class ItemInfo(BaseModel):
    name: str
    price: NonNegativeFloat
    deleted: bool = False


class PatchedItemInfo(BaseModel):
    name: Union[str, None] = None
    price: Union[NonNegativeFloat, None] = None
    deleted: bool = False


class ItemEntity(BaseModel):
    id: int
    info: ItemInfo


class ItemInCartInfo(BaseModel):
    info: ItemInfo
    quantity: PositiveInt


class CartInfo(BaseModel):
    items: dict[int, ItemInCartInfo] = {}

    @property
    def total_price(self) -> NonNegativeFloat:
        return sum(item.info.price * item.quantity for item in self.items.values())

    @property
    def total_quantity(self) -> PositiveInt:
        return sum(item.quantity for item in self.items.values())


class CartEntity(BaseModel):
    id: int
    info: CartInfo
