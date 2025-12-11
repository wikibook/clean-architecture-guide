from unittest.mock import Mock
import unittest

from application.usecases.create_order_usecase import (
    CreateOrderUseCase,
    CreateOrderInputDto,
    CreateOrderOutputDto,
)
from domain.entities.coffee import Coffee
from domain.value_objects.money import Money
from domain.exceptions import InvalidInputParameter


class TestCreateOrderUseCase(unittest.TestCase):
    def setUp(self):
        # 의존성 모킹
        self.output_boundary = Mock()
        self.coffee_repo = Mock()
        self.order_repo = Mock()

        # 유스케이스 초기화
        self.use_case = CreateOrderUseCase(
            output_boundary=self.output_boundary, coffee_repo=self.coffee_repo, order_repo=self.order_repo
        )

    def test_execute_success(self):
        # Given: 정상적인 입력 DTO와 모킹된 커피
        input_dto = CreateOrderInputDto(customer_id="customer1", coffee_id="coffee1", quantity=2)
        coffee = Coffee(id="coffee1", name="아메리카노", price=Money(amount=3000), description="깔끔한 아메리카노", stock=10)
        self.coffee_repo.find_by_id.return_value = coffee

        # When: 유스케이스 실행
        self.use_case.execute(input_dto)

        # Then: 의존성이 올바르게 호출되었는지 확인
        self.order_repo.save.assert_called_once()  # (1) 주문 저장 호출 확인
        self.coffee_repo.save.assert_called_once()  # (2) 커피 저장(재고 감소 반영) 호출 확인
        self.output_boundary.set_result.assert_called_once()  # (3) 출력 결과 설정 호출 확인

        # 출력 DTO 구조 확인
        called_output_dto = self.output_boundary.set_result.call_args[0][0]
        self.assertIsInstance(called_output_dto, CreateOrderOutputDto)  # (4) 결과 타입 확인
        self.assertEqual(called_output_dto.customer_id, "customer1")  # (5) 고객 ID 매핑 확인
        self.assertIsInstance(called_output_dto.total_amount, int)  # (6) 총액 타입(int) 확인
        self.assertIsInstance(called_output_dto.currency, str)  # (7) 통화 타입(str) 확인
        self.assertIsInstance(called_output_dto.status, str)  # (8) 주문 상태 타입(str) 확인
        self.assertEqual(len(called_output_dto.items), 1)  # (9) 아이템 1개 추가되었는지 확인

    def test_execute_unavailable_coffee(self):
        # Given: 주문 불가능한 커피 (재고 부족)
        input_dto = CreateOrderInputDto(customer_id="customer1", coffee_id="coffee2", quantity=1)
        coffee = Coffee(id="coffee2", name="라떼", price=Money(amount=4000), description="부드러운 라떼", stock=0)
        self.coffee_repo.find_by_id.return_value = coffee

        # When & Then: 예외 발생 확인
        with self.assertRaises(InvalidInputParameter) as context:
            self.use_case.execute(input_dto)

        # 예외의 debug_message 확인
        self.assertEqual(context.exception.get_debug_message(), "주문 불가능한 커피입니다")  # (10) 예외 메시지 확인


if __name__ == "__main__":
    unittest.main()
