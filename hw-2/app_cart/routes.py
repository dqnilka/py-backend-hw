from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import NonNegativeInt, PositiveInt, NonNegativeFloat

from app_store.domains import Cart
import app_store.quers as quers

router_cart = APIRouter(prefix="/cart")

@router_cart.get(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested cart",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested cart as one was not found",
        },
    },
)
async def get_cart_by_id(id: int) -> Cart:
    cart = quers.get_one_cart(id)
    if not cart:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Request resource /cart/{id} was not found",
        )
    return cart

@router_cart.get("/")
async def get_cart_list(
    offset: NonNegativeInt = Query(default=0),
    limit: PositiveInt = Query(default=10),
    min_price: Optional[NonNegativeFloat] = Query(default=None),
    max_price: Optional[NonNegativeFloat] = Query(default=None),
    min_quantity: Optional[NonNegativeInt] = Query(default=None),
    max_quantity: Optional[NonNegativeInt] = Query(default=None),
) -> List[Cart]:
    return [
        cart for cart in quers.get_many_carts(offset, limit, min_price, max_price, min_quantity, max_quantity)
    ]

@router_cart.post(
    "/",
    status_code=HTTPStatus.CREATED,
)
async def post_cart(response: Response):
    cart_id = quers.add_cart()
    response.headers["Location"] = f"/cart/{cart_id}"
    return {"id": cart_id}

@router_cart.post(
    "/{cart_id}/add/{item_id}",
    status_code=HTTPStatus.CREATED,
)
async def add_items_to_cart(cart_id: int, item_id: int):
    item = quers.add_items_to_cart(cart_id, item_id)
    if item is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Item with id {item_id} could not be added to cart {cart_id}."
        )
    return item
