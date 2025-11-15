# Base image for Streamlit on Debian Linux (where the dependencies work best)
FROM python:3.11-slim-buster

# 1. Install System Dependencies: ffmpeg is critical for video processing.
# We use apt-get to install the media packages specified in your original packages.txt.
RUN apt-get update && apt-get install -y \
    ffmpeg \
    # The Python package manager (pip) will install yt-dlp itself later, 
    # but ffmpeg is the crucial system dependency.
    && rm -rf /var/lib/apt/lists/*

# 2. Set the working directory
WORKDIR /app

# 3. Copy your requirements file and install all Python libraries.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of your application code
COPY . .

# 5. Define the entry point to run Streamlit
ENTRYPOINT ["streamlit", "run", "Dashboard.py", "--server.port=80", "--server.address=0.0.0.0"]
