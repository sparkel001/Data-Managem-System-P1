"""Test server override; every test still explicitly chooses a UUID database."""
import os
from pathlib import Path

MONGO_URI = os.environ.get('TEST_MONGODB_URI', 'mongodb://127.0.0.1:27017')
ARTIFACT_DIR = Path(os.environ.get('TEST_ARTIFACT_DIR', 'test-results/phase2'))
