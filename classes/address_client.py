from classes.config_reader import ConfigReader
from classes.rpc_client import RPCClient
from classes.amm_client import AMMClient
from xrpl.core import addresscodec
from xrpl.core.addresscodec import XRPLAddressCodecException

class AddressClient:
    def __init__(self, address):
        self.config = ConfigReader()
        self.rpc = RPCClient()
        self.amm = AMMClient()
        self.address = address
        self._validate_address()

    def _validate_address(self):
        is_valid = (
            addresscodec.is_valid_classic_address(self.address) or 
            addresscodec.is_valid_xaddress(self.address)
        )
        if not is_valid:
            raise ValueError(f'Invalid XRPL address: {self.address}')
        
    def get_balance_xrp(self):
        return self.rpc.get_account_balance(self.address)
    
    def get_trust_line_info(self, token_address):
        raw_data = self.rpc.get_token_trust_line(self.address, token_address)
        parsed_data = self._parse_trust_line_info(raw_data)
        return parsed_data
    def _parse_trust_line_info(self, raw_data):
        raise NotImplementedError('Parsing trust line information not implemented')
    
    def get_balance_token(self, token_address):
        raw_data = self.rpc.get_token_trust_line(self.address, token_address)
        parsed_data = self._parse_token_balance(raw_data)
        return parsed_data, None
    def _parse_token_balance(self, raw_data):
        return raw_data['result']['lines'][0]['balance']
        

    def get_transaction_count(self):
        pass
    
    def get_lp_balance(self, lp_issuer, lp_token):
        raw_data = self.rpc.get_amm_position(self.address, lp_issuer, lp_token)
        parsed_data = self._parse_lp_balance(raw_data)
        return float(parsed_data)
    def _parse_lp_balance(self, raw_data):
        return raw_data['result']['lines'][0]['balance']

    def get_lp_breakdown(self, lp_token, lp_issuer, token1, token2):
        lp_token_amount = self.get_lp_balance(lp_issuer, lp_token)
        breakdown_data = self.amm.get_position_breakdown(lp_issuer, token1, token2, lp_token_amount)
        return breakdown_data


    async def get_pending_txns(self):
        pass