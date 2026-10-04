"""
File Utils - File loading and parsing utilities
"""

import os
import json
import yaml
from typing import Any, Dict, List

def load_yaml(file_path: str) -> Any:
    """Load YAML file content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        # Load all documents, but return the first one as a default behavior
        documents = list(yaml.safe_load_all(f))
        if not documents:
            return {}
        if len(documents) == 1:
            return documents[0]
        return documents

def load_json(file_path: str) -> Any:
    """Load JSON file content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_yaml(data: Any, file_path: str) -> None:
    """Save data to YAML file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)

def save_json(data: Any, file_path: str, indent: int = 4) -> None:
    """Save data to JSON file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
