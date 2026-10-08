import os 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"), temperature=0.5)

class WaterIntakeAgent:
    def __init__(self):
        self.history = []

    def analyze_intake(self , intake_ml , goal_ml=2000):

        prompt = f"""
        you are a hydration assistant. The user has consumed {intake_ml} ml of water today.
        Their daily goal is {goal_ml} ml.
        Provide a hydration status and suggest if they need to drink more water. """

        response = llm.invoke([HumanMessage(content=prompt)])

        return response.text



if __name__ == "__main__":
    agent = WaterIntakeAgent()
    intake = 1500
    feedback = agent.analyze_intake(intake)
    print(f"Hydration Analysis: {feedback}")