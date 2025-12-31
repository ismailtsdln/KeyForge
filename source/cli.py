#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Command-Line Interface for RPG
Modern argparse-based CLI with rich features.
"""

import sys
import argparse
from typing import Optional

# Conditional imports for optional dependencies
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False
    # Fallback no-op definitions
    class Fore:
        RED = YELLOW = GREEN = CYAN = MAGENTA = WHITE = LIGHTRED_EX = LIGHTGREEN_EX = ''
    class Style:
        BRIGHT = RESET_ALL = DIM = ''

from source import rpg
from source.strength import analyze_password_strength, format_strength_bar, get_strength_emoji
from source.utils import (
    copy_to_clipboard, generate_qr_code, export_passwords,
    save_to_history
)
from source.config import Config


def print_colored(text: str, color: str = '', style: str = '') -> None:
    """Print colored text if colorama is available."""
    if HAS_COLORAMA:
        color_code = getattr(Fore, color.upper(), '')
        style_code = getattr(Style, style.upper(), '')
        print(f"{style_code}{color_code}{text}{Style.RESET_ALL}")
    else:
        print(text)


def print_banner() -> None:
    """Print RPG banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║     🔐 Random Password Generator (RPG) v2.0 🔐            ║
    ║                  Secure & Modern                          ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print_colored(banner, 'CYAN', 'BRIGHT')


