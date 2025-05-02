import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path='data/xrp_lp_data.db'):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)        
        self.db_path = db_path
        self.conn = None
        self.initialize_db()
    
    def get_connection(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def initialize_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Create snapshots table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                snapshot_type TEXT NOT NULL
            )
            """)
        
        # Create price_data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS price_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_id INTEGER NOT NULL,
                token_id TEXT NOT NULL,
                token_symbol TEXT NOT NULL,`
                usd_price REAL NOT NULL,
                FOREIGN KEY (snapshot_id) REFERENCES snapshots (id)
            )
        """)
        
        # Create amm_data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS amm_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_id INTEGER NOT NULL,
                lp_token TEXT NOT NULL,
                lp_issuer TEXT NOT NULL,
                lp_token_amount REAL NOT NULL,
                asset1 TEXT NOT NULL,
                asset2 TEXT NOT NULL,
                asset1_issuer TEXT,
                asset2_issuer TEXT NOT NULL,
                asset1_amount REAL NOT NULL,
                asset2_amount REAL NOT NULL,
                asset1_frozen BOOLEAN,
                asset2_frozen BOOLEAN,
                FOREIGN KEY (snapshot_id) REFERENCES snapshots (id)
            )
            """)
            
            # Create balance_data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS balance_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_id INTEGER NOT NULL,
                address TEXT NOT NULL,
                token_type TEXT NOT NULL,
                token_issuer TEXT,
                balance REAL NOT NULL,
                usd_value REAL,
                FOREIGN KEY (snapshot_id) REFERENCES snapshots (id)
            )
        """)
        
        # Create lp_position_data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lp_position_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_id INTEGER NOT NULL,
                address TEXT NOT NULL,
                lp_token TEXT NOT NULL,
                lp_issuer TEXT NOT NULL,
                lp_token_amount REAL NOT NULL,
                ownership_percentage REAL NOT NULL,
                asset1_amount REAL NOT NULL,
                asset2_amount REAL NOT NULL,
                total_usd_value REAL,
                FOREIGN KEY (snapshot_id) REFERENCES snapshots (id)
            )
        """)
        
        conn.commit()