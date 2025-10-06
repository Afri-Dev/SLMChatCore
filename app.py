from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import logging
import os
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

# Initialize FAQ Bot as None (will be loaded on first request)
faq_bot = None

def get_faq_bot():
    """Lazy load FAQ Bot on first request"""
    global faq_bot
    if faq_bot is None:
        logger.info("Loading FAQ Bot model...")
        try:
            # Import FAQBot only when needed
            from faq_bot import FAQBot
            faq_bot = FAQBot()
            logger.info("FAQ Bot model loaded successfully!")
        except Exception as e:
            logger.error(f"Failed to load FAQ Bot: {str(e)}")
            raise
    return faq_bot

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
        message="FAQ Bot is ready" if faq_bot is not None else "FAQ Bot not loaded yet",
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
        # Load FAQ bot on first request (lazy loading)
        bot = get_faq_bot()
        
        # Validate input
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Detect conversational greetings/check-ins
        question_lower = request.question.lower().strip()
        conversational_patterns = [
            "how are you", "how r u", "how are u", "how's it going", 
            "what's up", "whats up", "hey", "hi there", "hello",
            "good morning", "good afternoon", "good evening"
        ]
        
        if any(pattern in question_lower for pattern in conversational_patterns):
            return QueryResponse(
                success=True,
                results=[FAQResult(
                    question="How can I help you?",
                    answer="Hello! I'm here to help with mental health questions. You can ask me about:\n\n• Stress and anxiety management\n• Depression and mood\n• Sleep problems\n• Coping strategies\n• Mental health resources\n• Self-care tips\n\nWhat would you like to know about?",
                    score=1.0,
                    category="Greeting"
                )],
                message="I'm ready to help with mental health questions!",
                query=request.question,
                total_results=1
            )
        
        # Limit top_k to reasonable bounds
        top_k = min(max(request.top_k, 1), 10)
        min_score = max(min(request.min_score, 1.0), 0.0)
        
        logger.info(f"Processing query: '{request.question[:50]}...' (top_k={top_k}, min_score={min_score})")
        
        # Get results from FAQ bot
        results = bot.get_most_similar(request.question, top_k=top_k)
        
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

# ✅ CORRECT Error handlers - Return JSONResponse instead of dict
# This fixes the "'dict' object is not callable" error
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "message": "Check /docs for available endpoints"}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "message": "Something went wrong on our end"}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    General exception handler for all unhandled exceptions
    ✅ CORRECT - Return JSONResponse instead of dict to avoid 'dict' object is not callable error
    
    # ❌ WRONG - This would cause TypeError:
    # return {"error": str(exc)}
    """
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

if __name__ == "__main__":
    # Run the server
    # Port 7860 for Hugging Face Spaces, fallback to 8000 for local
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
