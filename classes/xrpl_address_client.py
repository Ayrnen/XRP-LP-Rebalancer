from classes.config_reader import ConfigReader
from classes.rpc_client import RPCClient

class XRPLAddressClient:
    def __init__(self, address):
        self.config = ConfigReader()
        self.rpc = RPCClient()
        self.address = address
        
    def get_balance_xrp(self):
        return self.rpc.get_account_balance(self.address)
    
    def get_balance_token(self, token_address):
        pass

    def get_transaction_count(self):
        pass
    
    def get_lp_position(self, lp_address, lp_abi):
        pass

    async def get_pending_txns(self):
        pass