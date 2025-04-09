import requests
import websocket
import json
from dotenv import load_dotenv
from classes.config_reader import ConfigReader
import os



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
            # Create connection with 5-second timeout
            ws = websocket.create_connection(
                self.ws_url,
                # header=['Authorization: Bearer {}'.format(self.api_key)],
                timeout=5
            )
            
            # Test connection with ping/pong
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
        try:
            response = requests.post(
                url=self.http_url,
                json={'method': 'server_info', 'params': [{}]},
                timeout=5
            )
            
            # Check for successful response
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
            
            print(data.get('result', {}))
            
            if not balance_drops:
                return None, 'No balance found in response'
            
            return int(balance_drops) / 1_000_000, None  # Convert drops to XRP

        except requests.exceptions.RequestException as e:
            return None, f'Connection error: {str(e)}'
        except ValueError:
            return None, 'Invalid JSON response'
        except KeyError:
            return None, 'Unexpected response format'