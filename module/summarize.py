from openai import OpenAI
import streamlit as st

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = st.secrets["NVIDIA_API_KEY"] 
)
 
def sumup(a):
    # tell the model to ONLY summarize the content provided
    # and state if the text is short or irrelevant.
    con = """You are an advanced text summarization model. Your task is to provide a concise, factual summary of the input text provided below. 
CRITICAL RULE: The summary must strictly be based ONLY on the input text. If the input text is non-sensical, contains junk, or is too short (under 100 words), you must only return the phrase: 'IRRELEVANT_CONTENT_FLAGGED'.

SUMMARY REQUIRED:
""" + str(a)

    completion = client.chat.completions.create(
    model="mistralai/mistral-7b-instruct-v0.3",
    messages=[{"role":"user","content":con}],
    temperature=0.2,
    top_p=0.7,
    max_tokens=1024,
    stream=True
    )
    s=""

    for chunk in completion:
     if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
        s+=chunk.choices[0].delta.content
    return s