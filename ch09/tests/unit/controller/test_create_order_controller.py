import unittest
from unittest.mock import Mock

from fastapi.testclient import TestClient

from adapter.presenter.create_order_presenter import CreateOrderPresenter
from application.usecases.create_order_usecase import CreateOrderInputDto, CreateOrderUseCase, CreateOrderOutputDto
from domain.exceptions import InvalidInputParameter
from infrastructure.web.fastapi import app, get_create_order_use_case


class TestCreateOrderController(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

        self.use_case_mock = Mock(spec=CreateOrderUseCase)
        self.use_case_mock.output_boundary = CreateOrderPresenter()
        app.dependency_overrides[get_create_order_use_case] = lambda: self.use_case_mock

    def tearDown(self):
        app.dependency_overrides = {}

    def test_create_order_success(self):
        # Given: 모킹된 성공 응답
        output_dto = CreateOrderOutputDto(
            order_id="order-123",
            customer_id="customer1",
            total_amount=6000,
            currency="KRW",
            status="pending",
            items=[
                {
                    "id": "item-order-123-coffee1",
                    "coffee_id": "coffee1",
                    "quantity": 2,
                    "unit_price": "3000 KRW",
                    "subtotal": "6000 KRW",
                }
            ],
        )
        self.use_case_mock.output_boundary.set_result(output_dto)

        # When: POST 요청
        response = self.client.post("/order", json={"customer_id": "customer1", "coffee_id": "coffee1", "quantity": 2})

        # Then: (1) Input DTO로의 변환 확인
        called_input_dto = self.use_case_mock.execute.call_args[0][0]
        self.assertIsInstance(called_input_dto, CreateOrderInputDto)  # (1) 컨트롤러가 올바른 DTO로 변환했는지 확인
        self.assertEqual(called_input_dto.customer_id, "customer1")  # (2) 고객 ID 매핑 확인
        self.assertEqual(called_input_dto.coffee_id, "coffee1")  # (3) 커피 ID 매핑 확인
        self.assertEqual(called_input_dto.quantity, 2)  # (4) 수량 매핑 확인

        # Then: (2) 응답 확인
        self.assertEqual(response.status_code, 200)  # (5) HTTP 200 OK 응답 확인
        self.assertEqual(  # (6) 응답 JSON 스냅샷 검증
            response.json(),
            {
                "status": "success",
                "data": {
                    "orderId": "order-123",
                    "customerId": "customer1",
                    "totalAmount": 6000,
                    "currency": "KRW",
                    "status": "pending",
                    "items": [
                        {
                            "id": "item-order-123-coffee1",
                            "coffee_id": "coffee1",
                            "quantity": 2,
                            "unit_price": "3000 KRW",
                            "subtotal": "6000 KRW",
                        }
                    ],
                },
                "message": "order created successfully",
            },
        )

    def test_create_order_failure(self):
        # Given: 모킹된 실패 응답
        self.use_case_mock.execute.side_effect = InvalidInputParameter("주문 불가능한 커피입니다")

        # When: POST 요청
        response = self.client.post("/order", json={"customer_id": "customer1", "coffee_id": "coffee2", "quantity": 1})

        # Then: (1) Input DTO로의 변환 확인
        called_input_dto = self.use_case_mock.execute.call_args[0][0]
        self.assertIsInstance(called_input_dto, CreateOrderInputDto)  # (7) 컨트롤러가 올바른 DTO로 변환했는지 확인
        self.assertEqual(called_input_dto.customer_id, "customer1")  # (8) 고객 ID 매핑 확인
        self.assertEqual(called_input_dto.coffee_id, "coffee2")  # (9) 커피 ID 매핑 확인
        self.assertEqual(called_input_dto.quantity, 1)  # (10) 수량 매핑 확인

        # Then: (2) 응답 확인
        self.assertEqual(response.status_code, 400)  # (11) HTTP 400 Bad Request 응답 확인
        response_data = response.json()
        print(response_data)
        self.assertEqual(response_data["status"], "failure")  # (12) 실패 상태 플래그 확인
        self.assertEqual(response_data["errorCode"], "1001")  # (13) 도메인 에러 코드 확인
        self.assertEqual(response_data["message"], "Bad Request")  # (14) 표준 에러 메시지 확인
        self.assertIn("주문 불가능한 커피입니다", response_data["debugMessage"])  # (15) 상세 디버그 메시지 포함 확인


if __name__ == "__main__":
    unittest.main()
