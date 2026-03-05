import streamlit as st
import json
from src import extractor, router, generator, database

# Page Configuration
st.set_page_config(page_title="AeroAgent | Ahmed Jet Support", page_icon="✈️", layout="wide")

# Initialize Database on Start
database.initialize_database()

# Sidebar
st.sidebar.title("✈️ AeroAgent Control")
st.sidebar.info("Autonomous AOG Quoting Engine for Ahmed Jet Support")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.sidebar.warning("Please enter your API Key to proceed.")

# Main UI
st.title("AOG Intelligence Dashboard")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Incoming Request")
    email_input = st.text_area("Paste the customer AOG email here:", height=300, 
                               placeholder="e.g., URGENT: Need VLV-1010 for AHMED-98...")
    
    process_btn = st.button("Process AOG Request", use_container_width=True)

with col2:
    st.subheader("Agent Analysis")
    
    if process_btn:
        if not api_key:
            st.error("API Key is missing!")
        elif not email_input:
            st.warning("Please paste an email first.")
        else:
            with st.spinner("Analyzing AOG requirements..."):
                # 1. Extraction
                client = extractor.get_ai_client(api_key)
                extracted = extractor.extract_aog_data(email_input, client)
                
                if extracted:
                    st.success("Data Extracted")
                    st.json(extracted)
                    
                    # 2. Routing
                    st.markdown("---")
                    st.subheader("🔍 Inventory Search")
                    decision = router.route_aog_request('data/processed/aeroagent.db', extracted)
                    
                    if decision['status'] == 'success':
                        st.write(f"**Match Found:** {decision['match_type']}")
                        st.info(f"Part: {decision['part_number']} | Location: {decision['location']}")
                    else:
                        st.error(f"No Stock: {decision['message']}")
                    
                    # 3. Generation
                    st.markdown("---")
                    st.subheader("Draft Response")
                    final_email = generator.draft_quote_email(decision, client)
                    st.text_area("Final Draft", value=final_email, height=250)
                else:
                    st.error("Failed to parse the email.")

# Footer
st.markdown("---")
st.caption("Developed by Milon Ahmed | Ahmed Jet Support AI Division")
