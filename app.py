import streamlit as st
from router import process_ticket

st.set_page_config(page_title="Structured Router Agent", layout="wide")

st.title("🛡️ Structured Output & Router Agent")
st.markdown("This agent converts unstructured customer tickets into strictly validated JSON. No hallucinations.")

examples = {
    "Select an example...": "",
    "Furious Billing Dispute": "I AM FURIOUS! My account ID US-7823 was charged $149 yesterday for a subscription I cancelled 3 weeks ago. Refund this immediately or I will chargeback.",
    "Technical Bug Report": "Hey whenever I try to export a PDF on my Mac the app crashes instantly. I get error code ERR_PDF_004. I click File > Export and it dies immediately.",
    "General Question": "Hi do you offer HIPAA compliant plans for enterprise customers?"
}

selected = st.selectbox("Test with an example:", list(examples.keys()))
default_text = examples[selected]

ticket = st.text_area("Customer Ticket Text:", value=default_text, height=120)

if st.button("🚀 Process Ticket", type="primary"):
    with st.spinner("Routing and validating output..."):
        result = process_ticket(ticket)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("1. Router Decision")
            st.markdown(f"**Category:** `{result['routing']['category']}`")
            st.markdown(f"**Urgency:** `{result['routing']['urgency']}`")
            st.info(result['routing']['reasoning'])
            st.json(result['routing'])

        with col2:
            st.subheader("2. Validated Structured Data")
            st.json(result['extracted_data'])