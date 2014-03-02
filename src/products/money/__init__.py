"""Let's talk about Money"""
import functools

from .exceptions import ConvertError

__all__ = ['Money', 'Currency', 'ExchangeRates', 'ConvertError']


class Currency:
    def __init__(self, currency_id, name, symbol):
        self.currency_id = currency_id
        self.name = name
        self.symbol = symbol

    def __str__(self):
        return u'{0} ({1})'.format(self.name, self.symbol)

    def __repr__(self):
        return "Currency<{0}, {1}, {2}>".format(
            self.currency_id, self.name, self.symbol)

    def __eq__(self, other):
        for field in ['currency_id', 'name', 'symbol']:
            if getattr(self, field) != getattr(other, field):
                return False
        return True


class ExchangeRates:
    def __init__(self, rates):
        """Objects of this class are aware about exchange rates from
           one currency to other ones. 'rates' is a mapping that must
           have the following format:
           {
                'ARS_USD': Decimal(...),
                'USD_ARS': Decimal(...),
                ...
           }
        """
        self.rates = rates

    def get_rate(self, currency_from, currency_to):
        key = u'{0}_{1}'.format(currency_from.currency_id,
                                currency_to.currency_id)
        return self.rates.get(key, None)


@functools.total_ordering
class Money:
    """Base class to represent money"""
    def __init__(self, amount, currency, exchange_rates=None):
        self.amount = amount
        self.currency = currency
        self.exchange_rates = exchange_rates

    def is_aware(self):
        return self.exchange_rates is not None

    def is_naive(self):
        return self.exchange_rates is None

    def convert_to(self, new_currency):
        """Converts the Money object from current currency to 'new_currency'.
           if object is Naive or given exchange rate is not defined
           ConvertError is raised.
           A Money object with 'new_currency' is returned.
        """
        if not self.is_aware():
            raise ConvertError("Naive Money objects don't know how to convert")

        rate = self.exchange_rates.get_rate(self.currency, new_currency)
        if rate is None:
            raise ConvertError('Exchange rate from {0} to {1} is not '
                               'defined'.format(self.currency, new_currency))
        return Money(
            currency=new_currency,
            exchange_rates=self.exchange_rates,
            amount=self.amount * rate
        )

    def __add__(self, other):
        """Returns the sum of two Money objects
           if both Money objects have different currencies, the second
           one is converted to the first currency, and a Money object with
           the sum of both and the currency of the first is returned.
        """
        if self.currency != other.currency:
            other = other.convert_to(self.currency)
        return Money(
            amount=self.amount + other.amount,
            currency=self.currency,
            exchange_rates=self.exchange_rates
        )

    def __str__(self):
        return u'{0} {1}'.format(self.currency.symbol, self.amount)

    def __lt__(self, other):
        if self.currency != other.currency:
            raise ValueError("Can't compare money in different currency.")

        return self.amount < other.amount

    def __eq__(self, other):
        return (
            self.currency == other.currency
            and self.amount == other.amount
            and self.is_aware() == other.is_aware()
        )

    __radd__ = __add__