const API_BASE_URL = 'http://localhost:8000/api';

// For index.html
document.addEventListener('DOMContentLoaded', () => {
    
    // --- Single Review Prediction ---
    const reviewForm = document.getElementById('reviewForm');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const text = document.getElementById('reviewText').value;
            const resultDiv = document.getElementById('singleResult');
            const loader = document.getElementById('singleLoader');
            
            if (!text.trim()) return;

            resultDiv.innerHTML = '';
            resultDiv.classList.remove('fade-in');
            loader.style.display = 'block';

            try {
                const response = await fetch(`${API_BASE_URL}/predict-review`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ review_text: text })
                });
                
                const data = await response.json();
                
                loader.style.display = 'none';
                
                if (response.ok) {
                    const isFake = data.prediction === 'Fake';
                    const badgeClass = isFake ? 'badge-fake' : 'badge-genuine';
                    const icon = isFake ? '⚠️' : '✅';
                    
                    resultDiv.innerHTML = `
                        <div class="result-badge ${badgeClass} fade-in">
                            ${icon} ${data.prediction} Review <br>
                            <small class="text-white-50" style="font-size: 0.8rem;">Confidence: ${(data.confidence * 100).toFixed(2)}%</small>
                        </div>
                    `;
                } else {
                    resultDiv.innerHTML = `<div class="text-danger mt-3 fade-in">Error: ${data.detail || 'An error occurred'}</div>`;
                }
            } catch (error) {
                loader.style.display = 'none';
                resultDiv.innerHTML = `<div class="text-danger mt-3 fade-in">Failed to connect to the server. Is it running?</div>`;
            }
        });
    }

    // --- URL Scrape & Predict ---
    const urlForm = document.getElementById('urlForm');
    if (urlForm) {
        urlForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const url = document.getElementById('productUrl').value;
            const resultDiv = document.getElementById('urlResult');
            const loader = document.getElementById('urlLoader');
            
            if (!url.trim()) return;

            resultDiv.innerHTML = '';
            loader.style.display = 'block';

            try {
                const response = await fetch(`${API_BASE_URL}/scrape-and-predict`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: url })
                });
                
                const data = await response.json();
                loader.style.display = 'none';
                
                if (response.ok) {
                    let html = `<h4 class="mt-4 mb-3">Scraping Results</h4>`;
                    html += `<p>Analyzed <strong>${data.total_scraped}</strong> reviews. 
                                <span class="text-fake">${data.fake_percentage}% Fake</span></p>`;
                    
                    html += `<div class="mt-3">`;
                    data.results.forEach((r, idx) => {
                        const badgeClass = r.prediction === 'Fake' ? 'text-fake' : 'text-genuine';
                        html += `
                            <div class="p-3 mb-2 rounded" style="background: rgba(0,0,0,0.2); border-left: 4px solid var(--${r.prediction === 'Fake' ? 'fake-color' : 'genuine-color'})">
                                <small class="d-block mb-1 ${badgeClass} fw-bold">${r.prediction} (${(r.confidence * 100).toFixed(1)}%)</small>
                                <div style="font-size: 0.9rem;">"${r.review_text}"</div>
                            </div>
                        `;
                    });
                    html += `</div>`;
                    
                    resultDiv.innerHTML = html;
                    resultDiv.classList.add('fade-in');
                } else {
                    resultDiv.innerHTML = `<div class="text-danger mt-3 fade-in">Error: ${data.detail || 'An error occurred'}</div>`;
                }
            } catch (error) {
                loader.style.display = 'none';
                resultDiv.innerHTML = `<div class="text-danger mt-3 fade-in">Failed to connect to the server.</div>`;
            }
        });
    }

    // --- Dashboard Stats ---
    if (window.location.pathname.includes('dashboard.html')) {
        fetchStats();
    }
});

async function fetchStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/dashboard-stats`);
        if (response.ok) {
            const data = await response.json();
            
            // Animate numbers
            animateValue("totalReviews", 0, data.total_reviews, 1000);
            animateValue("genuineCount", 0, data.genuine_count, 1000);
            animateValue("fakeCount", 0, data.fake_count, 1000);
            
            // Update progress bars
            document.getElementById("genuineProgress").style.width = `${data.genuine_percentage}%`;
            document.getElementById("genuineProgress").textContent = `${data.genuine_percentage}%`;
            
            document.getElementById("fakeProgress").style.width = `${data.fake_percentage}%`;
            document.getElementById("fakeProgress").textContent = `${data.fake_percentage}%`;
            
            // Setup simple chart logic via DOM manipulation instead of large libraries for simplicity,
            // but the rich UI makes up for it.
        }
    } catch (error) {
        console.error("Failed to load stats", error);
    }
}

// Helper to animate numbers
function animateValue(id, start, end, duration) {
    if (start === end) {
        document.getElementById(id).textContent = end;
        return;
    }
    let range = end - start;
    let current = start;
    let increment = end > start ? 1 : -1;
    // Calculate step time, avoiding division by 0 and extremely fast steps
    let stepTime = Math.max(Math.abs(Math.floor(duration / range)), 20);
    let obj = document.getElementById(id);
    
    let timer = setInterval(function() {
        current += increment;
        obj.textContent = current;
        if (current == end) {
            clearInterval(timer);
        }
    }, stepTime);
}
