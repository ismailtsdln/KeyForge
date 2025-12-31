#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Flask Web Application for RPG
Modern web interface for password generation.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from source import rpg
from source.strength import analyze_password_strength
from source.wordlist import get_wordlist_size, calculate_passphrase_entropy

app = Flask(__name__)
CORS(app)  # Enable CORS for API access

# Configuration
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def api_generate():
    """
    Generate password(s) via API.
    
    Request JSON:
        {
            "length": 16,
            "count": 1,
            "use_uppercase": true,
            "use_lowercase": true,
            "use_digits": true,
            "use_special": true,
            "custom_chars": null
        }
    
    Response JSON:
        {
            "success": true,
            "passwords": ["..."],
            "count": 1
        }
    """
    try:
        data = request.get_json() or {}
        
        length = data.get('length', 16)
        count = data.get('count', 1)
        use_uppercase = data.get('use_uppercase', True)
        use_lowercase = data.get('use_lowercase', True)
        use_digits = data.get('use_digits', True)
        use_special = data.get('use_special', True)
        custom_chars = data.get('custom_chars', None)
        
        # Validate inputs
        if length < 1 or length > 128:
            return jsonify({
                'success': False,
                'error': 'Length must be between 1 and 128'
            }), 400
        
        if count < 1 or count > 100:
            return jsonify({
                'success': False,
                'error': 'Count must be between 1 and 100'
            }), 400
        
        # Generate passwords
        passwords = rpg.generate_multiple_passwords(
            count=count,
            length=length,
            use_uppercase=use_uppercase,
            use_lowercase=use_lowercase,
            use_digits=use_digits,
            use_special=use_special,
            custom_chars=custom_chars
        )
        
        return jsonify({
            'success': True,
            'passwords': passwords,
            'count': len(passwords)
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500


@app.route('/api/passphrase', methods=['POST'])
def api_passphrase():
    """
    Generate passphrase via API.
    
    Request JSON:
        {
            "word_count": 4,
            "separator": "-",
            "capitalize": true,
            "include_number": false
        }
    
    Response JSON:
        {
            "success": true,
            "passphrase": "Word-Word-Word-Word",
            "entropy": 51.7
        }
    """
    try:
        data = request.get_json() or {}
        
        word_count = data.get('word_count', 4)
        separator = data.get('separator', '-')
        capitalize = data.get('capitalize', True)
        include_number = data.get('include_number', False)
        
        # Validate inputs
        if word_count < 1 or word_count > 20:
            return jsonify({
                'success': False,
                'error': 'Word count must be between 1 and 20'
            }), 400
        
        # Generate passphrase
        passphrase = rpg.generate_passphrase(
            word_count=word_count,
            separator=separator,
            capitalize=capitalize,
            include_number=include_number
        )
        
        # Calculate entropy
        entropy = calculate_passphrase_entropy(word_count)
        
        return jsonify({
            'success': True,
            'passphrase': passphrase,
            'entropy': round(entropy, 2)
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """
    Analyze password strength via API.
    
    Request JSON:
        {
            "password": "MyP@ssw0rd123"
        }
    
    Response JSON:
        {
            "success": true,
            "analysis": {...}
        }
    """
    try:
        data = request.get_json() or {}
        password = data.get('password', '')
        
        if not password:
            return jsonify({
                'success': False,
                'error': 'Password is required'
            }), 400
        
        analysis = analyze_password_strength(password)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500


@app.route('/api/info', methods=['GET'])
def api_info():
    """
    Get API information.
    
    Response JSON:
        {
            "name": "RPG API",
            "version": "2.0.0",
            "wordlist_size": 500
        }
    """
    return jsonify({
        'name': 'RPG API',
        'version': '2.0.0',
        'wordlist_size': get_wordlist_size(),
        'endpoints': {
            'POST /api/generate': 'Generate passwords',
            'POST /api/passphrase': 'Generate passphrases',
            'POST /api/analyze': 'Analyze password strength',
            'GET /api/info': 'API information'
        }
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║     🔐 RPG Web Server v2.0 🔐                            ║
    ║                                                           ║
    ║     Server running at: http://localhost:5000             ║
    ║     Press Ctrl+C to stop                                 ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
