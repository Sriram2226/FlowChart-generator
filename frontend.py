import streamlit as st
import requests

# Backend API URL
API_URL = "http://127.0.0.1:8000/render-mermaid/"

# Streamlit App
st.title("Mermaid.js Diagram Renderer")
st.write("Enter your Mermaid.js graph definition below:")

# Input Text Area
graph_definition = st.text_area(
    "Mermaid.js Graph Definition",
    "graph TD; A-->B; B-->C; C-->D;",
    height=200,
)

# Button to render graph
if st.button("Render Graph"):
    # Send graph definition to the FastAPI backend
    with st.spinner("Rendering graph..."):
        try:
            response = requests.post(
                API_URL,
                data={"graph_definition": graph_definition},
            )
            if response.status_code == 200:
                svg_content = response.json().get("svg", "")
                # Display the rendered SVG
                st.write("### Rendered Diagram")
                st.components.v1.html(svg_content, height=500, scrolling=True)
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
