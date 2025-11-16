# NetShield🛡️: AI-Powered Online Content Monitoring System

**NetShield**  represents a state of the art solution targeted at combating the spread of misinformation, fake news, and other types of harmful content across online platforms.

It uses a strong AI pipeline in order to automatically extract different content, translate non-English audio, fetch contextual news, and apply advanced Large Language Models (LLMs) to determine a clear authenticity status (Green, Yellow, or Red).

##  Core Features

* **AI-Powered Content Detection:** Uses advanced Natural Language Processing (NLP) and machine learning models to detect harmful content and fake news in real-time.
* **Advanced Video Verification:** Integrates the **YouTube Data API** to fetch video metrics and extracts audio streams using `yt-dlp` for transcription.
* **Content Validation Pipeline:** Automatically cross-checks video transcripts against summaries of related, trusted news articles scraped from sources like Google News.
* **LLM Driven Analysis:** Uses specialized LLMs for each step:
    * **Meta/Llama 3 70B** for final validation.
    * **Mistral 7B** for translation and summarization.
* **Multi Language Support:** Processes and translates non-English content for comprehensive global coverage.
* **Real Time Dashboard:** A Streamlit front-end provides an interface for requesting analysis, tracking reports, and managing accounts tagged as "Red" (misinformation).
* **AI Help Assistant:** Features an integrated, context-aware chatbot (powered by Groq and Llama ) to help users navigate features and understand the application's workflow.

## Technology Stack

| Category | Technology / Tool | Role in NetShield |
| :--- | :--- | :--- |
| **App Framework** | **Streamlit** | Interactive Web Dashboard and UI. |
| **LLM (Validation)** | **Meta/Llama 3 70B** | Final comparison logic (Green/Yellow/Red status). |
| **LLM (Processing)** | **Mistral 7B** | Content Summarization and Translation. |
| **LLM (ChatBot)** | **Groq / Llama** | Powers the NetShield AI Help Assistant.. |
| **Transcription** | **AssemblyAI** | Converts video audio streams into text. |
| **External Dependencies** | **`yt-dlp` and `FFmpeg`** | Downloads and converts YouTube audio streams to MP3. |
| **Data Scraping** | **`requests` and `BeautifulSoup`** | Fetches news articles from Google News. |

## Usage

1.  Navigate to the **Request Analysis** page in the sidebar.
2.  Enter a **hashtag** (e.g., `#liverdisease`) and a **City name** (e.g., `Delhi`).
3.  Click **Complete Analysis**.
4.  The system will process the data and redirect you to **Automate** page, displaying the final validation status for each video (Green, Yellow, or Red).
