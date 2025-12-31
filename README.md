# KeyForge 🔐

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](https://github.com/ismailtasdelen/Python-Random-Password-Generator)

Modern, secure, and feature-rich password and passphrase generator with CLI and Web interfaces.

## ✨ Features

### 🔒 Security

- **Cryptographically secure** random generation using Python's `secrets` module
- Guaranteed character type inclusion (no weak passwords)
- Entropy calculation and password strength analysis
- Common password detection

### 🎯 Password Generation

- Customizable length (6-128 characters)
- Character type selection (uppercase, lowercase, digits, special)
- Custom character sets
- Multiple password generation
- PIN codes and hex keys

### 📝 Passphrase Generation

- Memorable word-based passphrases
- Customizable word count and separators
- EFF wordlist support
- Optional number inclusion

### 💻 CLI Features

- Beautiful colored terminal output
- Password strength visualization
- Copy to clipboard
- QR code generation
- Export to JSON/CSV/TXT
- Configuration file support
- Password templates (web, wifi, pin, etc.)

### 🌐 Web Interface

- Modern, responsive design
- Dark mode support
- Real-time password generation
- Strength meter with visual feedback
- RESTful API

## 📦 Installation

### Basic Installation

```bash
git clone https://github.com/ismailtsdln/KeyForge.git
cd KeyForge
pip install -e .
```

### Full Installation (Recommended)

```bash
# Install with all features (CLI + Web)
pip install -e .[all]

# Or install specific features
pip install -e .[cli]   # CLI features only
pip install -e .[web]   # Web interface only
```

### Development Installation

```bash
pip install -e .[dev]
```

## 🚀 Usage

### Command Line Interface

#### Basic Usage

```bash
# Generate a 16-character password (default)
rpg

# Generate password with specific length
rpg --length 20

# Generate multiple passwords
rpg --count 5

# Generate without special characters
rpg --no-special
```

#### Passphrase Generation

```bash
# Generate a 4-word passphrase
rpg --passphrase

# Generate 6-word passphrase
rpg --passphrase --words 6

# Custom separator
rpg --passphrase --separator "_"

# Add number to passphrase
rpg --passphrase --add-number
```

#### Utility Features

```bash
# Copy to clipboard
rpg --copy

# Generate QR code
rpg --qrcode

# Export to file
rpg --output passwords.json
rpg --output passwords.csv
rpg --output passwords.txt

# Show password strength
rpg --strength
```

#### Templates

```bash
# Use predefined templates
rpg --template wifi      # 24 chars, no special
rpg --template pin       # 6-digit PIN
rpg --template maximum   # 32 chars, max security

# List available templates
rpg --list-templates
```

#### Special Modes

```bash
# Generate PIN code
rpg --pin 6

# Generate hex key (for API tokens)
rpg --hex 32
```

#### Configuration

```bash
# Create example config
rpg --create-config

# Use custom config
rpg --config my-config.yaml
```

### Web Interface

Start the web server:

```bash
python web/app.py
```

Then open your browser to: `http://localhost:5000`

#### Features

- 🌓 Dark/Light mode toggle
- 🔄 Real-time password generation
- 📊 Password strength visualization
- 📋 One-click copy to clipboard
- 📱 Fully responsive design

### Python API

```python
from source import rpg

# Generate password
password = rpg.generate_password(length=16)

# Generate passphrase
passphrase = rpg.generate_passphrase(word_count=4)

# Generate multiple unique passwords
passwords = rpg.generate_multiple_passwords(count=5, length=20)

# Special functions
pin = rpg.generate_pin(length=6)
hex_key = rpg.generate_hex_key(length=32)

# Password strength analysis
from source.strength import analyze_password_strength
analysis = analyze_password_strength(password)
print(f"Strength: {analysis['strength']}")
print(f"Score: {analysis['score']}/100")
print(f"Entropy: {analysis['entropy']} bits")
```

### REST API

The web application exposes RESTful API endpoints:

#### Generate Password

```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "length": 16,
    "count": 1,
    "use_uppercase": true,
    "use_lowercase": true,
    "use_digits": true,
    "use_special": true
  }'
```

#### Generate Passphrase

```bash
curl -X POST http://localhost:5000/api/passphrase \
  -H "Content-Type: application/json" \
  -d '{
    "word_count": 4,
    "separator": "-",
    "capitalize": true,
    "include_number": false
  }'
```

#### Analyze Password Strength

```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"password": "MyP@ssw0rd123"}'
```

## 📋 Configuration

Create a `config.yaml` file:

```yaml
defaults:
  length: 16
  use_uppercase: true
  use_lowercase: true
  use_digits: true
  use_special: true
  passphrase_words: 4

templates:
  web:
    length: 16
    use_special: true
  wifi:
    length: 24
    use_special: false

output:
  show_strength: true
  use_colors: true
```

## 🧪 Testing

Run tests:

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=source tests/

# Run specific test file
pytest tests/rpg_test.py -v
```

## 📁 Project Structure

```
Python-Random-Password-Generator/
├── source/
│   ├── rpg.py          # Core password generation
│   ├── cli.py          # Command-line interface
│   ├── strength.py     # Password strength analyzer
│   ├── utils.py        # Utility functions
│   ├── wordlist.py     # EFF wordlist for passphrases
│   └── config.py       # Configuration management
├── web/
│   ├── app.py          # Flask application
│   ├── templates/
│   │   └── index.html  # Web interface
│   └── static/
│       ├── css/
│       │   └── styles.css
│       └── js/
│           └── app.js
├── tests/
│   └── rpg_test.py     # Unit tests
├── run.py              # Legacy runner
├── setup.py            # Package setup
├── requirements.txt    # Dependencies
└── README.md           # This file
```

## 🔄 Changelog

### Version 2.0.0 (2026-01-01)

- ✨ **New**: Cryptographically secure password generation using `secrets`
- ✨ **New**: Modern CLI interface with argparse
- ✨ **New**: Passphrase generation with EFF wordlist
- ✨ **New**: Password strength analyzer
- ✨ **New**: QR code generation
- ✨ **New**: Clipboard support
- ✨ **New**: File export (JSON/CSV/TXT)
- ✨ **New**: Configuration file support
- ✨ **New**: Password templates
- ✨ **New**: Web interface with Flask
- ✨ **New**: RESTful API
- ✨ **New**: Dark mode support
- 🐛 **Fixed**: Password length bug (was generating random length 8-20)
- 🔒 **Security**: Replaced `random` with `secrets` module
- ✅ **Tests**: Comprehensive test suite
- 📚 **Docs**: Complete documentation with examples

### Version 0.1 (Original)

- Basic password generation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**İsmail Taşdelen**

- 📧 Email: <pentestdatabase@gmail.com>
- 🔗 LinkedIn: [ismailtasdelen](https://www.linkedin.com/in/ismailtasdelen)
- 🐙 GitHub: [@ismailtasdelen](https://github.com/ismailtasdelen)

## 🙏 Acknowledgments

- [EFF Wordlist](https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases) for memorable passphrases
- Python `secrets` module for cryptographically secure random generation
- All contributors and users of this project

## ⚠️ Security Notice

This tool generates passwords using Python's `secrets` module, which is designed for generating cryptographically strong random numbers suitable for managing secrets such as passwords. However, the security of generated passwords also depends on:

- Using sufficient password length (16+ characters recommended)
- Enabling multiple character types
- Not sharing passwords
- Using unique passwords for each service
- Storing passwords securely (password manager)

---

**Made with ❤️ by İsmail Taşdelen**
