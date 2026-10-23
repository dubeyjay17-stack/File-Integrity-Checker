# File Integrity Checker Using SHA-256

A Python desktop application built using Tkinter and hashlib to detect unauthorized file changes, corruption, or tampering using SHA-256 cryptographic hashing.

## Features
- **SHA-256 Hash Generation:** Computes unique 256-bit hash signatures for files using block-by-block streaming.
- **Reference Storage:** Saves reference hashes locally in `reference_hashes.json`.
- **Integrity Verification:** Compares real-time computed hashes against stored reference baselines to flag modifications.
- **Graphical User Interface:** Built with Python's native `tkinter` library.

## Tech Stack
- **Language:** Python 3.x
- **Libraries:** `hashlib`, `tkinter`, `json`, `os`

## Project Structure
- `integrity_checker.py` - Core application logic and GUI interface
- `reference_hashes.json` - Stored hash database
- `sample.txt.txt` - Verification test file

## How to Run
1. Clone the repository:
```bash
git clone [https://github.com/dubeyjay17-stack/File-Integrity-Checker.git](https://github.com/dubeyjay17-stack/File-Integrity-Checker.git)
cd File-Integrity-Checker
