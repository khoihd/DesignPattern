from unittest.mock import Mock


# =========================
# System Under Test
# =========================
class OrderService:
    def __init__(self, inventory, payment, email):
        self.inventory = inventory
        self.payment = payment
        self.email = email

    def place_order(self, product_id, amount, customer_email):
        if not self.inventory.is_available(product_id):
            return "OUT_OF_STOCK"

        if not self.payment.charge(amount):
            return "PAYMENT_FAILED"

        self.email.send(customer_email, "Order confirmed")

        return "SUCCESS"


# =========================
# Stub
# =========================
class InventoryStub:
    def is_available(self, product_id):
        return False


# =========================
# Fake
# =========================
class FakeInventory:
    def __init__(self):
        self.products = {}

    def add_product(self, product_id, quantity):
        self.products[product_id] = quantity

    def is_available(self, product_id):
        return self.products.get(product_id, 0) > 0


# =========================
# Spy
# =========================
class EmailSpy:
    def __init__(self):
        self.calls = []

    def send(self, address, message):
        self.calls.append((address, message))


# =========================
# Tests
# =========================
def test_dummy_and_stub():
    service = OrderService(
        inventory=InventoryStub(),  # Stub
        payment=None,  # Dummy
        email=None,  # Dummy
    )

    assert service.place_order(1, 100, "a@test.com") == "OUT_OF_STOCK"


def test_fake():
    inventory = FakeInventory()
    inventory.add_product(1, 5)

    assert inventory.is_available(1)
    assert not inventory.is_available(999)


def test_spy():
    inventory = FakeInventory()
    inventory.add_product(1, 5)

    payment = Mock()
    payment.charge.return_value = True

    email = EmailSpy()

    service = OrderService(inventory, payment, email)

    result = service.place_order(1, 100, "a@test.com")

    assert result == "SUCCESS"
    assert email.calls == [("a@test.com", "Order confirmed")]


def test_mock():
    inventory = Mock()
    inventory.is_available.return_value = True

    payment = Mock()
    payment.charge.return_value = True

    email = Mock()

    service = OrderService(inventory, payment, email)
    service.place_order(1, 100, "a@test.com")

    payment.charge.assert_called_once_with(100)
    email.send.assert_called_once_with("a@test.com", "Order confirmed")


if __name__ == "__main__":
    test_dummy_and_stub()
    test_fake()
    test_spy()
    test_mock()

    print("All 4 tests passed!")
