from dataclasses import dataclass
from typing import List


@dataclass
class MenuResponseDTO:
    menu_id: str
    name: str
    price: int
    category: str


@dataclass
class MenuListResponseDTO:
    menus: List[MenuResponseDTO]
