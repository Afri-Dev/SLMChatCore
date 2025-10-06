# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY faq_bot.py .
COPY Mental_Health_FAQ.csv .
COPY processed_faq.csv .

# Copy model files if they exist
COPY faq_model/ ./faq_model/

# Pre-download the sentence-transformers model at build time
# This speeds up startup and ensures the model is available
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

# Download NLTK data (punkt tokenizer and stopwords)
RUN python -c "import nltk; nltk.download('punkt', download_dir='/usr/local/nltk_data'); nltk.download('stopwords', download_dir='/usr/local/nltk_data')"

# Set NLTK data path
ENV NLTK_DATA=/usr/local/nltk_data

# Expose port 7860 (Hugging Face Spaces default)
EXPOSE 7860

# Set environment variables
ENV PORT=7860
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]