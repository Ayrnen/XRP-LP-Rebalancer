import json
import logging
import requests
import os
from dotenv import load_dotenv

class CoinMarketCapClient:
    def __init__(self):
        # Load API key from environment variables
        load_dotenv()
        self.api_key = os.getenv('COINMARKETCAP_API_KEY')
        if not self.api_key:
            raise ValueError("COINMARKETCAP_API_KEY not found in environment variables. Please set this environment variable with your CoinMarketCap API key.")
        
        self.base_url = "https://pro-api.coinmarketcap.com/v1"
        self.logger = logging.getLogger(__name__)
    
    def get_token_value_usd(self, token_id):
        """
        Get the USD value of a token using the CoinMarketCap API.
        
        Args:
            token_id: The CoinMarketCap ID or symbol of the token
            
        Returns:
            float: The USD price of the token
        """
        try:
            # Determine if token_id is a symbol or slug
            if token_id.islower() and not token_id.isdigit():
                # It's likely a slug (like 'bitcoin', 'ethereum')
                endpoint = f"{self.base_url}/cryptocurrency/quotes/latest"
                params = {
                    'slug': token_id,
                    'convert': 'USD'
                }
            else:
                # It's likely a symbol (like 'BTC', 'ETH') or an ID
                endpoint = f"{self.base_url}/cryptocurrency/quotes/latest"
                params = {
                    'symbol': token_id,
                    'convert': 'USD'
                }
            
            headers = {
                'X-CMC_PRO_API_KEY': self.api_key,
                'Accept': 'application/json'
            }
            
            response = requests.get(endpoint, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract the USD price
            if 'data' in data and data['data']:
                # Get the first item in the data dictionary
                first_id = next(iter(data['data']))
                return float(data['data'][first_id]['quote']['USD']['price'])
            else:
                error_msg = data.get('status', {}).get('error_message', 'Unknown error')
                self.logger.warning(f"Failed to get price for {token_id}: {error_msg}")
                raise Exception(f"Failed to get price for {token_id}: {error_msg}")
        except Exception as e:
            self.logger.error(f"Error getting price for {token_id}: {str(e)}")
            raise
