from classes.config_reader import ConfigReader
from classes.runtime_tracker import RuntimeTracker
from classes.rpc_client import RPCClient
from classes.address_client import AddressClient
from classes.amm_client import AMMClient
from classes.coinmarketcap_client import CoinMarketCapClient

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
     
    load_dotenv()
    address = os.getenv('ADDRESS')
    address_client = AddressClient(address)

    # print(address_client.get_balance_xrp())

    lp_token = config_reader.get_value('mainnet-lp-tokens', 'xrp_rlusd')
    lp_issuer = config_reader.get_value('mainnet-lp-issuers', 'xrp_rlusd')

    # print(address_client.get_lp_balance(lp_issuer, lp_token))
    xrp = 'XRP'
    rlusd = config_reader.get_value('mainnet-token-addresses', 'rlusd')
    breakdown = address_client.get_lp_breakdown(lp_token, lp_issuer, xrp, rlusd)


    # print(address_client.get_balance_token(rlusd))

    # print(address_client.get_trust_line_info(rlusd))


    # amm = AMMClient()
    # token1 = 'XRP'
    # token1 = config_reader.get_value('mainnet-token-addresses', 'rlusd')
    # token2 = config_reader.get_value('mainnet-token-addresses', 'mag')
    # issuer = config_reader.get_value('mainnet-lp-issuers', 'xrp_rlusd')
    # amm_info = amm.get_amm_details(issuer, token1, token2)
    # print(amm_info)
    
    cm = CoinMarketCapClient()
    xrp_id = config_reader.get_value('coinmarketcap-token-ids', 'xrp')
    xrp_price = cm.get_token_value_usd(xrp_id)
    print(xrp_price)

    rlusd_id = config_reader.get_value('coinmarketcap-token-ids', 'rlusd')
    rlusd_price = cm.get_token_value_usd(rlusd_id)
    print(rlusd_price)

    print(f"Dollar value of XRP portion of LP Position: {breakdown['assets']['xrp']['amount']*xrp_price}")
    print(f"Dollar value of RLUSD portion of LP Position: {breakdown['assets']['rlusd']['amount']*rlusd_price}")


    runtime_tracker.stop()