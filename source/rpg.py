#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python Random Password Generator (RPG) - Core Module
Secure password and passphrase generation using cryptographically safe methods.

Author: İSMAİL TAŞDELEN
Email: pentestdatabase@gmail.com
LinkedIn: https://www.linkedin.com/in/ismailtasdelen
Version: 2.0.0
"""

import secrets
import string
from typing import List, Optional, Set


def generate_password(
    length: int = 16,
    use_uppercase: bool = True,
    use_lowercase: bool = True,
    use_digits: bool = True,
    use_special: bool = True,
    custom_chars: Optional[str] = None
) -> str:
    """
    Generate a cryptographically secure random password.
    
    Args:
        length: Length of the password (default: 16)
        use_uppercase: Include uppercase letters (default: True)
        use_lowercase: Include lowercase letters (default: True)
        use_digits: Include digits (default: True)
        use_special: Include special characters (default: True)
        custom_chars: Custom character set to use (overrides other options)
    
    Returns:
        A randomly generated password string
        
    Raises:
        ValueError: If length < 1 or no character types are selected
        
    Examples:
        >>> pwd = generate_password(12)
        >>> len(pwd)
        12
        >>> pwd = generate_password(16, use_special=False)
        >>> any(c in string.punctuation for c in pwd)
        False
    """
    if length < 1:
        raise ValueError("Password length must be at least 1")
    
    # Use custom characters if provided
    if custom_chars:
        if not custom_chars:
            raise ValueError("Custom character set cannot be empty")
        return ''.join(secrets.choice(custom_chars) for _ in range(length))
    
    # Build character set based on options
    charset = ""
    if use_uppercase:
        charset += string.ascii_uppercase
    if use_lowercase:
        charset += string.ascii_lowercase
    if use_digits:
        charset += string.digits
    if use_special:
        charset += string.punctuation
    
    if not charset:
        raise ValueError("At least one character type must be enabled")
    
    # Generate password ensuring at least one character from each enabled type
    password = []
    
    # Ensure at least one character from each enabled type
    if use_uppercase:
        password.append(secrets.choice(string.ascii_uppercase))
    if use_lowercase:
        password.append(secrets.choice(string.ascii_lowercase))
    if use_digits:
        password.append(secrets.choice(string.digits))
    if use_special:
        password.append(secrets.choice(string.punctuation))
    
    # Fill the rest randomly
    remaining_length = length - len(password)
    if remaining_length > 0:
        password.extend(secrets.choice(charset) for _ in range(remaining_length))
    
    # Shuffle to avoid predictable patterns
    password_list = list(password)
    for i in range(len(password_list) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_list[i], password_list[j] = password_list[j], password_list[i]
    
    return ''.join(password_list[:length])


def generate_multiple_passwords(
    count: int = 1,
    length: int = 16,
    **kwargs
) -> List[str]:
    """
    Generate multiple unique passwords.
    
    Args:
        count: Number of passwords to generate
        length: Length of each password
        **kwargs: Additional arguments passed to generate_password()
    
    Returns:
        List of unique password strings
        
    Raises:
        ValueError: If count < 1
    """
    if count < 1:
        raise ValueError("Count must be at least 1")
    
    passwords: Set[str] = set()
    while len(passwords) < count:
        passwords.add(generate_password(length=length, **kwargs))
    
    return list(passwords)


def generate_passphrase(
    word_count: int = 4,
    separator: str = "-",
    capitalize: bool = True,
    include_number: bool = False
) -> str:
    """
    Generate a memorable passphrase using random words.
    
    Args:
        word_count: Number of words in the passphrase (default: 4)
        separator: Character(s) to separate words (default: "-")
        capitalize: Capitalize first letter of each word (default: True)
        include_number: Append a random number at the end (default: False)
    
    Returns:
        A randomly generated passphrase
        
    Raises:
        ValueError: If word_count < 1
        
    Examples:
        >>> phrase = generate_passphrase(4)
        >>> len(phrase.split('-'))
        4
    """
    if word_count < 1:
        raise ValueError("Word count must be at least 1")
    
    # Import wordlist here to avoid circular dependency
    from source.wordlist import get_random_words
    
    words = get_random_words(word_count)
    
    if capitalize:
        words = [word.capitalize() for word in words]
    
    passphrase = separator.join(words)
    
    if include_number:
        random_number = secrets.randbelow(100)
        passphrase += f"{separator}{random_number}"
    
    return passphrase


def random_password_generator() -> str:
    """
    Legacy function for backward compatibility.
    Generates a random password of length 12 (fixed from original bug).
    
    Returns:
        A randomly generated password string
        
    Deprecated:
        Use generate_password() instead for more options and security.
    """
    # Fixed bug: original used range(size, 20) which gave random length 8-20
    # Now generates fixed length of 12 for consistency
    return generate_password(length=12, use_special=False)


def random_password_generator_ico() -> None:
    """
    Display the RPG banner/logo.
    Legacy function for backward compatibility.
    """
    banner = """
    #############################################################
    # PYTHON - Random Password Generator (RPG) v2.0            #
    #############################################################
    #                    SECURE & MODERN                        #
    #############################################################
    #               DEVELOPER : İSMAİL TAŞDELEN                 #
    #          Mail Address : pentestdatabase@gmail.com         #
    #   LINKEDIN : https://www.linkedin.com/in/ismailtasdelen   #
    #############################################################
    """
    print(banner)


# Convenience function for CLI
def generate_pin(length: int = 4) -> str:
    """
    Generate a numeric PIN code.
    
    Args:
        length: Length of the PIN (default: 4)
    
    Returns:
        A randomly generated PIN string
    """
    return ''.join(secrets.choice(string.digits) for _ in range(length))


def generate_hex_key(length: int = 32) -> str:
    """
    Generate a hexadecimal key (useful for API keys, tokens).
    
    Args:
        length: Length of the hex key (default: 32)
    
    Returns:
        A randomly generated hex string
    """
    return secrets.token_hex(length // 2)
