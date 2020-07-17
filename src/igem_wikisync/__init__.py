__version__ = '0.0.0-alpha.7'

import ssl
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager


# For TLSv1.0 support
# https://lukasa.co.uk/2013/01/Choosing_SSL_Version_In_Requests/

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

from igem_wikisync.core import *