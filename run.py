#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Legacy runner for backward compatibility.
For new features, use: rpg --help
"""

import os
from source import rpg

# Running (legacy mode - maintains compatibility)
rpg.random_password_generator_ico()
password = rpg.random_password_generator()
print("Password : " + password)

# Hint for new features
print("\n" + "="*60)
print("💡 TIP: For more features, install and use the new CLI:")
print("   $ pip install -e .[all]")
print("   $ rpg --help")
print("="*60)

