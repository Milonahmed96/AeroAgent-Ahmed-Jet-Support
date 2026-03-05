import sqlite3
import logging
from contextlib import closing
from typing import Dict, Any, Optional, List

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def check_inventory(cursor: sqlite3.Cursor, part_number: str, conditions: List[str]) -> Optional[Dict[str, Any]]:
    """Queries the database for specific part availability and mandatory traceability."""
    if not conditions:
        logging.warning("No acceptable conditions provided for inventory check.")
        return None

    placeholders = ', '.join(['?'] * len(conditions))
    query = f'''
        SELECT Part_Number, Description, Condition, Quantity, Price_GBP, Location 
        FROM Inventory 
        WHERE Part_Number = ? AND Quantity > 0 AND Condition IN ({placeholders})
    '''
    cursor.execute(query, [part_number] + conditions)
    stock_match = cursor.fetchone()

    if stock_match:
        # Verify Traceability Documents
        cursor.execute('''
            SELECT Cert_Type, Trace_Source 
            FROM Trace_Documents 
            WHERE Part_Number = ? AND Condition = ?
        ''', (stock_match[0], stock_match[2]))
        trace_match = cursor.fetchone()

        if trace_match and "Invalid" not in trace_match[0]:
            return {
                "status": "success",
                "part_number": stock_match[0],
                "description": stock_match[1],
                "condition": stock_match[2],
                "price_gbp": stock_match[4],
                "location": stock_match[5],
                "certification": trace_match[0],
                "trace_source": trace_match[1]
            }
        else:
            return {
                "status": "paperwork_error", 
                "message": f"Part {part_number} is physically in stock but lacks valid release certification."
            }
    return None

def route_aog_request(db_path: str, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """Routes the AOG request through inventory, handling alternates and traceability constraints."""
    part_requested = extracted_data.get("part_number")
    conditions = extracted_data.get("acceptable_conditions", [])
    
    if not part_requested:
        return {"status": "error", "message": "No part number provided for routing."}
        
    with closing(sqlite3.connect(db_path)) as conn:
        cursor = conn.cursor()
        
        # Step A: Primary Part Check
        primary_result = check_inventory(cursor, part_requested, conditions)
        
        if primary_result and primary_result.get("status") == "success":
            primary_result["match_type"] = "Direct Match"
            return primary_result
            
        # Step B: Alternate Part Fallback
        cursor.execute('''
            SELECT Alternate_Part_Number, Approval_Notes 
            FROM Alternate_Parts 
            WHERE Primary_Part_Number = ?
        ''', (part_requested,))
        alt_match = cursor.fetchone()
        
        if alt_match:
            alt_pn, approval_notes = alt_match
            alt_result = check_inventory(cursor, alt_pn, conditions)
            
            if alt_result and alt_result.get("status") == "success":
                alt_result["match_type"] = "Alternate Match"
                alt_result["original_request"] = part_requested
                alt_result["interchangeability_notes"] = approval_notes
                return alt_result
                
        # Step C: Handle Failures
        if primary_result and primary_result.get("status") == "paperwork_error":
            return primary_result
            
        return {
            "status": "no_stock", 
            "message": f"Part {part_requested} and its approved alternates are completely out of stock."
        }
