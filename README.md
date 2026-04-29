# Internal Controls Testing Platform

## Overview
This project is a simple AI Testing Platform built using:
- FastAPI (Backend)
- React (Frontend)

## Features
- User input from UI
- Backend API processing
- Response display

## Project Structure
- ai-service → FastAPI backend
- frontend → React app

## Run Backend
cd ai-service
uvicorn main:app --reload

## Run Frontend
cd frontend
npm start

## API Endpoint
POST /ai

Request:
{
  "text": "hello"
}

Response:
{
  "response": "You said: hello"
}