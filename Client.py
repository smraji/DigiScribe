# Import necessary libraries

import streamlit as st
import os
from search_tree import get_icd_codes

# Set the webpage title
st.set_page_config(page_title="Welcome to DigiScribe MedChat!")
   
# Create a header element
st.header("Welcome to DigiScribe MedChat!")

os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

# Set the system prompt for the chatbot
system_prompt = st.text_area(
  label="System Prompt",
  value="You are a helpful AI assistant who can extract ICD-10 Codes from Clinical Notes.",
  key="system_prompt")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = [
         {"role": "assistant", "content": "Can you type the clinical case notes to get the ICD Codes?"}
    ]
         
if "current_response" not in st.session_state:
    st.session_state.current_response = ""
    
# Loop through each message in the session state and render it
for message in st.session_state.messages:
   with st.chat_message(message["role"]):
      st.markdown(message["content"])


# Take user input from the chat interface
if user_prompt := st.chat_input("Your message here", key="user_input"):
    # Add user input to session state
    st.session_state.messages.append(
         {"role": "user", "content": user_prompt}
    )

    # Pass user input to the LLM chain to generate a response
    #response = llm_chain.invoke({"question": user_prompt})   
    #print(response)
    icd_codes = get_icd_codes(user_prompt)
    icdcodes=''
    for s in icd_codes:
        icdcodes +=' , '+s

    # Add LLM response to session state
    st.session_state.messages.append({"role": "assistant", "content":icdcodes})        

    # Render LLM response in the chat interface
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        if len(icdcodes) <=1 :
            icdcodes='Sorry. I dont understand.Please refine your prompt to give a proper clinical note. Thanks'
            st.markdown(icdcodes)
        else :
            st.markdown(icdcodes)
    
