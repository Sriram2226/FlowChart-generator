from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import JSONResponse
import subprocess
import tempfile
import os

app = FastAPI()

@app.post("/render-mermaid/")
async def render_mermaid(graph_definition: str = Form(...)):
    """
    Accepts Mermaid.js graph definitions, processes them using the Mermaid CLI, and returns the rendered SVG.
    """
    try:
        # Create a temporary file for the Mermaid graph definition
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mmd") as temp_file:
            temp_file.write(graph_definition.encode())
            temp_file_path = temp_file.name

        # Create another temporary file to store the SVG output
        svg_file_path = temp_file_path.replace(".mmd", ".svg")

        # Use the Mermaid CLI to render the SVG
        command = ["mmdc", "-i", temp_file_path, "-o", svg_file_path]
        subprocess.run(command, check=True)

        # Read the SVG content
        with open(svg_file_path, "r") as svg_file:
            svg_content = svg_file.read()

        # Cleanup temporary files
        os.remove(temp_file_path)
        os.remove(svg_file_path)

        # Return the SVG content
        return JSONResponse(content={"svg": svg_content}, status_code=200)

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error rendering graph: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
