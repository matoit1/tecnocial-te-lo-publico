from decimal import Decimal

from django.test import TestCase

from .money import Money, ExchangeRates, ConvertError, currencies
from .models import Product

ARS = currencies.ARS
USD = currencies.USD


class TestMoney(TestCase):
    def setUp(self):
        rates = {
            'ARS_USD': Decimal('0.10'),
            'USD_ARS': Decimal('10.00')
        }
        self.exchange_rates = ExchangeRates(rates)

    def tearDown(self):
        pass

    def test_money_str(self):
        money = Money(amount=Decimal('100.00'), currency=USD)
        self.assertEqual(str(money), u'U$D 100.00')

    def test_money_eq_true(self):
        m1 = Money(amount=Decimal('100.00'), currency=USD)
        m2 = Money(amount=Decimal('100.00'), currency=USD)
        self.assertTrue(m1 == m2)

    def test_money_eq_false(self):
        # different amount
        m1 = Money(amount=Decimal('101.00'), currency=USD)
        m2 = Money(amount=Decimal('100.00'), currency=USD)
        self.assertFalse(m1 == m2)

        # different currency
        m1 = Money(amount=Decimal('100.00'), currency=USD)
        m2 = Money(amount=Decimal('100.00'), currency=ARS)
        self.assertFalse(m1 == m2)

        # different xrates
        m1 = Money(amount=Decimal('100.00'), currency=USD)
        m2 = Money(amount=Decimal('100.00'), currency=ARS,
                   exchange_rates=self.exchange_rates)
        self.assertFalse(m1 == m2)

    def test_money_rich_comparison_same_currency(self):
        m1 = Money(amount=Decimal('1'), currency=USD)
        m2 = Money(amount=Decimal('2'), currency=USD)

        self.assertTrue(m1 < m2)
        self.assertTrue(m1 <= m2)
        self.assertTrue(m2 > m1)
        self.assertTrue(m2 >= m1)

        self.assertTrue(m1 <= m1)
        self.assertTrue(m1 >= m1)

    def test_money_rich_comparison_different_currency(self):
        m1 = Money(amount=Decimal('1'), currency=USD)
        m2 = Money(amount=Decimal('1'), currency=ARS)

        with self.assertRaises(ValueError):
            self.assertTrue(m1 < m2)

        with self.assertRaises(ValueError):
            self.assertTrue(m1 <= m2)

        with self.assertRaises(ValueError):
            self.assertTrue(m2 > m1)

        with self.assertRaises(ValueError):
            self.assertTrue(m2 >= m1)

    def test_money_naive(self):
        money = Money(amount=Decimal('100.00'), currency=USD)
        self.assertEqual(money.is_naive(), True)
        self.assertEqual(money.is_aware(), False)

    def test_money_aware(self):
        money = Money(
            amount=Decimal('100.00'),
            currency=USD,
            exchange_rates=self.exchange_rates
        )
        self.assertEqual(money.is_naive(), False)
        self.assertEqual(money.is_aware(), True)

    def test_money_convert(self):
        money_in_dollar = Money(
            amount=Decimal('100.00'),
            currency=USD,
            exchange_rates=self.exchange_rates
        )
        money_in_peso = Money(
            amount=Decimal('1000.00'),
            currency=ARS,
            exchange_rates=self.exchange_rates
        )
        self.assertEqual(money_in_dollar.convert_to(ARS), money_in_peso)
        self.assertEqual(money_in_peso.convert_to(USD), money_in_dollar)

    def test_money_convert_naive(self):
        money = Money(
            amount=Decimal('100.00'),
            currency=USD,
            exchange_rates=None
        )
        self.assertTrue(money.is_naive())
        self.assertRaises(ConvertError, money.convert_to, ARS)

    def test_money_add_same_currency(self):
        m1 = Money(
            amount=Decimal('100.00'),
            currency=ARS,
            exchange_rates=self.exchange_rates
        )
        m2 = Money(
            amount=Decimal('50.00'),
            currency=ARS,
            exchange_rates=self.exchange_rates
        )
        m3 = Money(
            amount=Decimal('150.00'),
            currency=ARS,
            exchange_rates=self.exchange_rates
        )
        self.assertEqual(m1 + m2, m3)

    def test_money_add_different_currency(self):
        m1 = Money(
            amount=Decimal('100.00'),
            currency=ARS,
            exchange_rates=self.exchange_rates
        )
        m2 = Money(
            amount=Decimal('5.00'),
            currency=USD,
            exchange_rates=self.exchange_rates
        )
        m3 = Money(
            amount=Decimal('150.00'),
            currency=ARS,
            exchange_rates=self.exchange_rates
        )
        self.assertEqual(m1 + m2, m3)


class TestProductModel(TestCase):
    def setUp(self):
        pass

    def test_product_construction_in_init(self):
        price = Money(
            amount=Decimal('100.00'),
            currency=USD
        )
        product = Product(
            name='Mother MSI px8172MA',
            price=price
        )
        self.assertEqual(product.price, price)
        self.assertEqual(product._price_in_units, Decimal('100.00'))
        self.assertEqual(product._currency, USD)
        self.assertIsNone(product.id)

    def test_product_construction_in_manager(self):
        price = Money(
            amount=Decimal('100.00'),
            currency=USD
        )
        product = Product.objects.create(
            name='Mother MSI px8172MA',
            price=price
        )
        self.assertEqual(product.price, price)
        self.assertEqual(product._price_in_units, Decimal('100.00'))
        self.assertEqual(product._currency, USD)
        self.assertIsNotNone(product.id)