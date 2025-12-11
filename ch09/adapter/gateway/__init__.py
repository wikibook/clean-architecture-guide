import requests

from application.ports.outbound import PaymentGateway


class InMemoryPaymentGateway(PaymentGateway):
    """데모를 위한 인메모리 결제 게이트웨이. 항상 승인합니다."""

    def approve(self, order_id: str, amount: int, currency: str) -> bool:  # noqa: ARG002 (단순 데모)
        # 실제로는 외부 API 호출
        # return requests.post("https://pg.example.com/approve", ...)
        return True  # 데모용 항상 성공


class TozzPaymentGateway(PaymentGateway):
    """데모를 위한 Tozz 결제 게이트웨이 예시"""
    def approve(self, order_id: str, amount: int, currency: str) -> bool:
        try:
            response = requests.post(
                "https://api.tozzpayments.com/v1/payments",
                json={"amount": amount, "orderId": order_id},
                timeout=5  # 5초 제한
            )
            return response.status_code == 200
        except (requests.Timeout, requests.ConnectionError):
            return False  # 네트워크 장애
        except Exception:
            return False  # PG사 서버 오류
