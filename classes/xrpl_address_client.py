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
    
    def get_trust_line_info(self, token_address):
        try:
            raw_data, error = self.rpc.get_token_trust_line(self.address, token_address)
            if error:
                return None, error
            parsed_data = self._parse_trust_line_info(raw_data)
        except:
            return None, 'Error trust line information'
        return parsed_data, None
    def _parse_trust_line_info(self, raw_data):
        raise NotImplementedError('Parsing trust line information not implemented')
    
    def get_balance_token(self, token_address):
        try:
            raw_data, error = self.rpc.get_token_trust_line(self.address, token_address)
            if error:
                return None, error
            parsed_data = self._parse_token_balance(raw_data)
        except:
            return None, 'Error retrieving balance'
        return parsed_data, None
    def _parse_token_balance(self, raw_data):
        return raw_data['result']['lines'][0]['balance']
        

    def get_transaction_count(self):
        pass
    
    def get_lp_balance(self, lp_issuer, lp_token):
        try:
            raw_data, error = self.rpc.get_amm_position(self.address, lp_issuer, lp_token)
            if error:
                return None, error
            parsed_data = self._parse_lp_balance(raw_data)
        except:
            return None, 'Error retrieving balance'
        return parsed_data, None
    def _parse_lp_balance(self, raw_data):
        return raw_data['result']['lines'][0]['balance']

    async def get_pending_txns(self):
        pass