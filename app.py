import streamlit as st
from google.genai import Client
from pypdf import PdfReader
import os
import time
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = Client(api_key=api_key, http_options={'api_version': 'v1alpha'})

def research_agent(pdf_text):
    # We define a list of models from "Best" to "Most Stable"
    model_options = ["gemini-3.1-flash-lite-preview", "gemini-3-flash-preview", "gemini-2.5-flash"]
    
    analysis_text = ""
    
    # Try each model until one works
    for model_id in model_options:
        try:
            # Task: Analysis
            res_prompt = f"Analyze this research paper and extract the core findings: {pdf_text[:15000]}"
            response = client.models.generate_content(model=model_id, contents=res_prompt)
            analysis_text = response.text
            
            # If we got here, it worked! Now do the formatting with the same successful model
            edit_prompt = f"Format this analysis clearly for a student with headers: {analysis_text}"
            final_response = client.models.generate_content(model=model_id, contents=edit_prompt)
            return final_response.text, model_id # Return the text and which model worked
            
        except Exception as e:
            if "503" in str(e):
                st.warning(f"Model {model_id} is busy. Trying fallback model...")
                time.sleep(1) # Short pause before trying the next model
                continue
            else:
                raise e # If it's a different error (like API key), stop here.

    raise Exception("All models are currently busy. Please try again in a few minutes.")

# 3. Streamlit Website UI
st.title("🔬 Research Agent 3.1 (Auto-Fallback)")
uploaded_file = st.file_uploader("Upload your Research PDF", type="pdf")

if uploaded_file:
    with st.spinner("Agents are negotiating with servers..."):
        reader = PdfReader(uploaded_file)
        full_text = "".join([p.extract_text() for p in reader.pages])
        
        try:
            summary, used_model = research_agent(full_text)
            st.info(f"Analysis generated using: {used_model}")
            st.markdown(summary)
            st.success("Done!")
        except Exception as e:
            st.error(f"Error: {e}")