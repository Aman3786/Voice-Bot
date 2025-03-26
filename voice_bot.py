def speech_to_text(client,stt_model,audio_value):
    transcript = client.audio.transcriptions.create(
        model=stt_model,
        file = audio_value,
        response_format = "text"
    )
    
    return transcript


def chat_completions(client,chat_model,transcript,prompt):
    response = client.chat.completions.create(
        model=chat_model,
        temperature=0.7,
        messages=[
            {
                "role":"system",
                "content":prompt
            },
            {
                "role":"user",
                "content":transcript
            }
        ]
    )
    response = response.choices[0].message.content
    return response


def text_to_speech(client,tts_model,voice,response):
    audio_output = client.audio.speech.create(
        model=tts_model,
        voice=voice,
        input=response
    )
    return audio_output