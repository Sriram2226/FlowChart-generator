from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import JSONResponse
import subprocess
import tempfile
import os
from transformers import pipeline

app = FastAPI()

# Load the NLP model (e.g., Hugging Face pipeline)
flowchart_generator = pipeline("text2text-generation", model="openai/gpt-3.5-turbo")  # Replace with your model

@app.post("/generate-flowchart/")
async def generate_flowchart(prompt: str = Form(...)):
    """
    Accepts a natural language prompt and generates a Mermaid.js graph definition.
    """
    try:
        # Generate graph definition from prompt
        result = flowchart_generator(prompt, max_length=100)
        graph_definition = result[0]['generated_text']

        return JSONResponse(content={"graph_definition": graph_definition}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
