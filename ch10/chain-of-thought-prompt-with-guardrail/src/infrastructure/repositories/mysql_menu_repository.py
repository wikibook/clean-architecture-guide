from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from ...domain.entities.menu import Menu
from ...domain.repositories.menu_repository import MenuRepository
from ..database.models.menu import MenuModel


class MySQLMenuRepository(MenuRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> List[Menu]:
        menu_models = self.db.query(MenuModel).all()
        return [
            Menu(
                menu_id=model.menu_id,
                name=model.name,
                price=model.price,
                category=model.category,
                stock=model.stock,
                created_at=model.created_at,
                updated_at=model.updated_at,
            )
            for model in menu_models
        ]

    def get_by_id(self, menu_id: str) -> Optional[Menu]:
        menu_model = (
            self.db.query(MenuModel).filter(MenuModel.menu_id == menu_id).first()
        )
        if not menu_model:
            return None

        return Menu(
            menu_id=menu_model.menu_id,
            name=menu_model.name,
            price=menu_model.price,
            category=menu_model.category,
            stock=menu_model.stock,
            created_at=menu_model.created_at,
            updated_at=menu_model.updated_at,
        )

    def update(self, menu: Menu) -> None:
        menu_model = (
            self.db.query(MenuModel).filter(MenuModel.menu_id == menu.menu_id).first()
        )
        if menu_model:
            menu_model.name = menu.name
            menu_model.price = menu.price
            menu_model.category = menu.category
            menu_model.stock = menu.stock
            menu_model.updated_at = datetime.utcnow()
            self.db.commit()
        else:
            menu_model = MenuModel(
                menu_id=menu.menu_id,
                name=menu.name,
                price=menu.price,
                category=menu.category,
                stock=menu.stock,
            )
            self.db.add(menu_model)
            self.db.commit()
