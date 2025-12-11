class Money:
    def __init__(self, amount: int, currency: str = "KRW"):
        if amount < 0:
            raise ValueError("금액은 0 이상이어야 합니다")
        if currency not in ["USD", "KRW"]:
            raise ValueError("지원되지 않는 통화입니다")
        self.amount = amount
        self.currency = currency

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("통화가 일치하지 않습니다")
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def __mul__(self, quantity: int) -> "Money":
        if quantity < 0:
            raise ValueError("수량은 0 이상이어야 합니다")
        return Money(amount=self.amount * quantity, currency=self.currency)

    def __str__(self) -> str:
        return f"{self.amount} {self.currency}"

    def __repr__(self) -> str:
        return f"Money(amount={self.amount}, currency='{self.currency}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return False
        return self.amount == other.amount and self.currency == other.currency
