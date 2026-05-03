from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import List, Dict

# We will inject the dependencies later in main.py
router = APIRouter()

# Global variables to hold instances injected from main.py
model_service = None
db_service = None
scraper_service = None

class ReviewRequest(BaseModel):
    review_text: str

class ScrapeRequest(BaseModel):
    url: HttpUrl

@router.post("/predict-review")
async def predict_review(request: ReviewRequest):
    if not request.review_text.strip():
        raise HTTPException(status_code=400, detail="Review text cannot be empty")
        
    try:
        # Predict
        result = model_service.predict(request.review_text)
        
        # Save to database
        db_service.insert_review(
            text=request.review_text,
            prediction=result["prediction"],
            confidence=result["confidence"]
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/scrape-and-predict")
async def scrape_and_predict(request: ScrapeRequest):
    try:
        # Scrape reviews
        reviews = scraper_service.scrape_reviews(str(request.url))
        
        if not reviews:
            return {"message": "No reviews found at this URL", "results": []}
            
        results = []
        fake_count = 0
        
        # Predict and store each review
        for review_text in reviews:
            pred_result = model_service.predict(review_text)
            
            # Save to DB
            db_service.insert_review(
                text=review_text,
                prediction=pred_result["prediction"],
                confidence=pred_result["confidence"]
            )
            
            if pred_result["prediction"] == "Fake":
                fake_count += 1
                
            results.append({
                "review_text": review_text,
                "prediction": pred_result["prediction"],
                "confidence": pred_result["confidence"]
            })
            
        total = len(results)
        fake_percentage = round((fake_count / total * 100), 2) if total > 0 else 0
        
        return {
            "total_scraped": total,
            "fake_percentage": fake_percentage,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard-stats")
async def get_dashboard_stats():
    try:
        stats = db_service.fetch_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
