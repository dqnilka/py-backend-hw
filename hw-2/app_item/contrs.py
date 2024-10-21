from pydantic import BaseModel, ConfigDict
from app_store.domains import Item

class ItemRequestPatch(BaseModel):
    name: str = ''
    price: float = 0.0
    
    model_config = ConfigDict(extra="forbid")  

    def as_item_info(self, id: int, deleted: bool) -> Item:
        return Item(id=id, name=self.name, price=self.price, deleted=deleted)

class ItemRequestPost(BaseModel):
    name: str
    price: float
    deleted: bool = False
    
    model_config = ConfigDict(extra="forbid")  

    def as_item_info(self, id: int) -> Item:
        return Item(id=id, name=self.name, price=self.price, deleted=self.deleted)
