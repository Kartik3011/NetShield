from openai import OpenAI
import streamlit as st

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = st.secrets["NVIDIA_API_KEY"] 
)

def validator(transcribed_text,user_content):

    # Calc word counts for the inputs
    claim_word_count = len(transcribed_text.split())
    news_word_count = len(user_content.split())
    
    # minimum threshold for meaningful content
    MIN_CLAIM_WORDS = 5
    MIN_NEWS_WORDS = 15
    
    a=prompt = (
        "You are an AI tasked with analyzing and evaluating content alignment and relevance. Below are an **EXTRACTED FACTUAL CLAIM** from the video metadata and a **CONTEXTUAL NEWS ARTICLE SUMMARY**. Your tasks are:\n"
        "1. Compare the EXTRACTED CLAIM against the CONTEXTUAL NEWS ARTICLE SUMMARY.\n"
        "2. Identify if the video's claim is directly supported, contradicted, or generally consistent with the news summary.\n"
        "3. **CRITICAL DATA CHECK:** If the Video Claim has less than {MIN_CLAIM_WORDS} words OR the News Summary has less than {MIN_NEWS_WORDS} words, assign **YELLOW (Rule 4D)**.\n"
        "4. **CRITICAL POLICY OVERRIDE (Red Variance Introduced):** The following rules dictate a final status. Your response MUST include the reason for the Red or Yellow status, and must follow the format: 'STATUS (Reason)'.\n"
        "   - **Rule A (Contradiction/Inaccuracy):** If the claim contains **explicit, clear, and major** inaccuracies or contradictions to the news summary, assign **RED (Major Contradiction)**.\n"
        "   - **Rule B (Content Abuse):** If the claim is highly factual/technical **AND contains significant religious or devotional content**, assign **RED (Content Abuse/Misleading Tags)**.\n"
        "   - **Rule C (Sensitive/Unverifiable Risk):** If the claim is about a **highly sensitive topic** (e.g., specific political event, specific health claim, specific AQI number) **AND** the validation would otherwise result in YELLOW (i.e., the claim is uncontradicted but only generally related or unverifiable), **upgrade the status to RED (High Unverified Risk)**. This introduces necessary testing variance for high-impact content.\n"
        "   - **Rule D (Insufficient/Irrelevant Data):** Assign **YELLOW** if the inputs fail the data check in step 3 OR if the news summary is **completely irrelevant** to the core topic of the claim (e.g., searching for politics and finding a recipe).\n"
        "5. Provide your evaluation as one of the following:\n"
        "   - **Green (DEFAULT STATUS):** Assign **Green** if the claim **is not actively contradicted**, AND **is not assigned Yellow or Red by a Critical Rule**. If the content is generally related and not proven false, it must be Green. Response must be **Green (Thematic Match and Not Contradicted)**.\n"
        "   - **Yellow**: Assign **Yellow** ONLY if the claim violates Rule 4D (Insufficient/Irrelevant Data) and does not violate any RED rules. Response must be **Yellow (Reason from Rule 4D)**.\n"
        "   - **Red**: The claim violates Rule 4A, 4B, **or 4C**. Use the specific Red reason from the rule (e.g., Red (Major Contradiction) or Red (High Unverified Risk)).\n"
        "Only respond with the specified Status and Reason in the exact format 'STATUS (Reason)', without any additional explanation.\n\n"
        "Here are the inputs:\n\n"
        f"YouTube Video Claim (with Source Context):\n\"{transcribed_text}\"\n\n"
        f"News Article Summary:\n\"{user_content}\""
    )
    completion = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct-v0.3", 
         # meta/llama3-70b-instruct   very slow
        # mistralai/mistral-7b-instruct-v0.3
        # meta/llama3-8b-instruct
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