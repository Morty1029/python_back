from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import NonNegativeFloat, NonNegativeInt, PositiveInt
from typing import Union

from ..store import queries

from .contracts import CartResponse, ItemRequest, ItemResponse, PatchedItemRequest

router = APIRouter()


@router.post("/item", status_code=HTTPStatus.CREATED)
async def post_item(info: ItemRequest, response: Response) -> ItemResponse:
    entity = queries.add_item(info.as_info())
    response.headers["location"] = f"/item/{entity.id}"

    return ItemResponse.from_entity(entity)


@router.get(
    "/item/{id}",
    responses={
        HTTPStatus.OK: {"description": "Successfully returned requested item"},
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested item as one was not found"
        },
    },
)
async def get_item(id: int) -> Union[ItemResponse, None]:
    entity = queries.get_item(id)
    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, f"Request resource /item/{id} was not found"
        )

    return ItemResponse.from_entity(entity)


@router.get("/item")
async def get_items_list(
        offset: Annotated[NonNegativeInt, Query()] = 0,
        limit: Annotated[PositiveInt, Query()] = 10,
        min_price: Annotated[Union[NonNegativeFloat, None], Query()] = None,
        max_price: Annotated[Union[NonNegativeFloat, None], Query()] = None,
        show_deleted: Annotated[bool, Query()] = False,
) -> list[ItemResponse]:

    return [
        ItemResponse.from_entity(e)
        for e in queries.get_items_list(offset, limit, min_price, max_price, show_deleted)
    ]


@router.put(
    "/item/{id}",
    responses={
        HTTPStatus.OK: {"description": "Successfully updated item"},
        HTTPStatus.NOT_MODIFIED: {
            "description": "Failed to modify item as one was not found"
        },
    },
)
async def put_item(id: int, info: ItemRequest) -> ItemResponse:
    entity = queries.put_item(id, info.as_info())
    if entity is None:
        raise HTTPException(
            HTTPStatus.NOT_MODIFIED,
            f"Requested resource /item/{id} was not found",
        )

    return ItemResponse.from_entity(entity)


@router.patch(
    "/item/{id}",
    responses={
        HTTPStatus.OK: {"description": "Successfully patched item"},
        HTTPStatus.NOT_MODIFIED: {
            "description": "Failed to modify item as one was not found"
        },
    },
)
async def patch_item(id: int, patched_info: PatchedItemRequest) -> ItemResponse:
    entity = queries.patch_item(id, patched_info.as_patched_info())

    if entity is None:
        raise HTTPException(
            HTTPStatus.NOT_MODIFIED,
            f"Requested resource /item/{id} was not found",
        )

    return ItemResponse.from_entity(entity)


@router.delete("/item/{id}")
async def delete_item(id: int) -> Response:
    queries.delete_item(id)

    return Response("")


@router.post("/cart", status_code=HTTPStatus.CREATED)
async def create_cart(response: Response) -> dict[str, int]:
    l_id = queries.create_cart()
    response.headers["location"] = f"/cart/{l_id}"

    return {"id": l_id}


@router.get(
    "/cart/{id}",
    responses={
        HTTPStatus.OK: {"description": "Successfully returned requested cart"},
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested cart as one was not found"
        },
    },
)
async def get_cart(id: int) -> Union[CartResponse, None]:
    entity = queries.get_cart(id)
    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, f"Request resource /cart/{id} was not found"
        )

    return CartResponse.from_entity(entity)


@router.get("/cart")
async def get_carts_list(
        offset: Annotated[NonNegativeInt, Query()] = 0,
        limit: Annotated[PositiveInt, Query()] = 10,
        min_price: Annotated[Union[NonNegativeFloat, None], Query()] = None,
        max_price: Annotated[Union[NonNegativeFloat, None], Query()] = None,
        min_quantity: Annotated[Union[NonNegativeFloat, None], Query()] = None,
        max_quantity: Annotated[Union[NonNegativeFloat, None], Query()] = None,
) -> list[CartResponse]:

    return [
        CartResponse.from_entity(e)
        for e in queries.get_carts_list(
            offset, limit, min_price, max_price, min_quantity, max_quantity
        )
    ]


@router.post(
    "/cart/{cart_id}/add/{item_id}",
    responses={
        HTTPStatus.OK: {"description": "Successfully added item to cart"},
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to add item to cart as either one was not found"
        },
    },
)
async def add_item_to_cart(cart_id: int, item_id: int) -> Union[CartResponse, None]:
    entity = queries.add_item_in_cart(cart_id, item_id)
    if entity is None:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            "Failed to add item to cart as either one was not found",
        )

    return CartResponse.from_entity(entity)
