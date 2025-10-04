"""
Startup script for Render.com deployment
This ensures the server binds to the port immediately before loading heavy dependencies
"""
import os
import sys
import logging

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port {port}")
    
    # Set environment variables to suppress TensorFlow warnings and speed up import
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress all TensorFlow logs
    os.environ['TRANSFORMERS_VERBOSITY'] = 'error'  # Suppress transformers warnings
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'  # Avoid tokenizer warnings
    
    try:
        # Import uvicorn here (after env vars are set)
        logger.info("Importing uvicorn...")
        import uvicorn
        
        logger.info("Importing FastAPI app...")
        # Import the app directly to catch any import errors
        from faq_api import app
        
        logger.info(f"Starting uvicorn server on 0.0.0.0:{port}")
        
        # Start server with the app object directly
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
