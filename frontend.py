import streamlit as st
import requests

# Backend API URLs
RENDER_API_URL = "http://127.0.0.1:8000/render-mermaid/"
GENERATE_API_URL = "http://127.0.0.1:8000/generate-flowchart/"

# Streamlit App
st.title("AI-Powered Flowchart Generator")
st.write("Enter a natural language prompt to generate a flowchart:")

# Input Text Area for Prompt
prompt = st.text_area(
    "Flowchart Description (Prompt)",
    "Describe your flowchart here, e.g., 'A starts the process, then goes to B, then splits into C and D.'",
    height=150,
)

# Button to generate graph definition
if st.button("Generate Flowchart"):
    with st.spinner("Generating flowchart..."):
        try:
            # Send the prompt to the backend
            generate_response = requests.post(
                GENERATE_API_URL,
                data={"prompt": prompt},
            )
            if generate_response.status_code == 200:
                graph_definition = generate_response.json().get("graph_definition", "")
                
                # Send the generated graph definition to the rendering API
                render_response = requests.post(
                    RENDER_API_URL,
                    data={"graph_definition": graph_definition},
                )
                if render_response.status_code == 200:
                    svg_content = render_response.json().get("svg", "")
                    # Display the rendered SVG
                    st.write("### Generated Flowchart")
                    st.components.v1.html(svg_content, height=500, scrolling=True)
                else:
                    st.error(f"Error rendering graph: {render_response.json().get('detail', 'Unknown error')}")
            else:
                st.error(f"Error generating graph: {generate_response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
