import streamlit as st
import requests

# Streamlit configuration
st.set_page_config(page_title="Flowchart Generator", layout="centered")

# Title and description
st.title("AI-Powered Flowchart Generator")
st.write("Enter a prompt, and the AI will generate a flowchart for you!")

# Input for user prompt
user_prompt = st.text_area("Enter your prompt:", placeholder="e.g., Create a flowchart for a login system")

# Submit button
if st.button("Generate Flowchart"):
    if not user_prompt.strip():
        st.error("Please enter a valid prompt.")
    else:
        # Backend API call
        try:
            # Replace with your backend API URL
            api_url = "http://localhost:8000/generate-flowchart"  # Update with actual backend URL
            response = requests.post(api_url, json={"prompt": user_prompt})
            
            if response.status_code == 200:
                mermaid_markdown = response.json().get("mermaid_markdown")
                
                if mermaid_markdown:
                    # Display Mermaid.js markdown
                    st.subheader("Generated Flowchart")
                    st.write("```mermaid")
                    st.write(mermaid_markdown)
                    st.write("```")
                    
                    # Render Mermaid.js using Streamlit Markdown
                    st.markdown(f"""
                        <div class="mermaid">
                        {mermaid_markdown}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("Failed to generate flowchart. Please try again.")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Add Mermaid.js support in Streamlit
mermaid_js = """
<script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ startOnLoad: true });
</script>
"""
st.markdown(mermaid_js, unsafe_allow_html=True)
