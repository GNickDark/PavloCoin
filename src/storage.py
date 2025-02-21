import json
from pathlib import Path
from typing import Dict, Any
import fcntl
import os

class SecureStorage:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        # Create parent directories if they don't exist
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self.file_path.touch(exist_ok=True)
        # Set secure file permissions
        os.chmod(self.file_path, 0o600)

    def load(self) -> Dict[str, Any]:
        try:
            with open(self.file_path, 'r') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                try:
                    return json.load(f) if self.file_path.stat().st_size > 0 else {}
                except json.JSONDecodeError:
                    return {}
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        except (IOError, PermissionError) as e:
            raise RuntimeError(f"Failed to load storage file: {e}")

    def save(self, data: Dict[str, Any]) -> None:
        if not isinstance(data, dict):
            raise TypeError("Data must be a dictionary")
            
        try:
            with open(self.file_path, 'w') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                try:
                    json.dump(data, f, indent=4)
                    f.flush()
                    os.fsync(f.fileno())  # Ensure data is written to disk
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        except (IOError, PermissionError) as e:
            raise RuntimeError(f"Failed to save to storage file: {e}")
