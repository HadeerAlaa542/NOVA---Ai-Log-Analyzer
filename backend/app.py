from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from analyzer import analyze_log_text, chat_with_nova

import os

app = FastAPI(title="AI Log Analyzer")

@app.post("/analyze")
async def analyze_file(
    file: UploadFile = File(...), 
    context: str = Form("")
):
    if not file:
        raise HTTPException(status_code=400, detail="Provide file upload")
    
    data = await file.read()
    text = data.decode(errors='replace')

    result = analyze_log_text(text, context)
    return JSONResponse(result)

@app.post("/chat")
async def chat(message: str = Form(...)):
    response = chat_with_nova(message)
    return JSONResponse({"response": response})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

