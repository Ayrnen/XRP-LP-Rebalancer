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
        self.api_key = ''

        self.config = ConfigReader()

        self.ws_url = self.config.get_value('rpc-links', 'mainnet_wss') + self.api_key
        self.http_url = self.config.get_value('rpc-links', 'mainnet_https') + self.api_key

        # self.web3 = Web3(Web3.HTTPProvider(self.http_url))
        # if not self.web3.is_connected():
        #     raise ConnectionError('Failed to connect to Web3 provider')

    def get_account_balance(self, address):
        payload = {
            'method': 'account_info',
            'params': [
                {
                    'account': address,
                    'strict': True,
                    'ledger_index': 'validated',
                    'queue': True
                }
            ]
        }
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.post(self.http_url, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            balance = result['result']['account_data']['Balance']
            return balance
        else:
            raise Exception(f'HTTP Error: {response.status_code}, {response.text}')