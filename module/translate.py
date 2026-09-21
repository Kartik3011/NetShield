import groq
import streamlit as st

client = groq.Groq(api_key=st.secrets["GROQ_API_KEY"])

def trans(a):
    con = """You are an advanced language model capable of understanding and translating multiple languages. 
    Your task is to translate the provided text into English. Do not provide context or explanations. 
    Only return the translated text, and ensure it is clear, accurate, and concise. 
    CRITICAL RULE: The translated text must be a minimal, high-relevance search query. You must:
    1. Translate the core topic.
    2. Remove all hashtags, channel names, irrelevant filler words (like 'Vlog', 'Shorts', 'Unboxing').
    3. The final output must be a single phrase containing a MAXIMUM of 8 words.

    just only translated text
    The text to translate is as follows:
    """ + str(a)
  
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":con}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024,
        stream=True
    )
    ss = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            ss += chunk.choices[0].delta.content
            
    return ss
