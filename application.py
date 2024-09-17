import google.generativeai as genai
import streamlit as st
from langchain import PromptTemplate, LLMChain
import google.generativeai as palm  # Google LLM API (Gemini Pro)

# Setup Gemini Pro API client
def setup_gemini():
    # Load API key from environment variable (or replace with your key directly)
    api_key = st.secrets["api_key"]
    palm.configure(api_key=api_key)

# Function to run LLM chain and generate response
def generate_response(action, user_input):
    # Define the prompt template
    prompt_template = PromptTemplate(
        input_variables=["action", "user_input"],
        template="""You are an AI that acts as a {action}. Based on the following input: {user_input}, provide a response."""
    )

    # Create the prompt from user input
    prompt = prompt_template.format(action=action, user_input=user_input)

    # Send prompt to Google's Gemini Pro API (or other model available)
    model=palm.GenerativeModel("gemini-pro")
    chat = model.start_chat(history=[])
    response=chat.send_message(prompt)
    return response.text


# Streamlit App
def main():
    st.title("Web App for Assisting Developers")

    # Input: User defines the AI's role
    action = st.text_input("What should I act as (e.g., developer, translator, assistant, etc.)?")

    # Input: User's query
    user_input = st.text_area("Enter your query or request:")

    # Button to generate the response
    if st.button("Generate Response"):
        if action and user_input:
            # Ensure Gemini Pro API is configured
            setup_gemini()

            # Get response from LLM
            response = generate_response(action, user_input)
            st.write("### Response")
            st.write(response)
        else:
            st.write("Please provide both the action and the input.")

if __name__ == "__main__":
    main()
