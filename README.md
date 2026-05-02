# AI Service — Internal Controls Testing

## Overview
Flask-based AI microservice running on port 5000. Provides AI-powered endpoints for internal controls testing using Groq's LLaMA-3.3-70b model.

## Prerequisites
- Python 3.11
- Groq API key (get free at console.groq.com)
- Redis (optional — for caching)

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/Bhoomitha/internal-controls-testing-platform.git
cd internal-controls-testing-platform
```

### 2. Create .env file
```bash
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the service
```bash
python app.py
```

Service runs on http://localhost:5000

## API Reference

### GET /health
Returns service health status.

**Response:**
```json
{
  "status": "ok",
  "model": "llama-3.3-70b-versatile",
  "avg_response_time_seconds": 0.941,
  "uptime_seconds": 120,
  "redis_available": false
}
```

### POST /describe
Generates a structured description of an internal control.

**Request:**
```json
{
  "input": "Access control review for employee login system"
}
```

**Response:**
```json
{
  "result": "...",
  "generated_at": "2026-04-28T15:00:11.697456",
  "response_time_seconds": 1.095
}
```

### POST /recommend
Returns 3 recommendations for an internal control.

**Request:**
```json
{
  "input": "Access control review for employee login system"
}
```

**Response:**
```json
{
  "recommendations": "[{\"action_type\": \"Review\", \"description\": \"...\", \"priority\": \"High\"}]",
  "generated_at": "2026-04-28T15:00:23.824112",
  "response_time_seconds": 0.987
}
```

### POST /generate-report
Generates a full audit report for an internal control.

**Request:**
```json
{
  "input": "Access control review for employee login system"
}
```

**Response:**
```json
{
  "report": "...",
  "generated_at": "2026-04-28T15:00:45.123456",
  "response_time_seconds": 1.234
}
```

## Docker

### Build
```bash
docker build -t ai-service .
```

### Run
```bash
docker run -p 5000:5000 --env-file .env ai-service
```

## Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| GROQ_API_KEY | Your Groq API key | Yes |