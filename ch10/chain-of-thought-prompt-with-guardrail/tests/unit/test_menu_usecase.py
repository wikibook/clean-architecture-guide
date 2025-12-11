import unittest
from datetime import datetime, timezone
from unittest.mock import Mock

from src.domain.entities.menu import Menu
from src.domain.usecases.menu_usecases import GetMenuListUseCaseImpl


class TestMenuUseCase(unittest.TestCase):
    def setUp(self) -> None:
        self.menu_repository = Mock()
        self.get_menu_list_usecase = GetMenuListUseCaseImpl(
            menu_repository=self.menu_repository
        )

    def test_get_menu_list_success(self) -> None:
        # Arrange
        menu1 = Menu(
            menu_id="menu-1",
            name="Americano",
            price=3000,
            category="coffee",
            stock=100,
            created_at=datetime.now(timezone.utc),
        )
        menu2 = Menu(
            menu_id="menu-2",
            name="Latte",
            price=4000,
            category="coffee",
            stock=100,
            created_at=datetime.now(timezone.utc),
        )
        self.menu_repository.get_all.return_value = [menu1, menu2]

        # Act
        result = self.get_menu_list_usecase.execute()

        # Assert
        self.assertEqual(len(result.menus), 2)
        self.assertEqual(result.menus[0].menu_id, "menu-1")
        self.assertEqual(result.menus[0].name, "Americano")
        self.assertEqual(result.menus[0].price, 3000)
        self.assertEqual(result.menus[0].category, "coffee")
        self.menu_repository.get_all.assert_called_once()
