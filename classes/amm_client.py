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
        try:
            amm_data = raw_data[0]['amm']
            dict_return = {
                'lp_token': amm_data['lp_token']['currency'],
                'lp_issuer': amm_data['lp_token']['issuer'],
                'lp_token_amount': amm_data['lp_token']['value'],

                'asset1': code1,
                'asset2': code2,
                'asset1_frozen': amm_data.get('asset_frozen', None),
                'asset2_frozen': amm_data.get('asset2_frozen', None),
                'asset2_issuer': amm_data['amount2']['issuer'],
                'asset2_amount': amm_data['amount2']['value'],
            }
            if type(amm_data['amount']) == str:
                dict_return['asset1_issuer'] = None
                dict_return['asset1_amount'] = float(amm_data['amount']) / 1000000
            elif type(amm_data['amount']) == dict:
                dict_return['asset1_issuer'] = amm_data['amount']['issuer']
                dict_return['asset1_amount'] = amm_data['amount']['value']
            else:
                raise ValueError(f'Unexpected type for "amount": {type(amm_data["amount"])}')
        except:
            raise ValueError(f'Unexpected response from AMM API: {raw_data}')
    
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

    # Turns LP tokens count into pair token count
    def get_position_breakdown(self, lp_issuer, token1, token2, lp_token_amount):
        amm_details = self.get_amm_details(lp_issuer, token1, token2)
        
        total_lp = float(amm_details['lp_token_amount'])
        asset1_reserve = float(amm_details['asset1_amount'])
        asset2_reserve = float(amm_details['asset2_amount'])
        
        if total_lp <= 0:
            raise ValueError("Invalid total LP supply - pool may be inactive")
            
        ownership_pct = lp_token_amount / total_lp
        asset1_amount = ownership_pct * asset1_reserve
        asset2_amount = ownership_pct * asset2_reserve

        breakdown = {
            'lp_tokens': lp_token_amount,
            'ownership_percentage': round(ownership_pct * 100, 4),
            'assets': {
                amm_details['asset1']: {
                    'amount': asset1_amount,
                    'issuer': amm_details.get('asset1_issuer'),
                    'type': 'XRP' if amm_details['asset1'] == 'xrp' else 'issued'
                },
                amm_details['asset2']: {
                    'amount': asset2_amount,
                    'issuer': amm_details['asset2_issuer'],
                    'type': 'XRP' if amm_details['asset2'] == 'xrp' else 'issued'
                }
            },
            'pool_metrics': {
                'total_liquidity': total_lp,
                'trading_fee_bps': amm_details.get('trading_fee', 'N/A'),
                'frozen_status': {
                    'asset1': amm_details.get('asset1_frozen', False),
                    'asset2': amm_details.get('asset2_frozen', False)
                }
            }
        }

        if amm_details['asset1'] == 'xrp':
            breakdown['assets']['xrp']['amount_xrp'] = asset1_amount
        if amm_details['asset2'] == 'xrp':
            breakdown['assets']['xrp']['amount_xrp'] = asset2_amount

        return breakdown

    # To eventually cache AMM details
    def populate_amm_details(self, issuer, token1, token2):
        pass