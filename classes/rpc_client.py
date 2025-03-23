from dotenv import load_dotenv
from config_reader import ConfigReader
import os



class Web3Client:
    def __init__(self):

        load_dotenv()
        self.api_key = os.getenv('API_KEY')

        self.config = ConfigReader()

        self.ws_url = self.config.get_value('rpc-links', 'mainnet_wss') + self.api_key
        self.ws_url = self.config.get_value('rpc-links', 'mainnet_https') + self.api_key

        # self.web3 = Web3(Web3.HTTPProvider(self.http_url))
        # if not self.web3.is_connected():
        #     raise ConnectionError('Failed to connect to Web3 provider')