# GenAI-Based Detection of Fake Product Reviews

This project provides a full-stack solution to detect fake product reviews using a fine-tuned BERT Transformer model. It includes a FastAPI backend, a MySQL database for storing review history, and a rich, glassmorphism-styled HTML/JS frontend.

## Project Structure

```
project-root/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── requirements.txt        # Python dependencies
│   ├── model_save/             # (Created after training) Stores the BERT model
│   ├── routes/
│   │   └── review_routes.py    # API endpoints
│   └── classes/
│       ├── model_class.py      # ModelService for BERT inference
│       ├── database_class.py   # MySQL database interactions
│       └── scraper_class.py    # Web scraping service
├── frontend/
│   ├── index.html              # Main application UI
│   ├── dashboard.html          # Analytics dashboard
│   ├── styles.css              # Custom styling (glassmorphism/dark mode)
│   └── script.js               # Frontend logic and API calls
├── training/
│   └── train_model.ipynb       # Jupyter notebook for BERT fine-tuning
├── dataset/
│   └── sample_reviews.csv      # Mock dataset for training
├── docker-compose.yml          # Docker composition file
├── Dockerfile                  # Docker container definition
└── README.md                   # This file
```

## Setup & Running

### Using Docker (Recommended)

1. Make sure Docker and Docker Compose are installed.
2. In the `project-root` directory, run:
   ```bash
   docker-compose up --build
   ```
3. The API will be available at `http://localhost:8000/api`.
4. Simply open `frontend/index.html` in your browser to use the application.

### Manual Setup

1. **Database:** Ensure you have a local MySQL server running with a database named `reviews_db` and credentials `root/root`.
2. **Backend:**
   ```bash
   cd backend
   pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu
   python main.py
   ```
3. **Frontend:** Open `index.html` in a web browser.

## Features

- **Direct Text Analysis:** Paste any review text to get an instant fake/genuine classification and confidence score.
- **Product Link Analysis:** Paste an Amazon or Flipkart URL to scrape reviews and analyze them in bulk (uses mock data if scraping is blocked by anti-bot measures).
- **Analytics Dashboard:** View system-wide metrics including total reviews processed and the distribution of fake vs. genuine reviews.

