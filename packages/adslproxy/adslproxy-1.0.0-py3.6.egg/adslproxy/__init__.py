__version__ = '1.0.0'
from adslproxy.db import RedisClient
from adslproxy.api import server

def version():
    return __version__

