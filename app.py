import streamlit as st
from src import extractor, router, generator, database

st.set_page_config(page_title="AeroAgent Dashboard", layout="wide")
DB_PATH = 'data/processed/aeroagent_web.db'

st.title("✈️ AeroAgent: AOG Quoting Engine")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Gemini API Key", type="password")

email_input = st.text_area("Paste AOG Email Here", height=200)

if st.button("Process Request"):
    if not api_key:
        st.error("Please enter an API Key.")
    elif not email_input:
        st.error("Email input is empty.")
    else:
        with st.spinner("Processing..."):
            client = extractor.get_ai_client(api_key)
            extracted = extractor.extract_aog_data(email_input, client)
            
            # --- FIX: Check if extraction was successful ---
            if extracted is None:
                st.error("🤖 The AI could not identify a Part Number in that email. Please check the text and try again.")
            else:
                decision = router.route_aog_request(DB_PATH, extracted)
                email_draft = generator.draft_quote_email(decision, client)
                
                st.subheader("Final Quote")
                st.text_area("Draft", value=email_draft, height=200)
                st.success("Pipeline Complete!")
