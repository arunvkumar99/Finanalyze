import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader

# Define categories for the Indian context
categories = {
    # ... (as provided in the earlier messages) ...
}

def categorize_transaction(description):
    for cat, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in description.lower():
                return cat
    return 'Miscellaneous'

def extract_text_from_pdf(pdf_file):
    # Initialize a PDF reader object
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        # Extract text from each page
        text += page.extract_text()
    return text

def analyze_data(data):
    # Categorize transactions
    data['Category'] = data['Description'].apply(categorize_transaction)
    
    # ... (rest of the analysis as provided previously) ...

def main():
    st.title("Financial Data Analyzer")

    # Allow multiple file uploads
    uploaded_files = st.file_uploader("Upload your financial data (Excel/PDF)", type=["xlsx", "pdf"], accept_multiple_files=True)
    
    data_frames = []

    if uploaded_files:
        for uploaded_file in uploaded_files:
            if ".xlsx" in uploaded_file.name:
                df = pd.read_excel(uploaded_file)
                data_frames.append(df)
            elif ".pdf" in uploaded_file.name:
                text_data = extract_text_from_pdf(uploaded_file)
                # Use the file name as a unique key for each text_area
                st.text_area(f"Extracted PDF Data: {uploaded_file.name}", text_data, key=uploaded_file.name)
        
        if data_frames:
            consolidated_data = pd.concat(data_frames, ignore_index=True)
            analyze_data(consolidated_data)

if __name__ == "__main__":
    main()
