from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import FileResponse, JSONResponse
import subprocess
import tempfile
import os
from transformers import pipeline

app = FastAPI()

# Load an open-source LLM for generating Mermaid.js
llm_pipeline = pipeline("text2text-generation", model="t5-small")

@app.post("/generate-mermaid/")
async def generate_mermaid(user_prompt: str = Form(...)):
    """
    Uses an open-source LLM to generate a Mermaid.js graph definition from user input.
    """
    try:
        result = llm_pipeline(user_prompt, max_length=100)[0]["generated_text"]
        return JSONResponse(content={"mermaid_code": result}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating graph: {str(e)}")


@app.post("/render-mermaid/")
async def render_mermaid(graph_definition: str = Form(...), format: str = Form("png")):
    """
    Accepts Mermaid.js graph definitions, processes them using the Mermaid CLI, and returns a rendered image.
    """
    try:
        # Create a temporary file for the Mermaid graph definition
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mmd") as temp_file:
            temp_file.write(graph_definition.encode())
            temp_file_path = temp_file.name

        # Create another temporary file to store the output image
        image_file_path = temp_file_path.replace(".mmd", f".{format}")

        # Use the Mermaid CLI to render the image
        command = ["mmdc", "-i", temp_file_path, "-o", image_file_path, "-t", format]
        subprocess.run(command, check=True)

        # Cleanup the temporary Mermaid definition file
        os.remove(temp_file_path)

        # Return the rendered image file
        return FileResponse(image_file_path, media_type=f"image/{format}", filename=f"graph.{format}")

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error rendering graph: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
