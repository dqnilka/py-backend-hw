from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import NonNegativeInt, PositiveInt, NonNegativeFloat

from app_store.domains import Cart
import app_store.quers as queries

router_cart = APIRouter(prefix="/cart")


@router_cart.post(
    "/{cart_id}/add/{item_id}",
    status_code=HTTPStatus.CREATED,
)
async def add_items_to_cart(cart_id: int, item_id: int):
    item = queries.add_items_to_cart(cart_id, item_id)
    return item

@router_cart.post(
    "/",
    status_code=HTTPStatus.CREATED,
)
async def post_cart(response: Response):
    id = queries.add_cart()
    response.headers["location"] = f"/cart/{id}"
    return {"id": id}


@router_cart.get(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "done",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "fail",
        },
    },
)
async def get_cart_by_id(id: int) -> Cart:
    cart = queries.get_one_cart(id)
    if not cart:
        raise HTTPException(
                HTTPStatus.NOT_FOUND,
                f"Request resource /cart/{id} was not found",
            )
    return cart

@router_cart.get("/")
async def get_cart_list(
    offset: Annotated[NonNegativeInt, Query()] = 0,
    limit: Annotated[PositiveInt, Query()] = 10,
    min_price: Annotated[NonNegativeFloat, Query()] = None,
    max_price: Annotated[NonNegativeFloat, Query()] = None,
    min_quantity: Annotated[NonNegativeInt, Query()] = None,
    max_quantity: Annotated[NonNegativeInt, Query()] = None,
) -> list[Cart]:
    return [cart for cart in queries.get_many_carts(offset, limit, 
                                                    min_price, max_price,
                                                    min_quantity, max_quantity)]