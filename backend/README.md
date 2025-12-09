# Pharmaceutical Research Backend

Flask API server for the multi-agent pharmaceutical research system.

## Setup

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Make sure Ollama is running:**
   ```bash
   ollama serve
   ollama pull llama3
   ```

3. **Set API keys (optional but recommended):**
   ```bash
   export SERPER_API_KEY="your_serper_api_key"
   ```

4. **Start the server:**
   ```bash
   python server.py
   ```

   The server will start on `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /api/health
```

### Start Research
```
POST /api/research/start
Content-Type: application/json

{
  "molecule_name": "Metformin"
}

Response:
{
  "job_id": "uuid-here",
  "message": "Research started for Metformin"
}
```

### Check Status
```
GET /api/research/status/<job_id>

Response:
{
  "job_id": "uuid-here",
  "molecule_name": "Metformin",
  "status": "running",  // pending, running, complete, error
  "elapsed_seconds": 120
}
```

### Get Results
```
GET /api/research/result/<job_id>

Response:
{
  "job_id": "uuid-here",
  "molecule_name": "Metformin",
  "result": "# Research Report\n\n..."
}
```

## Notes

- Research typically takes 10-15 minutes to complete
- The frontend polls `/api/research/status` every 10 seconds
- Results are stored in memory (restart clears them)
- Output is also saved to `output.txt` in this directory
