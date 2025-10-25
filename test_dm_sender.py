#!/usr/bin/env python3
"""
Test script for dm_sender.py
Tests JSON loading and message formatting without GUI automation
"""

import json
import sys
from pathlib import Path

def test_json_loading():
    """Test loading and parsing JSON user data."""
    print("Testing JSON loading...")
    
    test_file = Path("users_example.json")
    if not test_file.exists():
        print(f"❌ Test file {test_file} not found")
        return False
    
    try:
        with open(test_file, 'r') as f:
            users = json.load(f)
        
        if not isinstance(users, list):
            print("❌ JSON should contain a list of users")
            return False
        
        print(f"✓ Successfully loaded {len(users)} users")
        
        # Validate user structure
        for i, user in enumerate(users):
            if 'name' not in user:
                print(f"❌ User at index {i} missing required 'name' field")
                return False
            print(f"  - User {i+1}: {user.get('name')} ({user.get('display_name', 'N/A')})")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_message_formatting():
    """Test message template formatting."""
    print("\nTesting message formatting...")
    
    test_user = {
        "id": 123456789,
        "name": "testuser",
        "display_name": "Test User"
    }
    
    templates = [
        ("Hello {name}!", "Hello testuser!"),
        ("Hi {display_name}", "Hi Test User"),
        ("Your ID: {id}", "Your ID: 123456789"),
        ("Hey {name}, you're {display_name}!", "Hey testuser, you're Test User!")
    ]
    
    for template, expected in templates:
        result = template.replace('{name}', test_user['name'])
        result = result.replace('{display_name}', test_user['display_name'])
        result = result.replace('{id}', str(test_user['id']))
        
        if result == expected:
            print(f"✓ Template: '{template}' -> '{result}'")
        else:
            print(f"❌ Template: '{template}'")
            print(f"   Expected: '{expected}'")
            print(f"   Got: '{result}'")
            return False
    
    # Test multiline message
    multiline_template = "Hello {name}!\n\nWelcome to our server!"
    multiline_expected = "Hello testuser!\n\nWelcome to our server!"
    multiline_result = multiline_template.replace('{name}', test_user['name'])
    
    if multiline_result == multiline_expected:
        print(f"✓ Multiline template: '{multiline_template[:20]}...' -> '{multiline_result[:20]}...'")
    else:
        print(f"❌ Multiline template failed")
        return False
    
    return True


def test_config_loading():
    """Test config.json loading."""
    print("\nTesting config loading...")
    
    config_file = Path("config.json")
    if not config_file.exists():
        print(f"⚠️  Config file {config_file} not found (optional)")
        return True
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        print(f"✓ Successfully loaded config")
        
        if 'settings' in config:
            print(f"  - Default delay: {config['settings'].get('default_delay', 'N/A')}s")
        
        if 'message_templates' in config:
            print(f"  - Message templates: {len(config['message_templates'])} available")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in config: {e}")
        return False
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return False


def test_message_file_loading():
    """Test loading messages from a file."""
    print("\nTesting message file loading...")
    
    message_file = Path("message_example.txt")
    if not message_file.exists():
        print(f"⚠️  Message file {message_file} not found (optional)")
        return True
    
    try:
        with open(message_file, 'r', encoding='utf-8') as f:
            message = f.read()
        
        if not message:
            print(f"❌ Message file is empty")
            return False
        
        # Check if message contains expected content
        if len(message) > 0:
            print(f"✓ Successfully loaded message from file")
            print(f"  - Message length: {len(message)} characters")
            print(f"  - Lines: {len(message.splitlines())} lines")
            
            # Preview first line
            first_line = message.split('\n')[0]
            print(f"  - First line: {first_line[:50]}{'...' if len(first_line) > 50 else ''}")
            return True
        else:
            print(f"❌ Message file appears to be empty")
            return False
        
    except Exception as e:
        print(f"❌ Error loading message file: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("DM Sender Tests")
    print("=" * 60)
    print()
    
    tests = [
        ("JSON Loading", test_json_loading),
        ("Message Formatting", test_message_formatting),
        ("Config Loading", test_config_loading),
        ("Message File Loading", test_message_file_loading)
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print()
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result for _, result in results)
    
    print()
    if all_passed:
        print("✓ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
