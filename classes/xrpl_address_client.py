from classes.config_reader import ConfigReader
from classes.rpc_client import RPCClient
from xrpl.core import addresscodec
from xrpl.core.addresscodec import XRPLAddressCodecException

class XRPLAddressClient:
    def __init__(self, address):
        self.config = ConfigReader()
        self.rpc = RPCClient()
        self.address = address
        self._validate_address()

    def _validate_address(self):
        try:
            is_valid = (
                addresscodec.is_valid_classic_address(self.address) or 
                addresscodec.is_valid_xaddress(self.address)
            )
            if not is_valid:
                raise ValueError(f'Invalid XRPL address: {self.address}')
            
        except XRPLAddressCodecException as e:
            raise ValueError(f'Address validation failed: {str(e)}') from e
        except TypeError:
            raise ValueError('Address must be a string') from None
        
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