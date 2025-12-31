#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Password Strength Analyzer Module
Analyzes password strength based on entropy, character diversity, and common patterns.
"""

import math
import string
from typing import Dict, Tuple
import re


# Common weak passwords (top 100 most common)
COMMON_PASSWORDS = {
    'password', '123456', '12345678', 'qwerty', 'abc123', 'monkey', '1234567',
    'letmein', 'trustno1', 'dragon', 'baseball', 'iloveyou', 'master', 'sunshine',
    'ashley', 'bailey', 'passw0rd', 'shadow', '123123', '654321', 'superman',
    'qazwsx', 'michael', 'football', 'welcome', 'jesus', 'ninja', 'mustang',
    'password1', '123456789', '12345', '1234', '111111', '1234567890', '000000',
    'admin', 'root', 'toor', 'pass', 'test', 'guest', 'info', 'adm', 'mysql',
    'user', 'administrator', 'oracle', 'ftp', 'pi', 'puppet', 'ansible', 'ec2-user',
    'vagrant', 'azureuser', 'qwerty123', 'password123', 'admin123'
}


def calculate_entropy(password: str) -> float:
    """
    Calculate the entropy (randomness) of a password in bits.
    
    Args:
        password: The password to analyze
    
    Returns:
        Entropy value in bits
    """
    if not password:
        return 0.0
    
    # Determine character pool size
    pool_size = 0
    
    if any(c in string.ascii_lowercase for c in password):
        pool_size += 26
    if any(c in string.ascii_uppercase for c in password):
        pool_size += 26
    if any(c in string.digits for c in password):
        pool_size += 10
    if any(c in string.punctuation for c in password):
        pool_size += len(string.punctuation)
    
    # Calculate entropy: log2(pool_size ^ length)
    if pool_size > 0:
        entropy = len(password) * math.log2(pool_size)
    else:
        entropy = 0.0
    
    return entropy


def analyze_password_strength(password: str) -> Dict[str, any]:
    """
    Comprehensive password strength analysis.
    
    Args:
        password: The password to analyze
    
    Returns:
        Dictionary containing:
            - score: Overall score (0-100)
            - strength: Text rating ('Very Weak', 'Weak', 'Medium', 'Strong', 'Very Strong')
            - entropy: Entropy in bits
            - length: Password length
            - has_uppercase: Boolean
            - has_lowercase: Boolean
            - has_digits: Boolean
            - has_special: Boolean
            - is_common: Boolean (found in common passwords list)
            - feedback: List of improvement suggestions
    """
    if not password:
        return {
            'score': 0,
            'strength': 'Very Weak',
            'entropy': 0,
            'length': 0,
            'has_uppercase': False,
            'has_lowercase': False,
            'has_digits': False,
            'has_special': False,
            'is_common': False,
            'feedback': ['Password cannot be empty']
        }
    
    # Character type checks
    has_uppercase = any(c in string.ascii_uppercase for c in password)
    has_lowercase = any(c in string.ascii_lowercase for c in password)
    has_digits = any(c in string.digits for c in password)
    has_special = any(c in string.punctuation for c in password)
    
    # Length check
    length = len(password)
    
    # Common password check
    is_common = password.lower() in COMMON_PASSWORDS
    
    # Calculate entropy
    entropy = calculate_entropy(password)
    
    # Calculate base score
    score = 0
    feedback = []
    
    # Length scoring (0-30 points)
    if length < 8:
        score += length * 2
        feedback.append(f"Increase length (currently {length}, recommended: 12+)")
    elif length < 12:
        score += 16 + (length - 8) * 2
        feedback.append("Good length, but 12+ characters is better")
    elif length < 16:
        score += 24 + (length - 12)
    else:
        score += 30
    
    # Character diversity scoring (0-40 points)
    diversity_score = 0
    if has_lowercase:
        diversity_score += 10
    else:
        feedback.append("Add lowercase letters")
    
    if has_uppercase:
        diversity_score += 10
    else:
        feedback.append("Add uppercase letters")
    
    if has_digits:
        diversity_score += 10
    else:
        feedback.append("Add numbers")
    
    if has_special:
        diversity_score += 10
    else:
        feedback.append("Add special characters (!@#$%^&*)")
    
    score += diversity_score
    
    # Entropy bonus (0-20 points)
    if entropy >= 80:
        score += 20
    elif entropy >= 60:
        score += 15
    elif entropy >= 40:
        score += 10
    elif entropy >= 20:
        score += 5
    
    # Pattern penalties
    # Sequential characters
    if re.search(r'(abc|bcd|cde|123|234|345|456|567|678|789)', password.lower()):
        score -= 10
        feedback.append("Avoid sequential characters (abc, 123)")
    
    # Repeated characters
    if re.search(r'(.)\1{2,}', password):
        score -= 10
        feedback.append("Avoid repeated characters (aaa, 111)")
    
    # Keyboard patterns
    if re.search(r'(qwerty|asdfgh|zxcvbn)', password.lower()):
        score -= 15
        feedback.append("Avoid keyboard patterns (qwerty, asdf)")
    
    # Common password penalty
    if is_common:
        score -= 50
        feedback.append("This is a commonly used password - VERY UNSAFE!")
    
    # Bonus for good practices (0-10 points)
    if length >= 16 and diversity_score == 40:
        score += 10
    
    # Ensure score is within bounds
    score = max(0, min(100, score))
    
    # Determine strength category
    if score < 20:
        strength = 'Very Weak'
    elif score < 40:
        strength = 'Weak'
    elif score < 60:
        strength = 'Medium'
    elif score < 80:
        strength = 'Strong'
    else:
        strength = 'Very Strong'
    
    # Add positive feedback if strong
    if score >= 80 and not feedback:
        feedback.append("Excellent password!")
    
    return {
        'score': score,
        'strength': strength,
        'entropy': round(entropy, 2),
        'length': length,
        'has_uppercase': has_uppercase,
        'has_lowercase': has_lowercase,
        'has_digits': has_digits,
        'has_special': has_special,
        'is_common': is_common,
        'feedback': feedback if feedback else ['Great password!']
    }


def get_strength_color(score: int) -> str:
    """
    Get color code for password strength (for terminal output).
    
    Args:
        score: Password strength score (0-100)
    
    Returns:
        Color code string for use with colorama
    """
    if score < 20:
        return 'RED'
    elif score < 40:
        return 'LIGHTRED_EX'
    elif score < 60:
        return 'YELLOW'
    elif score < 80:
        return 'LIGHTGREEN_EX'
    else:
        return 'GREEN'


def get_strength_emoji(score: int) -> str:
    """
    Get emoji representation of password strength.
    
    Args:
        score: Password strength score (0-100)
    
    Returns:
        Emoji string
    """
    if score < 20:
        return '🔴'
    elif score < 40:
        return '🟠'
    elif score < 60:
        return '🟡'
    elif score < 80:
        return '🟢'
    else:
        return '🟢🔒'


def format_strength_bar(score: int, width: int = 20) -> str:
    """
    Create a visual progress bar for password strength.
    
    Args:
        score: Password strength score (0-100)
        width: Width of the bar in characters
    
    Returns:
        ASCII progress bar string
    """
    filled = int(width * score / 100)
    empty = width - filled
    
    bar = '█' * filled + '░' * empty
    return f"[{bar}] {score}%"
