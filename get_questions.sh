#!/bin/bash

# Advent of Code Question Downloader
# Usage: ./get_questions.sh

YEAR=2025
COOKIE_FILE=".session_cookie"

# 0. Setup Virtual Environment
VENV_DIR=".venv"
PYTHON="$VENV_DIR/bin/python"
PIP="$VENV_DIR/bin/pip"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    
    echo "Installing dependencies..."
    "$PIP" install -r requirements.txt
    "$PIP" install playwright
    "$PYTHON" -m playwright install chromium
fi

# 1. Check for session cookie
if [ ! -f "$COOKIE_FILE" ]; then
    echo "Session cookie not found. Launching interactive login..."
    "$PYTHON" auth.py
    if [ ! -f "$COOKIE_FILE" ]; then
        echo "Login failed or cancelled. Exiting."
        exit 1
    fi
fi

# Load cookie
COOKIE=$(cat "$COOKIE_FILE")

# 2. Loop through days 1-25
for day in {1..25}; do
    echo "Processing Day $day..."
    
    # Create directory
    DIR="Day $day"
    mkdir -p "$DIR"
    
    # Define files
    HTML_FILE="$DIR/index.html"
    README_FILE="$DIR/README.md"
    
    # Download page
    URL="https://adventofcode.com/$YEAR/day/$day"
    echo "  Downloading $URL..."
    
    # Use curl with the cookie. -s for silent, -f to fail on 404 (e.g. future days)
    if curl -s -f -b "$COOKIE" "$URL" -o "$HTML_FILE"; then
        
        # Check if the page contains "Please don't repeatedly request this endpoint" or other errors not caught by -f
        # (AoC returns 200 even for "Puzzle not available yet" sometimes, but usually 404 for future days)
        
        # Extract the article content using Python
        # We use a small python script to parse the HTML because it's more robust than grep/sed
        # Extract the article content using separate Python script
        "$PYTHON" extract_content.py "$HTML_FILE" > "$DIR/temp_article.html"

        # Check if we got any content (if day is not unlocked, we might get nothing or a specific message)
        if [ -s "$DIR/temp_article.html" ]; then
            # Convert to Markdown using pandoc
            pandoc "$DIR/temp_article.html" -o "$README_FILE" --from html --to gfm
            
            echo "  Success! Saved to $README_FILE"
        else
            echo "  No question content found (maybe not unlocked yet?)."
        fi
        
        # Cleanup temp files
        rm -f "$HTML_FILE" "$DIR/temp_article.html"
        
    else
        echo "  Day $day not available yet (404). Stopping."
        rm -rf "$DIR"
        break
    fi
    
    # Be nice to the server
    sleep 1
done

echo "Done!"
