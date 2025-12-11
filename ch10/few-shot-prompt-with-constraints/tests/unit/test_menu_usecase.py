import unittest
from unittest.mock import Mock
from src.domain.entities.menu import Menu
from src.domain.usecases.menu_usecases import GetMenusUseCase


class TestGetMenusUseCase(unittest.TestCase):
    def setUp(self):
        self.menu_repository = Mock()
        self.usecase = GetMenusUseCase(self.menu_repository)
        
    def test_execute_returns_menu_list(self):
        # Arrange
        mock_menus = [
            Menu(menu_id="1", name="Americano", price=3000, category="coffee", stock=10),
            Menu(menu_id="2", name="Latte", price=4000, category="coffee", stock=10)
        ]
        self.menu_repository.get_all.return_value = mock_menus
        
        # Act
        result = self.usecase.execute()
        
        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].menu_id, "1")
        self.assertEqual(result[0].name, "Americano")
        self.assertEqual(result[0].price, 3000)
        self.assertEqual(result[0].category, "coffee")
        
        self.menu_repository.get_all.assert_called_once()