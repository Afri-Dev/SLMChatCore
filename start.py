"""
Startup script for Render.com deployment
This ensures the server binds to the port immediately before loading heavy dependencies
"""
import os
import sys

def main():
    port = int(os.environ.get("PORT", 8000))
    
    # Set environment variables to suppress TensorFlow warnings and speed up import
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow info/warning logs
    os.environ['TRANSFORMERS_VERBOSITY'] = 'error'  # Suppress transformers warnings
    
    # Import uvicorn here (after env vars are set)
    import uvicorn
    
    # Start server - this binds to the port immediately
    uvicorn.run(
        "faq_api:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()
