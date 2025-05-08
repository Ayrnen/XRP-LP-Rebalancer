import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DatabaseManager:
    def __init__(self, db_name='xrp'):
        # Get connection details from environment variables
        self.db_name = db_name
        self.user = os.getenv('PGUSER')
        self.password = os.getenv('PGPASSWORD')
        self.host = os.getenv('PGHOST')
        self.port = os.getenv('PGPORT')
        self.conn = None
    
    def get_connection(self):
        if self.conn is None:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
        return self.conn
    
    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def initialize_db(self):
        """
        Initialize the database by running the migration script.
        This assumes the tables have been created using the SQL migration script.
        """
        pass  # Tables should be created using the SQL migration script

    """
    Insert statements
    """
    def create_snapshot(self, snapshot_type):
        from datetime import datetime as dt
        
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO snapshots (timestamp, snapshot_type) VALUES (%s, %s) RETURNING id",
            (dt.now(), snapshot_type)
        )
        snapshot_id = cursor.fetchone()[0]
        conn.commit()
        return snapshot_id
    
    def insert_price_data(self, snapshot_id, token_id, token_symbol, usd_price):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO price_data 
            (snapshot_id, token_id, token_symbol, usd_price) 
            VALUES (%s, %s, %s, %s)
            """,
            (snapshot_id, token_id, token_symbol, usd_price)
        )
        conn.commit()

    def insert_amm_data(self, snapshot_id, amm_details):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO amm_data 
            (snapshot_id, lp_token, lp_issuer, lp_token_amount, 
            asset1, asset2, asset1_issuer, asset2_issuer, 
            asset1_amount, asset2_amount, asset1_frozen, asset2_frozen) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                snapshot_id, 
                amm_details['lp_token'], 
                amm_details['lp_issuer'],
                amm_details['lp_token_amount'],
                amm_details['asset1'],
                amm_details['asset2'],
                amm_details.get('asset1_issuer'),
                amm_details['asset2_issuer'],
                amm_details['asset1_amount'],
                amm_details['asset2_amount'],
                amm_details.get('asset1_frozen', False),
                amm_details.get('asset2_frozen', False)
            )
        )
        conn.commit()

    def insert_balance_data(self, snapshot_id, address, token_type, token_issuer, balance, usd_value=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO balance_data 
            (snapshot_id, address, token_type, token_issuer, balance, usd_value) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (snapshot_id, address, token_type, token_issuer, balance, usd_value)
        )
        conn.commit()

    def insert_lp_position_data(self, snapshot_id, address, lp_token, lp_issuer, lp_token_amount, 
                            ownership_percentage, asset1_amount, asset2_amount, total_usd_value=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO lp_position_data 
            (snapshot_id, address, lp_token, lp_issuer, lp_token_amount, 
            ownership_percentage, asset1_amount, asset2_amount, total_usd_value) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                snapshot_id,
                address,
                lp_token,
                lp_issuer,
                lp_token_amount,
                ownership_percentage,
                asset1_amount,
                asset2_amount,
                total_usd_value
            )
        )
        conn.commit()
