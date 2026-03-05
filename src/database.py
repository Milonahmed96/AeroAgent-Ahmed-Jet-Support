import sqlite3
import os
import logging
from contextlib import closing

DB_PATH = 'data/processed/aeroagent.db'
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def initialize_database() -> None:
    """Creates tables and populates initial data for Ahmed Jet Support."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Inventory (
                Part_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Part_Number TEXT NOT NULL,
                Description TEXT NOT NULL,
                Aircraft_Platform TEXT NOT NULL,
                Condition TEXT NOT NULL,
                Quantity INTEGER NOT NULL,
                Price_GBP REAL NOT NULL,
                Location TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Alternate_Parts (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Primary_Part_Number TEXT NOT NULL,
                Alternate_Part_Number TEXT NOT NULL,
                Approval_Notes TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Trace_Documents (
                Document_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Part_Number TEXT NOT NULL,
                Condition TEXT NOT NULL,
                Cert_Type TEXT NOT NULL,
                Trace_Source TEXT NOT NULL
            )
        ''')

        cursor.execute('DELETE FROM Inventory')
        cursor.execute('DELETE FROM Alternate_Parts')
        cursor.execute('DELETE FROM Trace_Documents')

        inventory_data = [
            ('VLV-1010', 'Main Hydraulic Valve', 'AHMED-98', 'AR', 0, 4500.00, 'London Warehouse'),
            ('VLV-1010-MOD', 'Upgraded Hydraulic Valve', 'AHMED-98', 'OH', 3, 6200.00, 'London Warehouse'),
            ('APU-1998', 'Auxiliary Power Unit', 'LION-19', 'SV', 1, 125000.00, 'Bristol HQ'),
            ('RAD-88', 'Weather Radar Array', 'MIL-10', 'NE', 2, 28000.00, 'Bristol HQ'),
            ('BRK-10', 'Carbon Brake Assembly', 'AHMED-98', 'SV', 4, 11000.00, 'London Warehouse')
        ]
        cursor.executemany('''
            INSERT INTO Inventory (Part_Number, Description, Aircraft_Platform, Condition, Quantity, Price_GBP, Location)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', inventory_data)

        alternate_data = [
            ('VLV-1010', 'VLV-1010-MOD', 'Fully interchangeable per AHMED-98 IPC Rev 12'),
            ('RAD-88', 'RAD-88-B', 'Approved two-way interchangeability')
        ]
        cursor.executemany('''
            INSERT INTO Alternate_Parts (Primary_Part_Number, Alternate_Part_Number, Approval_Notes)
            VALUES (?, ?, ?)
        ''', alternate_data)

        trace_data = [
            ('VLV-1010-MOD', 'OH', 'Dual Release EASA Form 1 / FAA 8130-3', 'Lufthansa Technik'),
            ('APU-1998', 'SV', 'EASA Form 1', 'Rolls-Royce'),
            ('RAD-88', 'NE', 'OEM CofC', 'Honeywell'),
            ('BRK-10', 'SV', 'Invalid / Expired', 'Unknown Supplier')
        ]
        cursor.executemany('''
            INSERT INTO Trace_Documents (Part_Number, Condition, Cert_Type, Trace_Source)
            VALUES (?, ?, ?, ?)
        ''', trace_data)

        conn.commit()
        logging.info("Database initialized successfully at %s", DB_PATH)

if __name__ == '__main__':
    initialize_database()
