from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings 

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    google_api_key=settings.GEMINI_API_KEY
)