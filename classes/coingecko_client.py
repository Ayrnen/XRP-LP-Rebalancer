import requests

class CoinGeckoClient:
    def __init__(self):
        self.url = 'https://api.coingecko.com/api/v3/simple/price'
    
    def get_token_value_usd(self, token_id):
        params = {
            'ids': token_id,
            'vs_currencies': 'usd'
        }
        response = requests.get(self.url, params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        return float(data[token_id]['usd'])