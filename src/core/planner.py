from langchain_core.messages import HumanMessage, AIMessage
from src.chains.itinerary_chain import generate_itinerary
from src.utils.logger import get_logger
from src.utils.custom_exception import CustomException

logger = get_logger(__name__)

class TravelPlanner:
    def __init__(self):
        self.messages = [] #It will store all the conversation history.
        self.city = ""
        self.interests = []
        self.itinerary = ""

        logger.info("TravelPlanner instance initialized")

    def set_city(self, city : str):
        try:
            self.city = city
            self.messages.append(HumanMessage(content=city))
            logger.info(f"City set successfully.")
        except Exception as e:
            logger.error(f"Error setting city: {e}")
            raise CustomException("failed to set city", e) 

    def set_interests(self, interests_str : str):
        try:
            self.interests = [i.strip() for i in interests_str.split(",")]
            self.messages.append(HumanMessage(content=str(self.interests)))
            logger.info(f"Interests set successfully.")
        except Exception as e:
            logger.error(f"Error setting interests: {e}")
            raise CustomException("failed to set interests", e)

    def generate_itinerary(self):
        try:
            logger.info(f"Generating itinerary for {self.city} with interests: {self.interests}")
            itinerary = generate_itinerary(self.city, self.interests)
            self.itinerary = itinerary
            self.messages.append(AIMessage(content=self.itinerary))
            logger.info(f"Itinerary generated successfully.")
            return self.itinerary
        except Exception as e:
            logger.error(f"Error generating itinerary: {e}")
            raise CustomException("failed to generate itinerary", e)
