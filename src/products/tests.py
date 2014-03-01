from decimal import Decimal

from django.test import TestCase

from .money import Money, ExchangeRates, CURRENCIES, ConvertError
from .models import Product

ARS = CURRENCIES['ARS']
USD = CURRENCIES['USD']


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

    def test_money_naive(self):
        money = Money(amount=Decimal('100.00'), currency=USD)
        self.assertEqual(money.is_naive(), True)
        self.assertEqual(money.is_aware(), False)

        # try setting exchange_rates as not ExchangeRates object
        money.exchange_rates = True
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

    def tearDown(self):
        pass

    def test_product_price_property(self):
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
