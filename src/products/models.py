from decimal import Decimal

from .money import CURRENCY_CHOICES, Money

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


def validate_empty(value):
    if value.strip() == '':
        raise ValidationError(u'This field must not be empty')


class UserSettings(models.Model):
    #user = models.OneToOneField(User)
    dollar_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.0'))]
    )


class Product(models.Model):
    name = models.CharField(
        max_length=255,
        validators=[validate_empty]
    )
    description = models.TextField(
        null=True,
        blank=True,
        max_length=1000
    )
    sku = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        validators=[validate_empty]
    )
    _price_in_units = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=False,
        null=False,
        validators=[MinValueValidator(Decimal('1'))]
    )
    _currency = models.CharField(
        max_length=30,
        default='nuevo',
        choices=CURRENCY_CHOICES
    )
    _weight_in_grams = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.0'))]
    )
    #fotos
    #precio_promocional
    #stock
    #categoria
    #variantes

    def __init__(self, *args, **kwargs):
        if 'price' in kwargs and type(kwargs['price']) == Money:
            price = kwargs['price']
            kwargs['_price_in_units'] = price.amount
            kwargs['_currency'] = price.currency
        super().__init__(*args, **kwargs)

    @property
    def weight(self):
        return None

    @property
    def price(self):
        return Money(
            amount=self._price_in_units,
            currency=self._currency,
            # use exchange rates from user settings
        )

    def __str__(self):
        return self.name
