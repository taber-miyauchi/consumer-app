"""Invoice generation module using shared utilities."""

from shared_utils import Calculator, format_currency, format_percentage


class Invoice:
    """Invoice generator that uses shared-utils for calculations."""

    def __init__(self, customer_name: str, tax_rate: float = 0.08):
        self.customer_name = customer_name
        self.tax_rate = tax_rate
        self.items: list[tuple[str, float, int]] = []
        self.calc = Calculator(precision=2)

    def add_item(self, name: str, price: float, quantity: int = 1) -> None:
        self.items.append((name, price, quantity))

    def calculate_subtotal(self) -> float:
        total = 0.0
        for _, price, quantity in self.items:
            total = self.calc.add(total, self.calc.multiply(price, quantity))
        return total

    def calculate_tax(self) -> float:
        subtotal = self.calculate_subtotal()
        return self.calc.multiply(subtotal, self.tax_rate)

    def calculate_total(self) -> float:
        return self.calc.add(self.calculate_subtotal(), self.calculate_tax())

    def generate_summary(self) -> str:
        subtotal = self.calculate_subtotal()
        tax = self.calculate_tax()
        total = self.calculate_total()

        lines = [
            f"Invoice for: {self.customer_name}",
            "-" * 40,
        ]

        for name, price, qty in self.items:
            item_total = self.calc.multiply(price, qty)
            lines.append(f"  {name} x{qty}: {format_currency(item_total)}")

        lines.extend([
            "-" * 40,
            f"Subtotal: {format_currency(subtotal)}",
            f"Tax ({format_percentage(self.tax_rate)}): {format_currency(tax)}",
            f"Total: {format_currency(total)}",
        ])

        return "\n".join(lines)
