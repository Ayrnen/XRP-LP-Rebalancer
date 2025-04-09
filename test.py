from classes.config_reader import ConfigReader
from classes.runtime_tracker import RuntimeTracker
from classes.rpc_client import RPCClient

from classes.xrpl_address_client import XRPLAddressClient

from dotenv import load_dotenv
import os

class Placeholder:
    def __init__(self):
        pass
    


if __name__ == '__main__':
    rpc = RPCClient()
    connected, status_message = rpc.validate_connection_http()
    print(f"Connected: {connected} | Status: {status_message}")

    connected, status_message = rpc.validate_connection_wss()
    print(f"Connected: {connected} | Status: {status_message}")