#!/usr/bin/env python3
"""
Script to apply database migration for XRP LP Rebalancer
"""

import os
import sys
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_database_connection():
    return psycopg2.connect(
        dbname=os.getenv('PGDATABASE', 'xrp'),
        user=os.getenv('PGUSER'),
        password=os.getenv('PGPASSWORD'),
        host=os.getenv('PGHOST'),
        port=os.getenv('PGPORT')
    )

def apply_migration(migration_file='01_create_tables.sql'):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    migration_path = os.path.join(script_dir, migration_file)
    
    # Read the migration SQL
    with open(migration_path, 'r') as f:
        migration_sql = f.read()
    
    # Connect to database and execute the migration
    conn = get_database_connection()
    cursor = conn.cursor()
    
    try:
        print(f"Applying migration from {migration_file}...")
        cursor.execute(migration_sql)
        conn.commit()
        print("Migration applied successfully!")
    except Exception as e:
        conn.rollback()
        print(f"Error applying migration: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Check if a specific migration file was provided
    migration_file = sys.argv[1] if len(sys.argv) > 1 else '01_create_tables.sql'
    apply_migration(migration_file)
