import streamlit as st
from openai import OpenAI
from voice_bot import speech_to_text, chat_completions, text_to_speech
from prompts import prompt
import os
import time

st.set_page_config(
    page_title="Voice Bot",
    page_icon="🔊",
)
st.title('🔊 Voice Bot')
st.caption('Enjoy the Chat feature with the power of Voice!') 


open_api_key = st.sidebar.text_input(
    "Enter Your OpenAI API Key 🗝️",
    value=st.session_state.get('open_api_key', ''),
    help="Get your API key from https://platform.openai.com/api-keys",
    type='password'
)
os.environ["OPENAI_API_KEY"] = open_api_key
st.session_state['open_api_key'] = open_api_key

with st.sidebar.expander("⚙️ Bot Settings"):
    voice = st.selectbox(
        "Voice Options 🗣️",
        [
            "nova",
            "alloy",
            "onyx",
            "shimmer",
            "echo",
            "fable"
        ],
        help="Choose the voice. Test out the voices here: https://platform.openai.com/docs/guides/text-to-speech"
    )
    
    stt_model = st.selectbox(
        "Speech-To-Text Model 🤖",
        ["whisper-1"]
    )
    
    tts_model = st.selectbox(
        "Text-To-Speech Model 🤖",
        [
            "tts-1",
            "tts-1-hd",
            "gpt-4o-mini-tts"
        ]
    )
    
    chat_model = st.selectbox(
        "Chat Model 🤖",
        [
            "gpt-3.5-turbo",
            "gpt-4o"
        ]
    )
    
    
audio_value = st.audio_input("Speak..")

if audio_value:
    if open_api_key == '' or open_api_key is None:
        st.error("⚠️ Please enter your OpenAI API key in the sidebar")
    else:
        client = OpenAI(
            api_key=open_api_key
        )
        
        output_filename = f"output_{time.time()}.mp3"
        
        with st.spinner('Generating audio...'):
            
            transcript = speech_to_text(client=client, stt_model=stt_model, audio_value=audio_value)
            
            response = chat_completions(client=client, chat_model=chat_model, transcript=transcript, prompt=prompt)
            
            audio_output = text_to_speech(client=client, tts_model=tts_model, voice=voice, response=response)
            audio_output.write_to_file(output_filename)
            
        time.sleep(1)
            
        with open(output_filename, "rb") as audio_file:
            st.audio(audio_file, format='audio/mp3', autoplay=True)
            
        st.text_area("Bot Response Transcript:", response)