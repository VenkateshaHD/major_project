import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Ensure the backend directory is in the path for module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes.model_class import ModelService
from classes.database_class import Database
from classes.scraper_class import ScraperService
from routes import review_routes

app = FastAPI(title="GenAI Fake Review Detection API")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Services
print("Initializing Model Service...")
model_service = ModelService(model_dir="model_save")

print("Initializing Database Service...")
db_service = Database()

print("Initializing Scraper Service...")
scraper_service = ScraperService()

# Inject services into routes module
review_routes.model_service = model_service
review_routes.db_service = db_service
review_routes.scraper_service = scraper_service

# Include Routers
app.include_router(review_routes.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "GenAI Fake Product Review Detection API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
