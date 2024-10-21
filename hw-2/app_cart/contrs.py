from pydantic import BaseModel, ConfigDict
from app_store.domains import Cart

class CartResponse(BaseModel):
    id: int
    items: list[dict] = []
    price: float = 0.0

    model_config = ConfigDict(extra="forbid")  

    @classmethod
    def from_entity(cls, entity: Cart) -> "CartResponse":
        return cls(
            id=entity.id,
            items=entity.items,
            price=entity.price,  
        )
