#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility Functions Module
Clipboard operations, QR code generation, file export, and password history.
"""

import json
import csv
import hashlib
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


def copy_to_clipboard(text: str) -> bool:
    """
    Copy text to system clipboard.
    
    Args:
        text: Text to copy
    
    Returns:
        True if successful, False otherwise
    """
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except ImportError:
        print("⚠️  pyperclip not installed. Install with: pip install pyperclip")
        return False
    except Exception as e:
        print(f"⚠️  Failed to copy to clipboard: {e}")
        return False


def generate_qr_code(text: str, filename: Optional[str] = None) -> bool:
    """
    Generate a QR code for the given text.
    
    Args:
        text: Text to encode in QR code (usually a password)
        filename: Optional filename to save QR code image
    
    Returns:
        True if successful, False otherwise
    """
    try:
        import qrcode
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        if filename:
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(filename)
            print(f"✓ QR code saved to: {filename}")
        else:
            # Print ASCII QR code to terminal
            qr.print_ascii()
        
        return True
    except ImportError:
        print("⚠️  qrcode not installed. Install with: pip install qrcode[pil]")
        return False
    except Exception as e:
        print(f"⚠️  Failed to generate QR code: {e}")
        return False


def export_passwords_json(passwords: List[str], filename: str) -> bool:
    """
    Export passwords to JSON file.
    
    Args:
        passwords: List of passwords
        filename: Output filename
    
    Returns:
        True if successful, False otherwise
    """
    try:
        data = {
            'generated_at': datetime.now().isoformat(),
            'count': len(passwords),
            'passwords': passwords
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Passwords exported to: {filename}")
        return True
    except Exception as e:
        print(f"⚠️  Failed to export to JSON: {e}")
        return False


def export_passwords_csv(passwords: List[str], filename: str) -> bool:
    """
    Export passwords to CSV file.
    
    Args:
        passwords: List of passwords
        filename: Output filename
    
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Password', 'Generated At'])
            timestamp = datetime.now().isoformat()
            for pwd in passwords:
                writer.writerow([pwd, timestamp])
        
        print(f"✓ Passwords exported to: {filename}")
        return True
    except Exception as e:
        print(f"⚠️  Failed to export to CSV: {e}")
        return False


def export_passwords_txt(passwords: List[str], filename: str) -> bool:
    """
    Export passwords to plain text file.
    
    Args:
        passwords: List of passwords
        filename: Output filename
    
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Generated Passwords - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Total: {len(passwords)}\n\n")
            for pwd in passwords:
                f.write(f"{pwd}\n")
        
        print(f"✓ Passwords exported to: {filename}")
        return True
    except Exception as e:
        print(f"⚠️  Failed to export to TXT: {e}")
        return False


def export_passwords(passwords: List[str], filename: str) -> bool:
    """
    Export passwords to file (auto-detect format from extension).
    
    Args:
        passwords: List of passwords
        filename: Output filename (.json, .csv, or .txt)
    
    Returns:
        True if successful, False otherwise
    """
    ext = Path(filename).suffix.lower()
    
    if ext == '.json':
        return export_passwords_json(passwords, filename)
    elif ext == '.csv':
        return export_passwords_csv(passwords, filename)
    elif ext == '.txt':
        return export_passwords_txt(passwords, filename)
    else:
        print(f"⚠️  Unsupported file format: {ext}")
        print("   Supported formats: .json, .csv, .txt")
        return False


def hash_password(password: str) -> str:
    """
    Create a SHA-256 hash of a password (for history tracking).
    
    Args:
        password: Password to hash
    
    Returns:
        Hexadecimal hash string
    """
    return hashlib.sha256(password.encode()).hexdigest()


def save_to_history(password: str, history_file: str = '.rpg_history.json') -> bool:
    """
    Save password hash to history file (for tracking, not storing actual passwords).
    
    Args:
        password: Password to add to history
        history_file: Path to history file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Load existing history
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = {'passwords': []}
        
        # Add new entry
        entry = {
            'hash': hash_password(password),
            'length': len(password),
            'generated_at': datetime.now().isoformat()
        }
        
        history['passwords'].append(entry)
        
        # Keep only last 100 entries
        if len(history['passwords']) > 100:
            history['passwords'] = history['passwords'][-100:]
        
        # Save updated history
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2)
        
        return True
    except Exception as e:
        print(f"⚠️  Failed to save to history: {e}")
        return False


def check_history(password: str, history_file: str = '.rpg_history.json') -> bool:
    """
    Check if a password (hash) exists in history.
    
    Args:
        password: Password to check
        history_file: Path to history file
    
    Returns:
        True if password found in history, False otherwise
    """
    try:
        if not os.path.exists(history_file):
            return False
        
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        pwd_hash = hash_password(password)
        return any(entry['hash'] == pwd_hash for entry in history.get('passwords', []))
    except Exception:
        return False


def format_size_bytes(size_bytes: int) -> str:
    """
    Format byte size to human-readable string.
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Formatted string (e.g., "1.5 KB", "2.3 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"
