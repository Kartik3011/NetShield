from openai import OpenAI
import streamlit as st

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = st.secrets["NVIDIA_API_KEY"] 
)

def validator(transcribed_text,user_content):

    a=prompt = (
        "You are an AI tasked with analyzing and evaluating content alignment and relevance. Below are summaries of a YouTube video transcription and a contextual news article. "
        "Your tasks are:\n"
        "1. Compare the two summaries and identify key similarities, differences, and discrepancies.\n"
        "2. Assess the overall accuracy of the YouTube video summary based on the news article summary.\n"
        "3. **CRITICAL: Evaluate if the topic of the content is highly factual or technical** (e.g., 'Air Quality Index', 'Legal Proceedings', 'Financial News') **and contains significant religious or devotional content**. If such a mismatch exists, it indicates **content abuse or misleading tagging**, and the status should be **RED** regardless of factual accuracy.\n"
        "4. Provide your evaluation as one of the following:\n"
        "   - **Green**: The video content is highly accurate and aligns well with the news context.\n"
        "   - **Yellow**: The video is partially accurate, misses key points, or lacks sufficient news context for verification.\n"
        "   - **Red**: The video contains major inaccuracies, contradictions, **OR exhibits content abuse/misleading tags** (e.g., devotional content in a factual report).\n"
        "Only respond with Green, Yellow, or Red, without any explanation..\n\n"
        "Here are the inputs:\n\n"
        f"YouTube Video Summary:\n\"{transcribed_text}\"\n\n"
        f"News Article Summary:\n\"{user_content}\""
    )
    completion = client.chat.completions.create(
        model="meta/llama3-70b-instruct",
        messages=[{"role":"user","content":a}],
        temperature=0.5,
        top_p=1,
        max_tokens=1024,
        stream=True
    )
    stt=""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            
            print(chunk.choices[0].delta.content, end="")
            stt+=chunk.choices[0].delta.content

    return stt