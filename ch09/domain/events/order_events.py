from domain.shared.aggregate_root import DomainEvent


class OrderCreated(DomainEvent):
    def __init__(self, order_id: str, customer_id: str):
        super().__init__(name="OrderCreated", payload={"order_id": order_id, "customer_id": customer_id})
        self.order_id = order_id
        self.customer_id = customer_id


class OrderItemAdded(DomainEvent):
    def __init__(self, order_id: str, item_id: str, coffee_id: str, quantity: int):
        super().__init__(
            name="OrderItemAdded",
            payload={"order_id": order_id, "item_id": item_id, "coffee_id": coffee_id, "quantity": quantity},
        )
        self.order_id = order_id
        self.item_id = item_id
        self.coffee_id = coffee_id
        self.quantity = quantity


class OrderStatusChanged(DomainEvent):
    def __init__(self, order_id: str, previous_status: str, new_status: str):
        super().__init__(
            name="OrderStatusChanged",
            payload={"order_id": order_id, "previous_status": previous_status, "new_status": new_status},
        )
        self.order_id = order_id
        self.previous_status = previous_status
        self.new_status = new_status

