"""
AeroAgent: End-to-End Pipeline Demonstration
This script demonstrates the modular capabilities of the AeroAgent system.
"""

from src import pipeline
from google.colab import userdata
import logging

def run_demo():
    logging.info("Initializing AeroAgent Professional Demo...")
    
    try:
        api_key = userdata.get('GEMINI_API_KEY')
    except Exception:
        print("❌ Error: Please ensure 'GEMINI_API_KEY' is set in Colab Secrets.")
        return

    # Sample AOG Scenario: Part is out of stock, but an alternate exists.
    aog_email = """
    URGENT REQUEST - AOG LONDON HEATHROW
    Aircraft: AHMED-98
    Required Part: VLV-1010 (Hydraulic Valve)
    Acceptable Conditions: OH (Overhauled) or SV (Serviceable)
    Required Certs: Dual Release EASA/FAA
    """

    print("\nINCOMING AOG EMAIL")
    print(aog_email)

    pipeline.run_aeroagent_pipeline(aog_email, api_key)

if __name__ == "__main__":
    run_demo()
