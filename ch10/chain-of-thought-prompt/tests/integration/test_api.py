import unittest
from fastapi.testclient import TestClient
from datetime import datetime
from src.main import app
from src.infrastructure.repositories.dynamodb_models import MenuModel, OrderModel

class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """테스트 클라이언트 설정"""
        cls.client = TestClient(app)

        # 테스트용 테이블 생성
        if not MenuModel.exists():
            MenuModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
        if not OrderModel.exists():
            OrderModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

    def setUp(self):
        """테스트 데이터 설정"""
        # 테스트용 메뉴 데이터 생성
        self.menu = MenuModel(
            menu_id="test-menu",
            name="Test Americano",
            price=3000,
            category="coffee",
            stock=10,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.menu.save()

    def tearDown(self):
        """테스트 데이터 정리"""
        # 테스트 후 데이터 삭제
        for menu in MenuModel.scan():
            menu.delete()
        for order in OrderModel.scan():
            order.delete()

    def test_get_menus(self):
        """메뉴 목록 조회 API 테스트"""
        # When
        response = self.client.get("/menu")

        # Then
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["data"]), 1)
        self.assertEqual(data["data"][0]["menu_id"], "test-menu")
        self.assertEqual(data["data"][0]["name"], "Test Americano")

    def test_create_order(self):
        """주문 생성 API 테스트"""
        # Given
        order_data = {
            "customer_id": "test-customer",
            "menu_id": "test-menu",
            "quantity": 2,
            "options": {"size": "medium"}
        }

        # When
        response = self.client.post("/order", json=order_data)

        # Then
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertIsNotNone(data["data"]["order_id"])

    def test_get_order(self):
        """주문 조회 API 테스트"""
        # Given
        # 먼저 주문 생성
        order_data = {
            "customer_id": "test-customer",
            "menu_id": "test-menu",
            "quantity": 2,
            "options": {"size": "medium"}
        }
        create_response = self.client.post("/order", json=order_data)
        order_id = create_response.json()["data"]["order_id"]

        # When
        response = self.client.get(f"/order/{order_id}")

        # Then
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["order_id"], order_id)

    def test_get_order_not_found(self):
        """존재하지 않는 주문 조회 API 테스트"""
        # When
        response = self.client.get("/order/invalid-order")

        # Then
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["status"], "error")

if __name__ == '__main__':
    unittest.main()