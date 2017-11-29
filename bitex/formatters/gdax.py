# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.formatters.base import Formatter

# Init Logging Facilities
log = logging.getLogger(__name__)


class GdaxFormatter(Formatter):

    @staticmethod
    def ticker(data, *args, **kwargs):
        return (data['bid'], data['ask'], None, None, None, None, data['price'],
                data['volume'], data['time'])

    @staticmethod
    def order_book(data, *args, **kwargs):
        return {
            'bids': [d[:2] for d in data['bids']],
            'asks': [d[:2] for d in data['asks']]
        }
