import requests
import websocket
import json
from dotenv import load_dotenv
from classes.config_reader import ConfigReader
import os
from xrpl.core import addresscodec


class RPCClient:
    def __init__(self):

        load_dotenv()
        self.api_key = os.getenv('API_KEY')

        self.config = ConfigReader()

        self.ws_url = self.config.get_value('rpc-links', 'mainnet_wss') + self.api_key
        self.http_url = self.config.get_value('rpc-links', 'mainnet_https') + self.api_key

    def validate_connection_wss(self):
        print(self.ws_url)
        try:
            ws = websocket.create_connection(self.ws_url, timeout=5)
            ws.ping()
            ws.close()
            return True, 'WebSocket connection successful'
            
        except websocket.WebSocketTimeoutException:
            return False, 'Connection timed out (5s)'
        except websocket.WebSocketBadStatusException as e:
            return False, f'Auth failed: {e}'
        except Exception as e:
            return False, f'WebSocket error: {str(e)}'

    def validate_connection_http(self):
        print(self.http_url)
        try:
            response = requests.post(
                url=self.http_url,
                json={'method': 'server_info', 'params': [{}]},
                timeout=5
            )
            
            if response.status_code == 200:
                return True, 'Connection validated successfully'
            return False, f'Server returned {response.status_code} status'

        except requests.exceptions.RequestException as e:
            return False, f'Connection failed: {str(e)}'
        

    def get_account_balance(self, address):
        payload = {
            'method': 'account_info',
            'params': [{
                'account': address,
                'ledger_index': 'validated'
            }]
        }

        try:
            response = requests.post(
                self.http_url,
                json=payload,
                timeout=5
            )
            response.raise_for_status()
            data = response.json()

            if 'error' in data:
                return None, f"RPC Error: {data['error'].get('message', 'Unknown error')}"

            balance_drops = data.get('result', {})\
                                .get('account_data', {})\
                                .get('Balance')
            
            if not balance_drops:
                return None, 'No balance found in response'
            
            return int(balance_drops) / 1_000_000, None  # Convert drops to XRP

        except requests.exceptions.RequestException as e:
            return None, f'Connection error: {str(e)}'
        except ValueError:
            return None, 'Invalid JSON response'
        except KeyError:
            return None, 'Unexpected response format'
        

    def get_amm_position(self, address, token1: str, token2: str):
        try:
            asset1 = self._validate_parse_token(token1)
            asset2 = self._validate_parse_token(token2)
            
            payload = {
                'method': 'amm_info',
                'params': [{
                    'asset': asset1,
                    'asset2': asset2,
                    'account': address
                }]
            }
            response = requests.post(
                self.http_url,
                json=payload,
                timeout=5
            )
            
            data = response.json()
            if error := data.get('error'):
                return None, error.get('message', 'Unknown RPC error')
                
            return data.get('result'), None

        except ValueError as e:
            return None, str(e)
        except Exception as e:
            return None, f'Connection error: {str(e)}'
        
    def _validate_parse_token(self, token: str) -> dict:
        if token.upper() == 'XRP':
            return {'currency': 'XRP'}
            
        if ':' in token:
            currency, issuer = token.split(':', 1)
            if addresscodec.is_valid_classic_address(issuer)\
            and (len(currency) == 3 or len(currency) == 40):
                return {'currency': currency, 'issuer': issuer}
                
        raise ValueError(f'Invalid asset format: {token}')