from pydantic import BaseModel, ConfigDict
from store.domains import Item

class ItemRequestPatch(BaseModel):
    name: str = ''
    price: float = 0.0
    
    model_config = ConfigDict(extra="forbid")  # Запретить дополнительные поля

    def as_item_info(self, id: int, deleted: bool) -> Item:
        """Преобразует данные запроса в объект Item."""
        return Item(id=id, name=self.name, price=self.price, deleted=deleted)

class ItemRequestPost(BaseModel):
    name: str
    price: float
    deleted: bool = False
    
    model_config = ConfigDict(extra="forbid")  # Запретить дополнительные поля

    def as_item_info(self, id: int) -> Item:
        """Преобразует данные запроса в объект Item."""
        return Item(id=id, name=self.name, price=self.price, deleted=self.deleted)
