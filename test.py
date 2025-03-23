from classes.config_reader import ConfigReader
from classes.runtime_tracker import RuntimeTracker

from classes.xrpl_address_client import XRPLAddressClient

from dotenv import load_dotenv
import os

class Placeholder:
    def __init__(self):
        pass
    


if __name__ == '__main__':

    address = os.getenv('ADDRESS')
    address_client = XRPLAddressClient()