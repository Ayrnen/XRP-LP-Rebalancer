from classes.config_reader import ConfigReader
from classes.runtime_tracker import RuntimeTracker
from classes.rpc_client import RPCClient
from classes.xrpl_address_client import XRPLAddressClient
from classes.amm_client import AMMClient

from dotenv import load_dotenv
import os

class Placeholder:
    def __init__(self):
        pass
    


if __name__ == '__main__':
    runtime_tracker = RuntimeTracker()
    runtime_tracker.start()
    config_reader = ConfigReader()

    # rpc = RPCClient()
    # connected, status_message = rpc.validate_connection_http()
    # print(f"Connected: {connected} | Status: {status_message}")

    # connected, status_message = rpc.validate_connection_wss()
    # print(f"Connected: {connected} | Status: {status_message}")
     
    # load_dotenv()
    # address = os.getenv('TEST_ADDRESS')
    # address_client = XRPLAddressClient(address)
    # print(address_client._validate_address())
    # print(address_client.get_balance_xrp())

    amm = AMMClient()
    token1 = 'XRP'
    token2 = config_reader.get_value('mainnet-token-addresses', 'rlusd')
    issuer = config_reader.get_value('mainnet-amm-info', 'xrp_rlusd_issuer')
    amm_info = amm.get_amm_details(issuer, token1, token2)
    print(amm_info)
    

    runtime_tracker.stop()