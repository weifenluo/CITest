#!/usr/bin/env python3
"""
Test database connection from Windows runner to Linux container database.
"""

import os
import sys
import time
import psycopg2
from psycopg2 import OperationalError


def get_db_config():
    """Get database configuration from environment variables."""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 5432)),
        'database': os.getenv('DB_NAME', 'testdb'),
        'user': os.getenv('DB_USER', 'testuser'),
        'password': os.getenv('DB_PASSWORD', 'testpass123')
    }


def test_connection(max_retries=5, retry_delay=2):
    """
    Test connection to PostgreSQL database.
    
    Args:
        max_retries: Maximum number of connection attempts
        retry_delay: Delay in seconds between retries
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    config = get_db_config()
    
    print(f"Testing connection to PostgreSQL database...")
    print(f"Host: {config['host']}")
    print(f"Port: {config['port']}")
    print(f"Database: {config['database']}")
    print(f"User: {config['user']}")
    
    for attempt in range(1, max_retries + 1):
        try:
            print(f"\nConnection attempt {attempt}/{max_retries}...")
            
            # Attempt to connect
            conn = psycopg2.connect(**config)
            cursor = conn.cursor()
            
            # Execute a simple query
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
            print(f"✓ Connected successfully!")
            print(f"PostgreSQL version: {db_version[0]}")
            
            # Test creating a table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_table (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            print("✓ Created test table successfully!")
            
            # Test inserting data
            cursor.execute("""
                INSERT INTO test_table (name) VALUES (%s)
                RETURNING id, name, created_at;
            """, ('Test from Windows Runner',))
            row = cursor.fetchone()
            conn.commit()
            print(f"✓ Inserted test record: ID={row[0]}, Name={row[1]}, Created={row[2]}")
            
            # Test querying data
            cursor.execute("SELECT COUNT(*) FROM test_table;")
            count = cursor.fetchone()[0]
            print(f"✓ Query successful! Total records: {count}")
            
            # Clean up
            cursor.close()
            conn.close()
            print("\n" + "="*60)
            print("SUCCESS: All database tests passed!")
            print("="*60)
            return True
            
        except OperationalError as e:
            print(f"✗ Connection attempt {attempt} failed: {e}")
            if attempt < max_retries:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("\n" + "="*60)
                print("FAILED: Could not connect to database after all retries")
                print("="*60)
                return False
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            print("\n" + "="*60)
            print(f"FAILED: {type(e).__name__}: {e}")
            print("="*60)
            return False
    
    return False


if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)
