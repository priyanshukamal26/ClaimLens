# ENVIRONMENT.md — Local Development Setup

## Prerequisites
- Python 3.12+
- Node.js 20+
- Git

## 1. Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables
Create `backend/.env`:
```ini
# Debug mode
DEBUG=true

# Allowed CORS origins
CORS_ORIGINS=http://localhost:5173

# LLM API Keys (Required for Ask ClaimLens live queries)
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL_ID=llama-3.1-8b-instant

GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL_ID=gemini-1.5-flash
```

### Running the Backend
```bash
python -m app.main
```
The server will start on `http://localhost:8000`.
*Note: On first boot, the system will automatically generate synthetic data (takes ~5-10 seconds) and run the anomaly detection pipeline.*

## 2. Frontend Setup

```bash
cd frontend
npm install
```

### Running the Frontend
```bash
npm run dev
```
The app will start on `http://localhost:5173`.

Vite is configured to proxy API requests:
```javascript
// vite.config.js
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
```

## 3. Database Management

The databases are stored in `backend/data/`:
- `claimlens.db`: SQLite operational store (safe to view with any SQLite browser)
- `analytics.duckdb`: DuckDB analytics layer

**Resetting the system:**
To regenerate all synthetic data from scratch, simply delete the `data` folder and restart the backend:
```bash
rm -rf backend/data
python -m app.main
```
