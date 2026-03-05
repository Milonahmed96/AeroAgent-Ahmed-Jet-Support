import json
import logging
from typing import Optional, Dict, Any
from google import genai
from google.genai import types

MODEL_NAME = "gemini-2.5-flash"
COMPANY_NAME = "Ahmed Jet Support"

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def get_ai_client(api_key: str) -> Optional[genai.Client]:
    """Initializes the GenAI client using the provided API key."""
    if not api_key:
        logging.error("No API key provided.")
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        logging.error(f"Failed to initialize GenAI client: {e}")
        return None

def extract_aog_data(email_text: str, client: genai.Client) -> Optional[Dict[str, Any]]:
    """Extracts structured AOG parameters from unstructured email text."""
    prompt = f"""
    You are an expert aviation data extraction assistant working for {COMPANY_NAME}.
    Extract critical data from the following AOG request email.
    
    Return ONLY a valid JSON object using this exact schema. Use null for missing data.
    {{
      "aircraft_platform": "extracted aircraft type",
      "part_number": "extracted primary part number",
      "acceptable_conditions": ["condition 1", "condition 2"],
      "certification_required": "extracted certification requirements"
    }}

    Customer Email:
    {email_text}
    """

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    
    except json.JSONDecodeError:
        logging.error("The AI model returned invalid JSON.")
        return None
    except Exception as e:
        logging.error(f"API request failed. Details: {e}")
        return None
