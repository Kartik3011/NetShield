from openai import OpenAI
import streamlit as st

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=st.secrets["NVIDIA_API_KEY"],
    timeout=1000
)

def validator(transcribed_text, user_content):

    prompt = (
        "You are an AI tasked with analyzing and evaluating content alignment and relevance. Below are summaries of a YouTube video transcription and a contextual news article. "
        "Your tasks are:\n"
        "1. Compare the two summaries and identify key similarities, differences, and discrepancies.\n"
        "2. Assess the overall accuracy of the YouTube video summary based on the news article summary.\n"
        "3. **CRITICAL: Evaluate if the topic of the content is highly factual or technical** (e.g., 'Air Quality Index', 'Legal Proceedings', 'Financial News') **and contains significant religious or devotional content**. If such a mismatch exists, it indicates **content abuse or misleading tagging**, and the status should be **RED** regardless of factual accuracy.\n"
        "4. Provide your evaluation as one of the following:\n"
        "   - **Green**: The video content's main arguments and facts are generally accurate and supported by the news context, allowing for minor factual differences.\n"
        "   - **Yellow**: The validation is inconclusive because there is insufficient news context, or the summaries are highly vague, making definite verification impossible.\n"
        "   - **Red**: The video contains outright, severe factual contradictions, demonstrable misinformation, **OR exhibits content abuse/misleading tags** (e.g., devotional content in a factual report).\n"
        "Only respond with Green, Yellow, or Red, without any explanation..\n\n"
        "Here are the inputs:\n\n"
        f"YouTube Video Summary:\n\"{transcribed_text}\"\n\n"
        f"News Article Summary:\n\"{user_content}\""
    )

    try:
        completion = client.chat.completions.create(
            model="meta/llama-3.1-8b-instruct",  # ✅ FIXED MODEL
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            top_p=1,
            max_tokens=50,   # no need 1024 for 1 word
            stream=True
        )

        stt = ""

        for chunk in completion:

            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta

            if not delta:
                continue

            if hasattr(delta, "content") and delta.content:
                stt += delta.content

        return stt.strip()

    except Exception as e:
        return f"Error: {e}"
