from typing import List, Optional

from pynamodb.attributes import NumberAttribute, UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

from ...domain.entities.menu import Menu
from ...domain.repositories.menu_repository import MenuRepository


class MenuModel(Model):
    class Meta:
        table_name = "menus"
        region = "ap-northeast-2"

    menu_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    price = NumberAttribute()
    category = UnicodeAttribute()
    stock = NumberAttribute()
    created_at = UTCDateTimeAttribute()
    updated_at = UTCDateTimeAttribute(null=True)


class DynamoDBMenuRepository(MenuRepository):
    def get_all(self) -> List[Menu]:
        return [
            Menu(
                menu_id=item.menu_id,
                name=item.name,
                price=item.price,
                category=item.category,
                stock=item.stock,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            for item in MenuModel.scan()
        ]

    def get_by_id(self, menu_id: str) -> Optional[Menu]:
        try:
            item = MenuModel.get(menu_id)
            return Menu(
                menu_id=item.menu_id,
                name=item.name,
                price=item.price,
                category=item.category,
                stock=item.stock,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
        except MenuModel.DoesNotExist:
            return None

    def update(self, menu: Menu) -> None:
        item = MenuModel(
            menu_id=menu.menu_id,
            name=menu.name,
            price=menu.price,
            category=menu.category,
            stock=menu.stock,
            created_at=menu.created_at,
            updated_at=menu.updated_at,
        )
        item.save()
