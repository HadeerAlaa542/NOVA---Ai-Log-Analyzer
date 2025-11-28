import re
import os
from typing import List
import json
from google import genai  
from dotenv import load_dotenv

load_dotenv()  # reads .env automatically

# === Gemini API client setup ===
API_KEY = os.getenv("GEMINI_API_KEY")  # your Gemini API key from AI Studio
client = genai.Client(api_key=API_KEY)

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

MAX_CHARS_PER_CHUNK = 4000
MAX_OUTPUT_TOKENS = 800  # adjust if needed

# === Utilities ===
def clean_log(text: str) -> str:
    text = re.sub(r'\x00|\x1b\[.*?m', '', text)
    text = re.sub(r'\r\n', '\n', text)
    return text.strip()

def chunk_text(text: str, max_chars: int = MAX_CHARS_PER_CHUNK) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        chunk = text[start:end]
        if end < len(text):
            last_nl = chunk.rfind('\n')
            if last_nl > 200:
                chunk = chunk[:last_nl]
                end = start + len(chunk)
        chunks.append(chunk)
        start = end
    return chunks

def build_prompt(log_chunk: str, context: str = "") -> str:
    return f"""
You are a skilled DevOps assistant. Analyze the following logs and produce JSON with keys:
- summary: one-sentence summary
- issues: list of {{error, count, example_line}}
- root_causes: short list of likely root causes
- remediation: short actionable remediation steps (3-6)
- commands: short shell/grep commands to locate similar logs

Context: {context}

Log:


Return ONLY valid JSON.
"""

# === Gemini call ===
def call_gemini(prompt: str, model: str = DEFAULT_MODEL, max_output_tokens: int = MAX_OUTPUT_TOKENS) -> str:
    """
    Call Gemini via google-genai SDK and return the response text.
    """
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "max_output_tokens": max_output_tokens,
            "temperature": 0.1,
        },
    )
    # response.text() works in recent SDK
    try:
        return response.text
    except Exception:
        # fallback
        try:
            return response.generations[0].text
        except Exception:
            return str(response)

# === Main analyzer ===
def analyze_log_text(text: str, context: str = "") -> dict:
    text = clean_log(text)
    chunks = chunk_text(text)
    raw_responses = []

    for chunk in chunks:
        prompt = build_prompt(chunk, context)
        out_text = call_gemini(prompt)
        raw_responses.append(out_text)

    # Try to parse the first chunk as JSON
    try:
        parsed = json.loads(raw_responses[0])
        parsed["_meta"] = {"chunks_processed": len(chunks)}
        return parsed
    except Exception:
        return {
            "note": f"{len(chunks)} chunk(s) processed",
            "raw_responses": raw_responses
        }

# === Chat with Nova ===
def chat_with_nova(message: str) -> str:
    prompt = f"""
You are Nova, a friendly and highly skilled AI DevOps Assistant. 
You are helpful, concise, and knowledgeable about system administration, logs, and debugging.
Answer the user's question directly.

User: {message}
Nova:
"""
    return call_gemini(prompt, max_output_tokens=300)
