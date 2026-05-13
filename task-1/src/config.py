"""Configuration loader.

Read INPUT_PATH and OUTPUT_PATH from a .env file (see .env.example for the
expected variable names) and expose them as named imports.

Tasks (see chapter Task 1):
  1. Use python-dotenv's load_dotenv() to read the .env file.
  2. Read INPUT_PATH and OUTPUT_PATH from os.environ.
  3. Raise ValueError if either is missing — do NOT let None silently propagate.
"""
import os

from dotenv import load_dotenv


# Load .env values into os.environ before they're read by _required().
# (Step 1 from the docstring above; already wired up so the rest of the
# module can rely on os.environ being populated.)
load_dotenv()


def _required(name: str) -> str:
    """Read an env var; fail loudly if missing."""

    value = os.environ.get(name)
    if not value:
        raise ValueError(f"Environment variable '{name}' is not set. Please check .env.example.")
    return value

INPUT_PATH: str = _required("INPUT_PATH")
OUTPUT_PATH: str = _required("OUTPUT_PATH")
