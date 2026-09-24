import streamlit as st
from langchain_groq import ChatGroq

st.set_page_config(page_title= 'My AI Chat', layout='centered')

st.title("THE GROQ CHATBOT")
st.write('A fully integrated, memory-enabled AI assistant.')

#the Sidebar
with st.sidebar:
  st.header('Configuration')
  user_api_key= st.text_input('Enter the Groq API key:', type='password')
  st.info('Your key is required to wake up the AI Brain')

#2.-------the memory vault------
if 'messages' not in st.session_state:
  st.session_state.messages = []

#3.-------display history-------
for msg in st.session_state.messages:
  with st.chat_message(msg['role']):
    st.markdown(msg['content'])

#4.------chat input and logic 
if user_query := st.chat_input('Say something to the AI...'):
  if not user_api_key:
    st.error('Please enter your API key in the sidebar first!')
  else:
    with st.chat_message('user'):
      st.markdown(user_query)
    #store the user msg to the vault
    st.session_state.messages.append({'role':'user','content':user_query})

    #initialise the brain 
    llm = ChatGroq(
        model = 'openai/gpt-oss-20b',
        temperature = 0.7,
        api_key = user_api_key
    )
    with st.spinner('AI is thinking...'):
      response= llm.invoke(st.session_state.messages)
      bot_answer = response.content

    st.session_state.messages.append({'role':'assistant','content':bot_answer})
    with st.chat_message('assistant'):
      st.markdown(bot_answer)
