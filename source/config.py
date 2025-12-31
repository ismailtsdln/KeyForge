#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration Management Module
Handles loading and managing user preferences and password templates.
"""

import json
from typing import Dict, Any, Optional
from pathlib import Path

# Optional YAML support
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


DEFAULT_CONFIG = {
    'defaults': {
        'length': 16,
        'use_uppercase': True,
        'use_lowercase': True,
        'use_digits': True,
        'use_special': True,
        'passphrase_words': 4,
        'passphrase_separator': '-',
        'passphrase_capitalize': True
    },
    'templates': {
        'web': {
            'length': 16,
            'use_uppercase': True,
            'use_lowercase': True,
            'use_digits': True,
            'use_special': True
        },
        'wifi': {
            'length': 24,
            'use_uppercase': True,
            'use_lowercase': True,
            'use_digits': True,
            'use_special': False
        },
        'pin': {
            'length': 6,
            'use_uppercase': False,
            'use_lowercase': False,
            'use_digits': True,
            'use_special': False,
            'custom_chars': '0123456789'
        },
        'memorable': {
            'passphrase': True,
            'word_count': 4,
            'separator': '-',
            'capitalize': True,
            'include_number': True
        },
        'maximum': {
            'length': 32,
            'use_uppercase': True,
            'use_lowercase': True,
            'use_digits': True,
            'use_special': True
        }
    },
    'output': {
        'show_strength': True,
        'use_colors': True,
        'save_to_history': False
    }
}


class Config:
    """Configuration manager for RPG."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to configuration file (JSON or YAML)
        """
        self.config_file = config_file
        self.config = DEFAULT_CONFIG.copy()
        
        if config_file:
            self.load(config_file)
    
    def load(self, config_file: str) -> bool:
        """
        Load configuration from file.
        
        Args:
            config_file: Path to configuration file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            path = Path(config_file)
            
            if not path.exists():
                print(f"⚠️  Config file not found: {config_file}")
                return False
            
            with open(path, 'r', encoding='utf-8') as f:
                if path.suffix.lower() in ['.yaml', '.yml']:
                    if not HAS_YAML:
                        print("⚠️  YAML support not available. Install PyYAML: pip install PyYAML")
                        return False
                    loaded_config = yaml.safe_load(f)
                elif path.suffix.lower() == '.json':
                    loaded_config = json.load(f)
                else:
                    print(f"⚠️  Unsupported config format: {path.suffix}")
                    return False
            
            # Merge with defaults
            self._merge_config(loaded_config)
            print(f"✓ Configuration loaded from: {config_file}")
            return True
            
        except Exception as e:
            print(f"⚠️  Failed to load config: {e}")
            return False
    
    def _merge_config(self, new_config: Dict[str, Any]) -> None:
        """
        Merge new configuration with existing config.
        
        Args:
            new_config: New configuration dictionary
        """
        for key, value in new_config.items():
            if key in self.config and isinstance(value, dict):
                self.config[key].update(value)
            else:
                self.config[key] = value
    
    def save(self, config_file: Optional[str] = None) -> bool:
        """
        Save current configuration to file.
        
        Args:
            config_file: Path to save config (uses loaded file if not specified)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            file_path = config_file or self.config_file
            
            if not file_path:
                print("⚠️  No config file specified")
                return False
            
            path = Path(file_path)
            
            with open(path, 'w', encoding='utf-8') as f:
                if path.suffix.lower() in ['.yaml', '.yml']:
                    if not HAS_YAML:
                        print("⚠️  YAML support not available. Install PyYAML: pip install PyYAML")
                        return False
                    yaml.dump(self.config, f, default_flow_style=False)
                elif path.suffix.lower() == '.json':
                    json.dump(self.config, f, indent=2)
                else:
                    print(f"⚠️  Unsupported config format: {path.suffix}")
                    return False
            
            print(f"✓ Configuration saved to: {file_path}")
            return True
            
        except Exception as e:
            print(f"⚠️  Failed to save config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'defaults.length')
            default: Default value if key not found
        
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """
        Get password template configuration.
        
        Args:
            template_name: Name of the template
        
        Returns:
            Template configuration or None if not found
        """
        return self.config.get('templates', {}).get(template_name)
    
    def list_templates(self) -> list:
        """
        Get list of available template names.
        
        Returns:
            List of template names
        """
        return list(self.config.get('templates', {}).keys())


def create_example_config(filename: str = 'config.example.yaml') -> bool:
    """
    Create an example configuration file.
    
    Args:
        filename: Output filename
    
    Returns:
        True if successful, False otherwise
    """
    try:
        path = Path(filename)
        
        with open(path, 'w', encoding='utf-8') as f:
            if path.suffix.lower() in ['.yaml', '.yml']:
                if not HAS_YAML:
                    print("⚠️  YAML support not available. Creating JSON config instead...")
                    filename = filename.replace('.yaml', '.json').replace('.yml', '.json')
                    path = Path(filename)
                    json.dump(DEFAULT_CONFIG, f, indent=2)
                else:
                    yaml.dump(DEFAULT_CONFIG, f, default_flow_style=False, sort_keys=False)
            else:
                json.dump(DEFAULT_CONFIG, f, indent=2)
        
        print(f"✓ Example config created: {filename}")
        print(f"  Copy it to 'config.yaml' (or .json) and customize as needed")
        return True
        
    except Exception as e:
        print(f"⚠️  Failed to create example config: {e}")
        return False
