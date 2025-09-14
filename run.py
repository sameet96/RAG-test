#!/usr/bin/env python3
"""
Main entry point for the RAG PDF Chat Application
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Run the main script
from scripts.run import main

if __name__ == "__main__":
    main()
