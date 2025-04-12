from classes.rpc_client import RPCClient


class AMMClient:
    def __init__(self):
        self.rpc = RPCClient()

    def get_amm_details(self, issuer, token1, token2):
        raw_data = self.rpc.get_amm_details(issuer, token1, token2)
        code1 = self.hex_to_code(token1)
        code2 = self.hex_to_code(token2)
        parsed_data = self._parse_amm_details(raw_data, code1, code2)
        return parsed_data

    def _parse_amm_details(self, raw_data, code1, code2):
        print(raw_data)
        data = raw_data[0]['amm']

        dict_return = {
            'lp_token': data['lp_token']['currency'],
            'lp_issuer': data['lp_token']['issuer'],
            # value?
            f'{code1}_frozen': data.get('asset1_frozen', None),
            f'{code2}_frozen': data.get('asset2_frozen', None),
        }
        
        print(data)
        print(type(data))
        return dict_return

    def hex_to_code(self, token_input):
        if token_input == 'XRP':
            return token_input.lower()
        
        else:
            token_code = token_input.split(':')[0]
            if len(token_code) == 3:
                return token_code.lower()
            else:
                bytes_data = bytes.fromhex(token_code)
                decoded = bytes_data.decode('utf-8').rstrip('\x00')
                return decoded.lower()

    # To eventually cache AMM details
    def populate_amm_details(self, issuer, token1, token2):
        pass