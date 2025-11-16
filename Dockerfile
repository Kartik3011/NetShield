# 1. Base Image: Use an official Python image
FROM python:3.11-slim

# 2. Environment Variables: Set the port Streamlit will use
ENV PORT 8501
EXPOSE 8501

# 3. System Dependencies (CRITICAL: Installs FFmpeg and yt-dlp)
# We use apt-get to install system packages on the Debian-based image
RUN apt-get update && apt-get install -y \
    ffmpeg \
    # yt-dlp is often a system package or included in your requirements.txt
    # We install dependencies for yt-dlp here if it's needed as a system binary
    # If yt-dlp is only in requirements.txt, ensure it's the right version.
    # For robust deployment, ensure both are available.
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 4. Set working directory
WORKDIR /app

# 5. Copy requirements and install Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy all other application code
COPY . .

# 7. Entrypoint: Command to run the Streamlit app
# This command tells Streamlit to run your main dashboard file
ENTRYPOINT ["streamlit", "run", "Dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
