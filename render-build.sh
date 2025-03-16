#!/bin/bash

# Install ffmpeg
echo "Installing ffmpeg..."
apt-get update && apt-get install -y ffmpeg

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Build completed successfully!"