def print_password(password: str, show_strength: bool = True) -> None:
    """
    Print password with optional strength analysis.
    
    Args:
        password: Password to print
        show_strength: Whether to show strength analysis
    """
    print_colored("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 'CYAN')
    print_colored(f"  Password: {password}", 'GREEN', 'BRIGHT')
    print_colored("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n", 'CYAN')
    
    if show_strength:
        analysis = analyze_password_strength(password)
        
        # Determine color based on score
        if analysis['score'] < 40:
            strength_color = 'LIGHTRED_EX'
        elif analysis['score'] < 70:
            strength_color = 'YELLOW'
        else:
            strength_color = 'LIGHTGREEN_EX'
        
        emoji = get_strength_emoji(analysis['score'])
        
        print_colored(f"  {emoji} Strength: {analysis['strength']}", strength_color, 'BRIGHT')
        print(f"  {format_strength_bar(analysis['score'])}")
        print(f"  Length: {analysis['length']} | Entropy: {analysis['entropy']} bits")
        
        # Character composition
        chars = []
        if analysis['has_uppercase']:
            chars.append("ABC")
        if analysis['has_lowercase']:
            chars.append("abc")
        if analysis['has_digits']:
            chars.append("123")
        if analysis['has_special']:
            chars.append("!@#")
        print(f"  Characters: {' + '.join(chars)}")
        
        # Feedback
        if analysis['feedback']:
            print_colored("\n  💡 Suggestions:", 'YELLOW')
            for feedback in analysis['feedback']:
                print(f"     • {feedback}")
        
        print()


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='🔐 Random Password Generator - Secure password and passphrase generation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  rpg                              Generate a 16-character password
  rpg -l 20 -c 5                  Generate 5 passwords of length 20
  rpg --no-special                Generate without special characters
  rpg --passphrase                Generate a memorable passphrase
  rpg --passphrase -w 6           Generate 6-word passphrase
  rpg -C                          Generate and copy to clipboard
  rpg --qrcode                    Generate with QR code
  rpg -o passwords.json           Export to JSON file
  rpg --template wifi             Use WiFi template (24 chars, no special)
  rpg --config my-config.yaml     Use custom configuration

Templates:
  web      - 16 chars, all types (default web password)
  wifi     - 24 chars, no special (WiFi password)
  pin      - 6 digits (PIN code)
  memorable - 4-word passphrase with number
  maximum  - 32 chars, maximum security
        """
    )
    
    # Password options
    pwd_group = parser.add_argument_group('password options')
    pwd_group.add_argument('-l', '--length', type=int, default=16,
                          help='Password length (default: 16)')
    pwd_group.add_argument('-c', '--count', type=int, default=1,
                          help='Number of passwords to generate (default: 1)')
    pwd_group.add_argument('--no-uppercase', action='store_true',
                          help='Exclude uppercase letters')
    pwd_group.add_argument('--no-lowercase', action='store_true',
                          help='Exclude lowercase letters')
    pwd_group.add_argument('--no-digits', action='store_true',
                          help='Exclude digits')
    pwd_group.add_argument('--no-special', action='store_true',
                          help='Exclude special characters')
    pwd_group.add_argument('--custom-chars', type=str,
                          help='Custom character set to use')
    
    # Passphrase options
    phrase_group = parser.add_argument_group('passphrase options')
    phrase_group.add_argument('-p', '--passphrase', action='store_true',
                            help='Generate passphrase instead of password')
    phrase_group.add_argument('-w', '--words', type=int, default=4,
                            help='Number of words in passphrase (default: 4)')
    phrase_group.add_argument('--separator', type=str, default='-',
                            help='Word separator (default: -)')
    phrase_group.add_argument('--no-capitalize', action='store_true',
                            help='Don\'t capitalize words')
    phrase_group.add_argument('--add-number', action='store_true',
                            help='Add number to passphrase')
    
    # Utility options
    util_group = parser.add_argument_group('utility options')
    util_group.add_argument('-C', '--copy', action='store_true',
                          help='Copy to clipboard')
    util_group.add_argument('-q', '--qrcode', action='store_true',
                          help='Generate QR code')
    util_group.add_argument('--qr-file', type=str,
                          help='Save QR code to file (e.g., qr.png)')
    util_group.add_argument('-s', '--strength', action='store_true', default=True,
                          help='Show password strength (default: enabled)')
    util_group.add_argument('--no-strength', action='store_true',
                          help='Hide password strength analysis')
    util_group.add_argument('-o', '--output', type=str,
                          help='Export to file (.json, .csv, .txt)')
    
    # Template and config
    template_group = parser.add_argument_group('template and configuration')
    template_group.add_argument('-t', '--template', type=str,
                              help='Use password template (web, wifi, pin, memorable, maximum)')
    template_group.add_argument('--config', type=str,
                              help='Load configuration from file')
    template_group.add_argument('--list-templates', action='store_true',
                              help='List available templates')
    template_group.add_argument('--create-config', type=str, nargs='?', const='config.example.yaml',
                              help='Create example config file')
    
    # Special modes
    special_group = parser.add_argument_group('special modes')
    special_group.add_argument('--pin', type=int, nargs='?', const=4,
                             help='Generate numeric PIN (default: 4 digits)')
    special_group.add_argument('--hex', type=int, nargs='?', const=32,
                             help='Generate hex key (default: 32 chars)')
    
    # Display options
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    parser.add_argument('--no-banner', action='store_true',
                       help='Don\'t show banner')
    parser.add_argument('--version', action='version', version='RPG 2.0.0')
    
    args = parser.parse_args()
    
    # Show banner unless disabled
    if not args.no_banner:
        print_banner()
    
    # Load configuration
    config = Config(args.config) if args.config else Config()
    
    # Handle special commands
    if args.create_config:
        from source.config import create_example_config
        create_example_config(args.create_config)
        return 0
    
    if args.list_templates:
        print_colored("📋 Available Templates:\n", 'CYAN', 'BRIGHT')
        for name in config.list_templates():
            template = config.get_template(name)
            print_colored(f"  • {name}", 'GREEN', 'BRIGHT')
            if template:
                for key, value in template.items():
                    print(f"      {key}: {value}")
        return 0
    
    # Handle special modes
    if args.pin is not None:
        password = rpg.generate_pin(args.pin)
        print_colored(f"\n  PIN Code: {password}", 'GREEN', 'BRIGHT')
        if args.copy:
            copy_to_clipboard(password)
            print_colored("  ✓ Copied to clipboard", 'GREEN')
        return 0
    
    if args.hex is not None:
        password = rpg.generate_hex_key(args.hex)
        print_colored(f"\n  Hex Key: {password}", 'GREEN', 'BRIGHT')
        if args.copy:
            copy_to_clipboard(password)
            print_colored("  ✓ Copied to clipboard", 'GREEN')
        return 0
    
    # Apply template if specified
    if args.template:
        template = config.get_template(args.template)
        if not template:
            print_colored(f"⚠️  Unknown template: {args.template}", 'RED')
            print(f"   Use --list-templates to see available templates")
            return 1
        
        # Apply template settings (command line args override template)
        if 'passphrase' in template and template['passphrase']:
            args.passphrase = True
            args.words = template.get('word_count', args.words)
            args.separator = template.get('separator', args.separator)
        else:
            if 'length' in template:
                args.length = template['length']
            if 'custom_chars' in template:
                args.custom_chars = template['custom_chars']
    
    # Generate passwords
    passwords = []
    
    try:
        for i in range(args.count):
            if args.passphrase:
                password = rpg.generate_passphrase(
                    word_count=args.words,
                    separator=args.separator,
                    capitalize=not args.no_capitalize,
                    include_number=args.add_number
                )
            else:
                password = rpg.generate_password(
                    length=args.length,
                    use_uppercase=not args.no_uppercase,
                    use_lowercase=not args.no_lowercase,
                    use_digits=not args.no_digits,
                    use_special=not args.no_special,
                    custom_chars=args.custom_chars
                )
            
            passwords.append(password)
            
            # Print password
            show_strength = args.strength and not args.no_strength
            if args.count == 1:
                print_password(password, show_strength)
            else:
                # Multiple passwords - simpler output
                if show_strength:
                    analysis = analyze_password_strength(password)
                    emoji = get_strength_emoji(analysis['score'])
                    print(f"  {i+1}. {password} {emoji} ({analysis['strength']})")
                else:
                    print(f"  {i+1}. {password}")
        
        # Copy to clipboard (first password if multiple)
        if args.copy and passwords:
            if copy_to_clipboard(passwords[0]):
                print_colored("\n  ✓ Copied to clipboard", 'GREEN')
        
        # Generate QR code (first password if multiple)
        if args.qrcode and passwords:
            qr_file = args.qr_file if args.qr_file else None
            if generate_qr_code(passwords[0], qr_file):
                if not qr_file:
                    print_colored("\n  ✓ QR code generated above", 'GREEN')
        
        # Export to file
        if args.output and passwords:
            export_passwords(passwords, args.output)
        
        # Save to history
        if config.get('output.save_to_history', False):
            for pwd in passwords:
                save_to_history(pwd)
        
        return 0
        
    except ValueError as e:
        print_colored(f"❌ Error: {e}", 'RED')
        return 1
    except KeyboardInterrupt:
        print_colored("\n\n⚠️  Interrupted by user", 'YELLOW')
        return 130
    except Exception as e:
        print_colored(f"❌ Unexpected error: {e}", 'RED')
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
