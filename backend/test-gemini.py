import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env")

print(f"✅ API Key Loaded: {api_key[:10]}...")

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
      model="gemini-flash-latest",
    google_api_key=api_key,
    temperature=0,
)

# Test prompt
response = llm.invoke([
    HumanMessage(
        content="""
Extract structured information.

Input:
I stitch school uniforms and do block printing on fabric.

Return:
- Skill Name
- Category
- Sellable Products
"""
    )
])

print("\n==============================")
print("Gemini Response")
print("==============================")
print(response.content)