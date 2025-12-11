import unittest
from unittest.mock import Mock
from datetime import datetime
from src.domain.entities.menu import Menu
from src.domain.usecases.menu_usecases import MenuUseCases

class TestMenuUseCases(unittest.TestCase):
    def setUp(self):
        """테스트 설정"""
        self.menu_repository = Mock()
        self.menu_usecase = MenuUseCases(self.menu_repository)

    def test_get_all_menus_success(self):
        """메뉴 목록 조회 성공 테스트"""
        # Given
        mock_menus = [
            Menu(
                menu_id="menu-1",
                name="Americano",
                price=3000,
                category="coffee",
                stock=100,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            Menu(
                menu_id="menu-2",
                name="Latte",
                price=4000,
                category="coffee",
                stock=100,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        self.menu_repository.get_all.return_value = mock_menus

        # When
        result = self.menu_usecase.get_all_menus()

        # Then
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].menu_id, "menu-1")
        self.assertEqual(result[0].name, "Americano")
        self.assertEqual(result[0].price, 3000)
        self.assertEqual(result[0].category, "coffee")

    def test_get_all_menus_empty(self):
        """메뉴 목록이 비어있는 경우 테스트"""
        # Given
        self.menu_repository.get_all.return_value = []

        # When
        result = self.menu_usecase.get_all_menus()

        # Then
        self.assertEqual(len(result), 0)

    def test_get_all_menus_database_error(self):
        """데이터베이스 에러 테스트"""
        # Given
        self.menu_repository.get_all.side_effect = Exception("Database error")

        # When/Then
        with self.assertRaises(Exception) as context:
            self.menu_usecase.get_all_menus()
        self.assertTrue("Database error" in str(context.exception))

if __name__ == '__main__':
    unittest.main()