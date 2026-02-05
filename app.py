import streamlit as st
from src.core.planner import TravelPlanner
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Travel Agent", page_icon=":earth_asia:", layout="wide")
st.title("AI Travel Itinerary Planner")

st.write("Plan your day trip itinerary by entering your city and interests.")

with st.form("travel_form"):
    city = st.text_input("Enter the city for your trip")
    interests = st.text_input("Enter your interests for the trip(comma separated)")
    submit_button = st.form_submit_button("Generate Itinerary")

    if submit_button:
        if city and interests:
            planner = TravelPlanner()
            planner.set_city(city)
            planner.set_interests(interests)
            itinerary = planner.generate_itinerary()

            st.subheader("📄 Your Itinerary")
            st.markdown(itinerary)
        
        else:
            st.warning("Please enter a city and interests to generate an itinerary.")