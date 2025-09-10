#!/usr/bin/env python3
"""
Run script for the AI Prescription Verifier application.
This script provides an easy way to run the FastAPI application.
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["app"],  # Only watch the app directory for changes
        log_level="info"
    )
