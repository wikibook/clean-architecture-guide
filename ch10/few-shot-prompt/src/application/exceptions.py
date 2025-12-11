class ApplicationError(Exception):
    """애플리케이션 기본 예외 클래스"""
    pass


class MenuNotFoundError(ApplicationError):
    """메뉴를 찾을 수 없을 때 발생하는 예외"""
    pass


class InsufficientStockError(ApplicationError):
    """재고가 부족할 때 발생하는 예외"""
    pass


class OrderNotFoundError(ApplicationError):
    """주문을 찾을 수 없을 때 발생하는 예외"""
    pass


class DatabaseError(ApplicationError):
    """데이터베이스 오류 발생 시 발생하는 예외"""
    pass