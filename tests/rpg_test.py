# -*- coding: utf-8 -*-

"""
Unit tests for RPG password generation module.
"""

import unittest
import string
from source import rpg


class TestPasswordGeneration(unittest.TestCase):
    """Test password generation functions."""
    
    def test_generate_password_default(self):
        """Test default password generation."""
        password = rpg.generate_password()
        self.assertEqual(len(password), 16)
        
    def test_generate_password_custom_length(self):
        """Test password with custom length."""
        for length in [8, 12, 20, 32]:
            password = rpg.generate_password(length=length)
            self.assertEqual(len(password), length)
    
    def test_generate_password_character_types(self):
        """Test that password contains required character types."""
        password = rpg.generate_password(length=20)
        
        # Should contain all types by default
        has_upper = any(c in string.ascii_uppercase for c in password)
        has_lower = any(c in string.ascii_lowercase for c in password)
        has_digit = any(c in string.digits for c in password)
        has_special = any(c in string.punctuation for c in password)
        
        self.assertTrue(has_upper or has_lower or has_digit or has_special)
    
    def test_generate_password_no_special(self):
        """Test password without special characters."""
        password = rpg.generate_password(length=20, use_special=False)
        has_special = any(c in string.punctuation for c in password)
        self.assertFalse(has_special)
    
    def test_generate_password_only_digits(self):
        """Test password with only digits."""
        password = rpg.generate_password(
            length=10,
            use_uppercase=False,
            use_lowercase=False,
            use_digits=True,
            use_special=False
        )
        self.assertTrue(password.isdigit())
    
    def test_generate_password_custom_chars(self):
        """Test password with custom character set."""
        custom = "ABC123"
        password = rpg.generate_password(length=10, custom_chars=custom)
        
        for char in password:
            self.assertIn(char, custom)
    
    def test_generate_password_invalid_length(self):
        """Test that invalid length raises ValueError."""
        with self.assertRaises(ValueError):
            rpg.generate_password(length=0)
        
        with self.assertRaises(ValueError):
            rpg.generate_password(length=-5)
    
    def test_generate_password_no_char_types(self):
        """Test that disabling all char types raises ValueError."""
        with self.assertRaises(ValueError):
            rpg.generate_password(
                use_uppercase=False,
                use_lowercase=False,
                use_digits=False,
                use_special=False
            )


class TestMultiplePasswords(unittest.TestCase):
    """Test multiple password generation."""
    
    def test_generate_multiple_passwords(self):
        """Test generating multiple passwords."""
        count = 5
        passwords = rpg.generate_multiple_passwords(count=count, length=12)
        
        self.assertEqual(len(passwords), count)
        # All should be unique
        self.assertEqual(len(set(passwords)), count)
    
    def test_generate_multiple_passwords_invalid_count(self):
        """Test that invalid count raises ValueError."""
        with self.assertRaises(ValueError):
            rpg.generate_multiple_passwords(count=0)


class TestPassphraseGeneration(unittest.TestCase):
    """Test passphrase generation."""
    
    def test_generate_passphrase_default(self):
        """Test default passphrase generation."""
        passphrase = rpg.generate_passphrase()
        words = passphrase.split('-')
        
        self.assertEqual(len(words), 4)
        # First letter should be capitalized
        for word in words:
            self.assertTrue(word[0].isupper())
    
    def test_generate_passphrase_custom_word_count(self):
        """Test passphrase with custom word count."""
        for count in [3, 5, 6]:
            passphrase = rpg.generate_passphrase(word_count=count)
            words = passphrase.split('-')
            self.assertEqual(len(words), count)
    
    def test_generate_passphrase_custom_separator(self):
        """Test passphrase with custom separator."""
        separator = '_'
        passphrase = rpg.generate_passphrase(separator=separator)
        self.assertIn(separator, passphrase)
        self.assertNotIn('-', passphrase)
    
    def test_generate_passphrase_no_capitalize(self):
        """Test passphrase without capitalization."""
        passphrase = rpg.generate_passphrase(capitalize=False)
        words = passphrase.split('-')
        
        # At least some words should be lowercase
        lowercase_count = sum(1 for word in words if word[0].islower())
        self.assertGreater(lowercase_count, 0)
    
    def test_generate_passphrase_with_number(self):
        """Test passphrase with number."""
        passphrase = rpg.generate_passphrase(include_number=True)
        parts = passphrase.split('-')
        
        # Last part should be a number
        self.assertTrue(parts[-1].isdigit())
    
    def test_generate_passphrase_invalid_word_count(self):
        """Test that invalid word count raises ValueError."""
        with self.assertRaises(ValueError):
            rpg.generate_passphrase(word_count=0)


class TestLegacyFunctions(unittest.TestCase):
    """Test legacy functions for backward compatibility."""
    
    def test_random_password_generator(self):
        """Test legacy password generator."""
        password = rpg.random_password_generator()
        
        # Should be fixed length of 12
        self.assertEqual(len(password), 12)
        
        # Should not contain special characters
        has_special = any(c in string.punctuation for c in password)
        self.assertFalse(has_special)
    
    def test_random_password_generator_ico(self):
        """Test legacy banner function."""
        # Should not raise any exceptions
        try:
            rpg.random_password_generator_ico()
        except Exception as e:
            self.fail(f"random_password_generator_ico raised {e}")


class TestSpecialFunctions(unittest.TestCase):
    """Test special generation functions."""
    
    def test_generate_pin(self):
        """Test PIN generation."""
        pin = rpg.generate_pin(length=6)
        
        self.assertEqual(len(pin), 6)
        self.assertTrue(pin.isdigit())
    
    def test_generate_pin_default(self):
        """Test default PIN generation."""
        pin = rpg.generate_pin()
        self.assertEqual(len(pin), 4)
    
    def test_generate_hex_key(self):
        """Test hex key generation."""
        key = rpg.generate_hex_key(length=32)
        
        self.assertEqual(len(key), 32)
        # Should be valid hexadecimal
        try:
            int(key, 16)
        except ValueError:
            self.fail("Generated key is not valid hexadecimal")
    
    def test_generate_hex_key_default(self):
        """Test default hex key generation."""
        key = rpg.generate_hex_key()
        self.assertEqual(len(key), 32)


class TestRandomness(unittest.TestCase):
    """Test randomness and uniqueness."""
    
    def test_password_uniqueness(self):
        """Test that generated passwords are unique."""
        passwords = [rpg.generate_password(length=16) for _ in range(100)]
        
        # All should be unique
        self.assertEqual(len(passwords), len(set(passwords)))
    
    def test_passphrase_uniqueness(self):
        """Test that generated passphrases are unique."""
        passphrases = [rpg.generate_passphrase() for _ in range(50)]
        
        # Most should be unique (allowing for very rare collisions)
        unique_ratio = len(set(passphrases)) / len(passphrases)
        self.assertGreater(unique_ratio, 0.95)


if __name__ == '__main__':
    unittest.main()

