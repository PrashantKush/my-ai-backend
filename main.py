import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load your API key from the .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ask-ai")
async def ask_ai(prompt: str):
    try:
        # 2. Call GPT-5.2
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a travel expert at MakeMyTrip. Provide concise, expert travel advice."},
                {"role": "user", "content": prompt}
            ],
        )
        
        # 3. Return the AI's answer
        return {"answer": response.choices[0].message.content}
    
    except Exception as e:
        return {"answer": f"Error calling AI: {str(e)}"}

@app.get("/")
def home():
    return {"status": "AI Backend is Live"}