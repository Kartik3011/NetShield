# 1. Base Image: Use an official Python image
FROM python:3.11-slim

# 2. Environment Variables: Set the port Streamlit will use
ENV PORT 8501
EXPOSE 8501

# 3. System Dependencies (CRITICAL: Installs FFmpeg)
# ffmpeg is a system binary required by yt-dlp, so it must be installed via apt.
RUN apt-get update && apt-get install -y ffmpeg \
    # The clean command should be separate for robustness
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 4. Set working directory
WORKDIR /app

# 5. Copy requirements and install Python libraries
# yt-dlp is installed here via requirements.txt, and ffmpeg is already installed above.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy all other application code
COPY . .

# 7. Entrypoint: Command to run the Streamlit app
ENTRYPOINT ["streamlit", "run", "Dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]