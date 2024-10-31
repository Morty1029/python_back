
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, NonNegativeFloat, PositiveInt
from typing import Union

from ..store.models import (
    CartEntity,
    ItemEntity,
    ItemInfo,
    PatchedItemInfo,
)


class ItemResponse(BaseModel):
    id: int
    name: str
    price: NonNegativeFloat
    deleted: bool

    @staticmethod
    def from_entity(entity: ItemEntity) -> ItemResponse:
        return ItemResponse(
            id=entity.id,
            name=entity.info.name,
            price=entity.info.price,
            deleted=entity.info.deleted,
        )


class ItemRequest(BaseModel):
    name: str
    price: NonNegativeFloat
    deleted: bool = False

    def as_info(self) -> ItemInfo:
        return ItemInfo(name=self.name, price=self.price, deleted=self.deleted)


class PatchedItemRequest(BaseModel):
    name: Union[str, None] = None
    price: Union[NonNegativeFloat, None] = None

    model_config = ConfigDict(extra="forbid")

    def as_patched_info(self) -> PatchedItemInfo:
        return PatchedItemInfo(name=self.name, price=self.price)


class ItemInCartResponse(BaseModel):
    id: int
    name: str
    quantity: PositiveInt
    available: bool


class CartResponse(BaseModel):
    id: int
    items: list[ItemInCartResponse] = []
    price: NonNegativeFloat

    @staticmethod
    def from_entity(entity: CartEntity) -> CartResponse:
        items = []
        for item_id, item_info in entity.info.items.items():
            items.append(
                ItemInCartResponse(
                    id=item_id,
                    name=item_info.info.name,
                    quantity=item_info.quantity,
                    available=not item_info.info.deleted,
                )
            )
        return CartResponse(id=entity.id, items=items, price=entity.info.total_price)
