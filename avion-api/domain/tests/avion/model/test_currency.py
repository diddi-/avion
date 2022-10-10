from unittest import TestCase

from avion.model.currency import Currency


class TestCurrency(TestCase):

    def test_currency_can_be_cast_to_int(self):
        self.assertEqual(1, int(Currency(1)))

    def test_currency_can_be_compared_with_another_currency(self):
        self.assertGreater(Currency(10), Currency(1))
        self.assertLess(Currency(1), Currency(10))
        self.assertEqual(Currency(10), Currency(10))

    def test_currency_supports_math_operations(self):
        self.assertEqual(Currency(10), Currency(5) + Currency(5))
        self.assertEqual(Currency(10), Currency(20) - Currency(10))
        self.assertEqual(Currency(10), Currency(5) * Currency(2))
        self.assertEqual(Currency(10), Currency(100) / Currency(10))
