from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from src.config.config import (
    RAG_MODEL, 
    OLLAMA_BASE_URL, 
    GROQ_API_KEY, 
    OLLAMA_MODEL,
    GROQ_MODEL,
    USE_OLLAMA
)

# Initialize LLM based on configuration
if USE_OLLAMA:
    llm = ChatOllama(
        model=OLLAMA_MODEL, 
        base_url=OLLAMA_BASE_URL, 
        temperature=0.2
    )
else:
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=0.2
    )

# Create the itinerary prompt template
itinerary_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful travel assistant. Create a day trip itinerary for {city} based on user's interests: {interests}. Provide a brief, bulleted itinerary."),
    ("human", "Create an itinerary for my day trip")
])

# Create the chain
itinerary_chain = itinerary_prompt | llm

def generate_itinerary(city: str, interests: list[str]) -> str:
    """
    Generate a travel itinerary based on city and interests.
    
    Args:
        city: The destination city
        interests: List of user interests
        
    Returns:
        Generated itinerary as a string
    """
    response = itinerary_chain.invoke({
        "city": city, 
        "interests": ', '.join(interests)
    })
    return response.content
