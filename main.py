import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
from supabase import create_client as create_supabase_client

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Supabase (optional – log trips when configured)
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = None
if supabase_url and supabase_key:
    supabase = create_supabase_client(supabase_url, supabase_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ask-ai")
async def ask_ai(
    prompt: str,
    user_name: str | None = Query(None, description="User's name"),
    user_email: str | None = Query(None, description="User's email"),
):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a travel expert at MakeMyTrip. Provide concise, expert travel advice."},
                {"role": "user", "content": prompt}
            ],
        )
        answer = response.choices[0].message.content

        # Log to Supabase if configured and we have at least one user detail
        if supabase and (user_name or user_email):
            try:
                supabase.table("trip_logs").insert({
                    "user_name": user_name or None,
                    "user_email": user_email or None,
                    "query": prompt,
                    "response": answer,
                }).execute()
            except Exception as log_err:
                # Don't fail the request if logging fails
                print(f"Supabase log error: {log_err}")

        return {"answer": answer}
    except Exception as e:
        return {"answer": f"Error calling AI: {str(e)}"}

@app.get("/")
def home():
    return {"status": "AI Backend is Live"}