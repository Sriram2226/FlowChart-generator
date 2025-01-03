import streamlit as st
import requests

# Backend API URLs
API_URL_RENDER = "http://127.0.0.1:8000/render-mermaid/"
API_URL_GENERATE = "http://127.0.0.1:8000/generate-mermaid/"

# Streamlit App
st.title("Mermaid.js Diagram Renderer with AI")
st.write("Generate and Render Mermaid.js diagrams effortlessly.")

# Section: AI-Generated Mermaid.js Code
st.header("Generate Mermaid.js from Natural Language")
user_prompt = st.text_input("Describe your flowchart requirements:")
if st.button("Generate Mermaid.js Code"):
    with st.spinner("Generating Mermaid.js Code..."):
        try:
            response = requests.post(API_URL_GENERATE, data={"user_prompt": user_prompt})
            if response.status_code == 200:
                generated_code = response.json().get("mermaid_code", "")
                st.text_area("Generated Mermaid.js Code", value=generated_code, height=150)
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Section: Render and Download Mermaid.js Graph
st.header("Render Mermaid.js Diagram")
graph_definition = st.text_area(
    "Mermaid.js Graph Definition",
    "graph TD; A-->B; B-->C; C-->D;",
    height=200,
)
output_format = st.radio("Choose Output Format", ["png", "jpg"])

if st.button("Render Graph"):
    # Send graph definition to the FastAPI backend
    with st.spinner("Rendering graph..."):
        try:
            response = requests.post(
                API_URL_RENDER,
                data={"graph_definition": graph_definition, "format": output_format},
            )
            if response.status_code == 200:
                # Display download link for the image
                st.success("Graph rendered successfully!")
                st.markdown(
                    f"[Download Rendered Diagram](http://127.0.0.1:8000/render-mermaid/?format={output_format})"
                )
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
