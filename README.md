Memory Stack 🧠

AI-Powered Flashcard Generator

Overview

Memory Stack is a lightweight web application that converts study notes into structured flashcards using AI. The goal of the project is to improve study efficiency while demonstrating practical skills in Python, API usage, and rapid UI development with Streamlit.

This project was built with a focus on learning by building: understanding how APIs, data parsing, and frontend layouts work together in a real application.

Features: 
- Paste raw study notes and generate flashcards automatically
- Clean two-column UI (input → output)
- Structured Q&A flashcards generated using OpenAI
- Designed for future expansion (Quiz Mode, spaced repetition, etc.)
- No HTML/CSS required — pure Python via Streamlit

Tech Stack: 
- Python
- Streamlit – frontend & app framework
- OpenAI API – flashcard generation
- JSON – structured data exchange

How It Works
- User pastes study notes into the app
- Notes are sent to the OpenAI API with instructions to return structured flashcards
- The response is parsed from JSON into Python objects
- Flashcards are rendered dynamically in the UI

Demo Link: https://memory-stack-flashcard-ai.streamlit.app/
