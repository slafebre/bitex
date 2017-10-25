"""
https://cex.io/rest-api/
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.REST.rest import CexioREST
from bitex.utils import return_api_response
from bitex.formatters.cexio import CexioFormatter as fmt
# Init Logging Facilities
log = logging.getLogger(__name__)


class Cexio(CexioREST):
    def __init__(self, key='', secret='', key_file='', websocket=False):
        super(Cexio, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)
        if websocket:
            raise NotImplementedError
            # self.wss = BitfinexWSS()
            # self.wss.start()
        else:
            self.wss = None

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, **kwargs)

    def private_query(self, endpoint, **kwargs):
        return self.query('POST', endpoint, authenticate=True, **kwargs)

    """
    Cexio Standardized Methods
    """
    @return_api_response(fmt.order_book)
    def order_book(self, pair, **kwargs):
        quote_currency, base_currency = pair[:3], pair[-3:]
        return self.public_query(
            'order_book/%s/%s/' % (quote_currency, base_currency),
            params=kwargs)

    @return_api_response(fmt.ticker)
    def ticker(self, pair, **kwargs):
        quote_currency = pair[-3:]
        return self.public_query('tickers/%s' % quote_currency)

    @return_api_response(fmt.trades)
    def trades(self, pair, **kwargs):
        quote_currency, base_currency = pair[:3], pair[-3:]
        return self.public_query(
            'trade_history/%s/%s/' % (quote_currency, base_currency),
            params=kwargs)

    def _place_order(self, pair, size, price, side, replace, **kwargs):
        quote_currency, base_currency = pair[:3], pair[-3:]
        q = {'amount': size, 'price': price, 'type': side}
        q.update(kwargs)
        if replace:
            raise NotImplementedError
        else:
            return self.private_query(
                'place_order/%s/%s' % (quote_currency, base_currency), params=q)

    @return_api_response(fmt.order)
    def bid(self, pair, price, size, replace=False, **kwargs):
        return self._place_order(pair, size, price, 'buy',
                                 replace=replace, **kwargs)

    @return_api_response(fmt.order)
    def ask(self, pair, price, size, replace=False, **kwargs):
        return self._place_order(pair, size, price, 'sell',
                                 replace=replace, **kwargs)

    @return_api_response(fmt.cancel)
    def cancel_order(self, order_id, all=False, **kwargs):
        q = {'id': int(order_id)}
        q.update(kwargs)
        if not all:
            return self.private_query('cancel_order/', params=q)
        else:
            raise NotImplementedError

    @return_api_response(fmt.order_status)
    def order(self, order_id, **kwargs):
        q = {'id': order_id}
        q.update(kwargs)
        return self.private_query('get_order/', params=q)

    @return_api_response(fmt.balance)
    def balance(self, **kwargs):
        return self.private_query('balance/', params=kwargs)

    @return_api_response(fmt.withdraw)
    def withdraw(self, size, tar_addr, **kwargs):
        raise NotImplementedError

    @return_api_response(fmt.deposit)
    def deposit_address(self, **kwargs):
        raise NotImplementedError

    """
    Exchange Specific Methods
    """

    @return_api_response(None)
    def orders(self):
        return self.private_query('open_orders/')

    @return_api_response(None)
    def balance_history(self, currency, **kwargs):
        raise NotImplementedError
        q = {'currency': currency}
        q.update(kwargs)
        return self.private_query('history/movements', params=q)

    @return_api_response(None)
    def trade_history(self, pair, since, **kwargs):
        raise NotImplementedError
        q = {'symbol': pair, 'timestamp': since}
        q.update(kwargs)
        return self.private_query('mytrades', params=q)

    @return_api_response(None)
    def positions(self):
        raise NotImplementedError
        return self.private_query('positions')
