from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging
import os
from faq_bot import FAQBot
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Mental Health FAQ API",
    description="A REST API for mental health FAQ retrieval using sentence transformers",
    version="1.0.0"
)

# Add CORS middleware to allow requests from Flutter/web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Flutter app's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize FAQ Bot (this will load the model on startup)
logger.info("Loading FAQ Bot model...")
try:
    faq_bot = FAQBot()
    logger.info("FAQ Bot model loaded successfully!")
except Exception as e:
    logger.error(f"Failed to load FAQ Bot: {str(e)}")
    faq_bot = None

# Pydantic models for request/response
class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 3
    min_score: Optional[float] = 0.0

class FAQResult(BaseModel):
    question: str
    answer: str
    score: float
    category: Optional[str] = "General"

class QueryResponse(BaseModel):
    success: bool
    results: List[FAQResult]
    message: Optional[str] = None
    query: str
    total_results: int

class HealthResponse(BaseModel):
    status: str
    message: str
    model_loaded: bool

# API Routes
@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Mental Health FAQ API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "query": "/faq",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if faq_bot is not None else "unhealthy",
        message="FAQ Bot is ready" if faq_bot is not None else "FAQ Bot failed to load",
        model_loaded=faq_bot is not None
    )

@app.post("/faq", response_model=QueryResponse)
async def query_faq(request: QueryRequest):
    """
    Query the FAQ bot with a question and get similar FAQ results
    
    - **question**: The user's question
    - **top_k**: Number of top results to return (default: 3, max: 10)
    - **min_score**: Minimum similarity score to include (default: 0.0, range: 0.0-1.0)
    """
    try:
        # Validate FAQ bot is loaded
        if faq_bot is None:
            raise HTTPException(status_code=503, detail="FAQ Bot model is not available")
        
        # Validate input
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Limit top_k to reasonable bounds
        top_k = min(max(request.top_k, 1), 10)
        min_score = max(min(request.min_score, 1.0), 0.0)
        
        logger.info(f"Processing query: '{request.question[:50]}...' (top_k={top_k}, min_score={min_score})")
        
        # Get results from FAQ bot
        results = faq_bot.get_most_similar(request.question, top_k=top_k)
        
        # Filter by minimum score and format results
        filtered_results = [
            FAQResult(
                question=result.get('question', '').strip(),
                answer=result.get('answer', result.get('text', '')).strip(),
                score=round(float(result.get('score', 0.0)), 4),
                category=result.get('category', 'General')
            )
            for result in results
            if result.get('score', 0.0) >= min_score
        ]
        
        # Determine response message
        message = None
        if not filtered_results:
            message = "No results found matching your criteria. Try lowering the minimum score or rephrasing your question."
        elif filtered_results and filtered_results[0].score < 0.5:
            message = "The results have low confidence. Consider rephrasing your question for better matches."
        
        return QueryResponse(
            success=True,
            results=filtered_results,
            message=message,
            query=request.question,
            total_results=len(filtered_results)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/stats", response_model=dict)
async def get_stats():
    """Get statistics about the FAQ database"""
    try:
        if faq_bot is None:
            raise HTTPException(status_code=503, detail="FAQ Bot model is not available")
        
        return {
            "total_faqs": len(faq_bot.faq_df),
            "model_name": "sentence-transformers/all-MiniLM-L6-v2",
            "embedding_dimensions": faq_bot.question_embeddings.shape[1] if hasattr(faq_bot.question_embeddings, 'shape') else "unknown"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Endpoint not found", "message": "Check /docs for available endpoints"}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "message": "Something went wrong on our end"}

if __name__ == "__main__":
    # Run the server
    # Read port from environment variable (for Render.com) or default to 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        app,  # Changed from "faq_api:app" to app
        host="0.0.0.0",
        port=port,
        log_level="info"
    )