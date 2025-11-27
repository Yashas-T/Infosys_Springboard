# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
# We list them here directly to avoid needing a separate requirements.txt file if it doesn't exist yet,
# but typically you'd COPY requirements.txt and RUN pip install -r requirements.txt
RUN pip install --no-cache-dir \
    torch \
    transformers \
    accelerate \
    streamlit \
    fastapi \
    uvicorn \
    pyngrok \
    python-dotenv \
    PyJWT \
    vaderSentiment \
    Pillow \
    pandas \
    matplotlib \
    requests \
    nest_asyncio \
    bitsandbytes \
    sentencepiece

# Create necessary directories if they don't exist (though COPY . does this, explicit creation ensures permissions)
RUN mkdir -p backend streamlit_app/avatars

# Expose ports for Streamlit and FastAPI
EXPOSE 8501
EXPOSE 8000

# Copy the start script and make it executable
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Set the entrypoint
ENTRYPOINT ["/start.sh"]
