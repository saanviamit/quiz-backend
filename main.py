from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
import base64
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load your API key correctly
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ------------------ QUESTION GENERATION ------------------

class QuestionRequest(BaseModel):
    topic: str
    language: str
    count: int

@app.post("/generate-questions")
def generate_questions(data: QuestionRequest):

    prompt = f"""
Generate {data.count} MCQ questions on "{data.topic}" in {data.language}.
Output format EXACT:

Q1) Question text?
a) option
b) option
c) option
d) option
Correct: a
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"raw": res.choices[0].message.content}

# ------------------ AI VOICE (TTS) ------------------

class TTSRequest(BaseModel):
    text: str
    voice: str = "verse"

@app.post("/tts")
def tts(data: TTSRequest):
    return {"audio": None}

