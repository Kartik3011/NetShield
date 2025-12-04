from openai import OpenAI
import streamlit as st

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = st.secrets["NVIDIA_API_KEY"] 
)
 
def sumup(a):
    # This remains the same, used for News Summary
    con = """You are an advanced text summarization model. Your task is to provide a concise, factual summary of the input text provided below. 
CRITICAL RULE: The summary must strictly be based ONLY on the input text. If the input text is non-sensical, contains junk, or is too short, simply provide the shortest possible summary or return the original text if it's the most relevant content. DO NOT flag short input as irrelevant.

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

#  NEW FUNCTION FOR  CLAIM EXTRACTION

def extract_claim(a):
    """Extracts a focused claim and evidence from sparse video metadata (Title/Description)."""
    con = """You are a forensic analyst. Your task is to analyze the sparse YouTube video metadata (Title and Description) provided below and extract the single, most critical factual claim and the evidence supporting it. 
    
    CRITICAL RULE:
    1. Output MUST start with 'Claim:'.
    2. Immediately after the extracted claim, you MUST insert a literal newline character ('\n').
    3. The next line MUST start with 'Evidence:'.
    4. Output MUST state the claim and the evidence presented (if any) based ONLY on the video title/description.
    5. Do NOT include channel details or subscriber counts.
    6. Do NOT summarize or generalize. Extract the single, most specific factual statement made.

    VIDEO METADATA:
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
        s+=chunk.choices[0].delta.content
    return s