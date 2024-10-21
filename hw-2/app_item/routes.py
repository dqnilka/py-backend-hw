from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import NonNegativeInt, PositiveInt, NonNegativeFloat

from app_store.domains import Item
import app_store.quers as quers
from app_item.contrs import ItemRequestPatch, ItemRequestPost

router_item = APIRouter(prefix="/item")

@router_item.get(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested item",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested item as one was not found",
        },
    },
)
async def get_item_by_id(id: int) -> Item:
    """Возвращает товар по его идентификатору."""
    item = quers.get_one_item(id)
    if not item:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Request resource /item/{id} was not found",
        )
    return item

@router_item.get("/")
async def get_item_list(
    offset: NonNegativeInt = Query(default=0),
    limit: PositiveInt = Query(default=10),
    min_price: Optional[NonNegativeFloat] = Query(default=None),
    max_price: Optional[NonNegativeFloat] = Query(default=None),
    show_deleted: bool = Query(default=False),
) -> List[Item]:
    return [
        item for item in quers.get_many_items(offset, limit, min_price, max_price, show_deleted)
    ]

@router_item.post(
    "/",
    status_code=HTTPStatus.CREATED,
)
async def post_item(info: ItemRequestPost, response: Response):
    item = quers.add_item(info=info)
    response.headers["Location"] = f"/item/{item.id}"
    return item

@router_item.put(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully updated or upserted item",
        },
        HTTPStatus.NOT_MODIFIED: {
            "description": "Failed to modify item as one was not found",
        },
    },
)
async def put_item(id: int, info: ItemRequestPost) -> Item:
    item = quers.put_item(id, info)
    if item is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_MODIFIED,
            detail=f"Requested resource /item/{id} was not found",
        )
    return item

@router_item.delete(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully deleted item",
        },
    },
)
async def delete_item(id: int, response: Response):
    item = quers.delete_item(id)
    if item is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Requested resource /item/{id} was not found",
        )
    return item

@router_item.patch(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully patched item",
        },
        HTTPStatus.NOT_MODIFIED: {
            "description": "Failed to modify item as one was not found",
        },
    },
)
async def patch_item(id: int, info: ItemRequestPatch) -> Item:
    item = quers.patch_item(id, info)
    if item is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_MODIFIED,
            detail=f"Requested resource /item/{id} was not found",
        )
    return item
