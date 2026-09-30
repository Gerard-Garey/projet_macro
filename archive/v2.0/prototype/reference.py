"""One explicit reference configuration shared by both public CLIs."""
import json
from pathlib import Path

def reference_parameters():
    return json.loads((Path(__file__).resolve().parents[1]/'config/reference.json').read_text())
