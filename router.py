import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from schemas import RouteDecision, TechnicalBugReport, BillingInquiry

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

def route_ticket(ticket_text: str):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert support ticket router. Classify this ticket accurately."),
        ("human", "{ticket_text}")
    ])
    
    structured_llm = llm.with_structured_output(RouteDecision)
    return (prompt | structured_llm).invoke({"ticket_text": ticket_text})

def extract_tech_bug(ticket_text: str):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract all technical bug details from this ticket."),
        ("human", "{ticket_text}")
    ])
    
    structured_llm = llm.with_structured_output(TechnicalBugReport)
    return (prompt | structured_llm).invoke({"ticket_text": ticket_text})

def extract_billing(ticket_text: str):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract all billing and payment details from this ticket."),
        ("human", "{ticket_text}")
    ])
    
    structured_llm = llm.with_structured_output(BillingInquiry)
    return (prompt | structured_llm).invoke({"ticket_text": ticket_text})

def process_ticket(ticket_text: str):
    route = route_ticket(ticket_text)
    
    if route.category == "technical_bug":
        data = extract_tech_bug(ticket_text)
    elif route.category == "billing":
        data = extract_billing(ticket_text)
    else:
        data = {"message": "General inquiry routed to support"}

    return {
        "routing": route.model_dump(),
        "extracted_data": data.model_dump() if hasattr(data, "model_dump") else data
    }