#!/bin/bash

echo "🧪 Running tests..."

if [ -d "venv" ]; then
    source venv/bin/activate
fi

pytest tests/ -v

echo "✅ Done!"
