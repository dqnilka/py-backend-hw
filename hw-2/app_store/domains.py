from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Cart:
    id: int
    items: List[Dict[str, int]] = field(default_factory=list)
    price: float = 0.0

@dataclass
class Item:
    id: int
    name: str
    price: float
    deleted: bool = False
