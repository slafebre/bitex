# Import Built-ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.formatters.base import Formatter


log = logging.getLogger(__name__)


class CexioFormatter(Formatter):

    @staticmethod
    def ticker(data, *args, **kwargs):
        pair = args[1]
        for ticker in data['data']:
            if ticker['pair'] == pair:
                break
        else:
            return tuple([None] * 9)
        return (ticker['bid'], ticker['ask'], ticker['high'], ticker['low'],
                None, None, ticker['last'], ticker['volume'], ticker['timestamp'])

    @staticmethod
    def order(data, *args, **kwargs):
        try:
            return data['order_id']
        except KeyError:
            return False

    @staticmethod
    def cancel(data, *args, **kwargs):
        return data == True

    @staticmethod
    def order_status(data, *args, **kwargs):
        return data['status']
