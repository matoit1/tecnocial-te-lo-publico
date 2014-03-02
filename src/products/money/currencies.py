from . import Currency

ARS = Currency(currency_id='ARS', name='Argentine Peso', symbol='$')
USD = Currency(currency_id='USD', name='US Dollar', symbol='U$D')

REGISTERED_CURRENCIES = {
    'ARS': ARS,
    'USD': USD
}


