"""
Python Random Password Generator (RPG)
Secure password and passphrase generation.

Version: 2.0.0
Author: İsmail Taşdelen
"""

from source.rpg import (
    generate_password,
    generate_passphrase,
    generate_multiple_passwords,
    generate_pin,
    generate_hex_key,
    random_password_generator,
    random_password_generator_ico
)

__version__ = '2.0.0'
__author__ = 'İsmail Taşdelen'
__email__ = 'pentestdatabase@gmail.com'

__all__ = [
    'generate_password',
    'generate_passphrase',
    'generate_multiple_passwords',
    'generate_pin',
    'generate_hex_key',
    'random_password_generator',
    'random_password_generator_ico',
]
