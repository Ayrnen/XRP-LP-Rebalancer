#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv
from datetime import datetime

# Import your existing classes
from classes.config_reader import ConfigReader
from classes.runtime_tracker import RuntimeTracker
from classes.rpc_client import RPCClient
from classes.address_client import AddressClient
from classes.amm_client import AMMClient
from classes.coinmarketcap_client import CoinMarketCapClient
from classes.database_manager import DatabaseManager

class DataCollector:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.config_reader = ConfigReader()
        self.runtime_tracker = RuntimeTracker()
        self.cmc_client = CoinMarketCapClient()
        
        # Load address from environment
        load_dotenv()
        self.address = os.getenv('ADDRESS')
        
        if not self.address:
            print("No address found in environment variables")
            raise ValueError("ADDRESS environment variable not set")
        
        self.address_client = AddressClient(self.address)
        self.amm_client = AMMClient()
    
    def collect_price_data(self):
        """Collect price data for tokens configured in config.ini"""
        try:
            print("Collecting price data")
            
            # Create a snapshot
            snapshot_id = self.db_manager.create_snapshot("price_data")
            
            # Get token IDs from config
            token_ids_section = "coinmarketcap-token-ids"
            token_ids = self.config_reader.get_section(token_ids_section)
            
            for token_symbol, token_id in token_ids.items():
                try:
                    price = self.cmc_client.get_token_value_usd(token_id)
                    
                    # Store in database
                    self.db_manager.insert_price_data(snapshot_id, token_id, token_symbol, price)
                    
                    print(f"Collected price for {token_symbol}: ${price}")
                except Exception as e:
                    print(f"Error collecting price for {token_symbol}: {str(e)}")
            
            print("Price data collection completed")
            
        except Exception as e:
            print(f"Error in price data collection: {str(e)}")
    
    def collect_amm_data(self):
        """Collect AMM data for pools configured in config.ini"""
        try:
            print("Collecting AMM data")
            
            # Create a snapshot
            snapshot_id = self.db_manager.create_snapshot("amm_data")
            
            # Get LP tokens and issuers from config
            lp_tokens = self.config_reader.get_section("mainnet-lp-tokens")
            lp_issuers = self.config_reader.get_section("mainnet-lp-issuers")
            token_addresses = self.config_reader.get_section("mainnet-token-addresses")
            
            for pair_name, lp_token in lp_tokens.items():
                try:
                    lp_issuer = lp_issuers[pair_name]
                    
                    # Parse pair name to get tokens
                    token1_name, token2_name = pair_name.split('_')
                    token1 = "XRP" if token1_name.upper() == "XRP" else token_addresses[token1_name]
                    token2 = "XRP" if token2_name.upper() == "XRP" else token_addresses[token2_name]
                    
                    # Get AMM details
                    amm_details = self.amm_client.get_amm_details(lp_issuer, token1, token2)
                    
                    # Store in database
                    self.db_manager.insert_amm_data(snapshot_id, amm_details)
                    
                    print(f"Collected AMM data for {pair_name}")
                except Exception as e:
                    print(f"Error collecting AMM data for {pair_name}: {str(e)}")
            
            print("AMM data collection completed")
            
        except Exception as e:
            print(f"Error in AMM data collection: {str(e)}")
    
    def collect_balance_data(self):
        """Collect balance data for the configured address"""
        try:
            print(f"Collecting balance data for address: {self.address}")
            
            # Create a snapshot
            snapshot_id = self.db_manager.create_snapshot("balance_data")
            
            # Get XRP balance
            xrp_balance = self.address_client.get_balance_xrp()
            
            # Get XRP price
            xrp_id = self.config_reader.get_value("coinmarketcap-token-ids", "xrp")
            xrp_price = self.cmc_client.get_token_value_usd(xrp_id)
            xrp_usd_value = xrp_balance * xrp_price
            
            # Store XRP balance
            self.db_manager.insert_balance_data(
                snapshot_id, 
                self.address, 
                "XRP", 
                None, 
                xrp_balance, 
                xrp_usd_value
            )
            
            print(f"Collected XRP balance: {xrp_balance} (${xrp_usd_value})")
            
            # Get token balances
            token_addresses = self.config_reader.get_section("mainnet-token-addresses")
            token_ids = self.config_reader.get_section("coinmarketcap-token-ids")
            
            for token_name, token_address in token_addresses.items():
                try:
                    # Skip tokens without proper address
                    if token_address == "???" or not token_address:
                        continue
                    
                    # Get token balance
                    token_balance, _ = self.address_client.get_balance_token(token_address)
                    
                    # Get token price if available
                    usd_value = None
                    if token_name in token_ids:
                        token_id = token_ids[token_name]
                        token_price = self.cmc_client.get_token_value_usd(token_id)
                        usd_value = float(token_balance) * token_price
                    
                    # Parse token issuer
                    token_issuer = None
                    if ":" in token_address:
                        _, token_issuer = token_address.split(":", 1)
                    
                    # Store token balance
                    self.db_manager.insert_balance_data(
                        snapshot_id, 
                        self.address, 
                        token_name, 
                        token_issuer, 
                        float(token_balance), 
                        usd_value
                    )
                    
                    print(f"Collected {token_name} balance: {token_balance}")
                except Exception as e:
                    print(f"Error collecting balance for {token_name}: {str(e)}")
            
            print("Balance data collection completed")
            
        except Exception as e:
            print(f"Error in balance data collection: {str(e)}")
    
    def collect_lp_position_data(self):
        """Collect LP position data for the configured address"""
        try:
            print(f"Collecting LP position data for address: {self.address}")
            
            # Create a snapshot
            snapshot_id = self.db_manager.create_snapshot("lp_position_data")
            
            # Get LP tokens and issuers from config
            lp_tokens = self.config_reader.get_section("mainnet-lp-tokens")
            lp_issuers = self.config_reader.get_section("mainnet-lp-issuers")
            token_addresses = self.config_reader.get_section("mainnet-token-addresses")
            token_ids = self.config_reader.get_section("coinmarketcap-token-ids")
            
            for pair_name, lp_token in lp_tokens.items():
                try:
                    lp_issuer = lp_issuers[pair_name]
                    
                    # Parse pair name to get tokens
                    token1_name, token2_name = pair_name.split('_')
                    token1 = "XRP" if token1_name.upper() == "XRP" else token_addresses[token1_name]
                    token2 = "XRP" if token2_name.upper() == "XRP" else token_addresses[token2_name]
                    
                    # Get LP balance
                    try:
                        lp_balance = self.address_client.get_lp_balance(lp_issuer, lp_token)
                    except Exception as e:
                        print(f"Error getting LP balance for {pair_name}: {str(e)}")
                        continue
                    
                    # Skip if no balance
                    if lp_balance <= 0:
                        print(f"No LP balance for {pair_name}, skipping")
                        continue
                    
                    # Get LP breakdown
                    breakdown = self.address_client.get_lp_breakdown(lp_token, lp_issuer, token1, token2)
                    
                    # Calculate USD value if possible
                    total_usd_value = None
                    try:
                        asset1_value = 0
                        asset2_value = 0
                        
                        # Get asset1 value
                        asset1_name = token1_name.lower()
                        asset1_amount = breakdown['assets'][asset1_name]['amount']
                        if asset1_name in token_ids:
                            token1_id = token_ids[asset1_name]
                            token1_price = self.cmc_client.get_token_value_usd(token1_id)
                            asset1_value = asset1_amount * token1_price
                        
                        # Get asset2 value
                        asset2_name = token2_name.lower()
                        asset2_amount = breakdown['assets'][asset2_name]['amount']
                        if asset2_name in token_ids:
                            token2_id = token_ids[asset2_name]
                            token2_price = self.cmc_client.get_token_value_usd(token2_id)
                            asset2_value = asset2_amount * token2_price
                        
                        total_usd_value = asset1_value + asset2_value
                    except Exception as e:
                        print(f"Could not calculate USD value for {pair_name}: {str(e)}")
                    
                    # Store LP position
                    self.db_manager.insert_lp_position_data(
                        snapshot_id,
                        self.address,
                        lp_token,
                        lp_issuer,
                        lp_balance,
                        breakdown['ownership_percentage'],
                        breakdown['assets'][token1_name.lower()]['amount'],
                        breakdown['assets'][token2_name.lower()]['amount'],
                        total_usd_value
                    )
                    
                    print(f"Collected LP position data for {pair_name}")
                except Exception as e:
                    print(f"Error collecting LP position for {pair_name}: {str(e)}")
            
            print("LP position data collection completed")
            
        except Exception as e:
            print(f"Error in LP position data collection: {str(e)}")
    
    def run_collection(self):
        """Run all data collection tasks"""
        try:
            print(f"Starting data collection run at {datetime.now()}")
            self.runtime_tracker.start()
            
            self.collect_price_data()
            self.collect_amm_data()
            self.collect_balance_data()
            self.collect_lp_position_data()
            
            self.runtime_tracker.stop()
            print("Data collection run completed successfully")
        except Exception as e:
            print(f"Error in data collection run: {str(e)}")
        finally:
            self.db_manager.close_connection()


if __name__ == "__main__":
    # Set up output redirection to log file
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"data_collection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    # Redirect stdout and stderr to the log file
    sys.stdout = open(log_file, 'w')
    sys.stderr = sys.stdout
    
    try:
        collector = DataCollector()
        collector.run_collection()
    except Exception as e:
        print(f"Fatal error in data collection: {str(e)}")
    finally:
        # Close the log file
        sys.stdout.close()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
