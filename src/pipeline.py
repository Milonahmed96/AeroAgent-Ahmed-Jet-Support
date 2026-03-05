import logging
import json
from src import database, extractor, router, generator

# Configuration
DB_PATH = 'data/processed/aeroagent.db'
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def run_aeroagent_pipeline(email_text: str, api_key: str):
    """Orchestrates the full AOG processing flow."""
    
    # 1. Initialize Database
    database.initialize_database()
    
    # 2. Initialize AI Client
    client = extractor.get_ai_client(api_key)
    if not client:
        return
    
    # 3. Extraction
    logging.info("Starting Phase 1: AI Extraction...")
    extracted_data = extractor.extract_aog_data(email_text, client)
    if not extracted_data:
        logging.error("Pipeline failed at Extraction phase.")
        return
    
    # 4. Routing
    logging.info("Starting Phase 2: Inventory Routing...")
    routing_decision = router.route_aog_request(DB_PATH, extracted_data)
    
    # 5. Generation
    logging.info("Starting Phase 3: Generative Quoting...")
    final_email = generator.draft_quote_email(routing_decision, client)
    
    # Output Results
    print("\n" + "="*50)
    print("AEROAGENT PIPELINE COMPLETE")
    print("="*50)
    print(f"\n[AI EXTRACTED DATA]:\n{json.dumps(extracted_data, indent=4)}")
    print(f"\n[ROUTING DECISION]:\n{json.dumps(routing_decision, indent=4)}")
    print(f"\n[FINAL EMAIL DRAFT]:\n\n{final_email}")
    print("="*50)

if __name__ == "__main__":
    # This block allows for testing the pipeline directly
    import os
    from google.colab import userdata
    
    # Attempt to get key from Colab secrets for the test run
    try:
        API_KEY = userdata.get('GEMINI_API_KEY')
        
        SAMPLE_EMAIL = """
        URGENT AOG HEATHROW! 
        Our AHMED-98 is grounded. The main hydraulic valve has sheared.
        We urgently need replacement p/n VLV-1010. 
        We can accept SV or OH condition. Must have Dual Release EASA/FAA certs.
        """
        
        run_aeroagent_pipeline(SAMPLE_EMAIL, API_KEY)
    except Exception as e:
        logging.error("To run a test, ensure 'GEMINI_API_KEY' is in Colab Secrets.")
