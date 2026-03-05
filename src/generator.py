import logging
from typing import Dict, Any, Optional
from google import genai

COMPANY_NAME = "Ahmed Jet Support"
MODEL_NAME = "gemini-2.5-flash"

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def draft_quote_email(routing_decision: Dict[str, Any], client: genai.Client) -> Optional[str]:
    """Generates a professional email response based on the database routing decision."""
    if not routing_decision:
        logging.error("No routing decision provided to the generator.")
        return None

    prompt = f"""
    You are an expert AOG Desk Agent working for {COMPANY_NAME}.
    Your job is to draft a professional, polite, and concise email reply to a customer based on the inventory routing decision provided below.
    
    Inventory Routing Decision (JSON):
    {routing_decision}
    
    Instructions based on status:
    1. If status is 'success' and match_type is 'Direct Match': Offer the part, state the price, condition, location, and confirm the exact paperwork available.
    2. If status is 'success' and match_type is 'Alternate Match': Politely explain the original part is out of stock, but offer the fully approved alternate part. Include the interchangeability notes, price, and paperwork.
    3. If status is 'paperwork_error': Apologise and explain that while the physical part is in the warehouse, it currently lacks the valid certification required for release.
    4. If status is 'no_stock': Apologise and clearly state that both the requested part and its alternates are currently out of stock.
    
    Draft the email now. Do not include subject lines, just the email body. Sign off as "AOG Desk, {COMPANY_NAME}".
    """

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text
    
    except Exception as e:
        logging.error(f"Email generation failed. Details: {e}")
        return None
