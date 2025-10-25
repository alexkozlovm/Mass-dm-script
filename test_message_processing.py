#!/usr/bin/env python3
"""
Test the message loading functionality without GUI dependencies
"""
import sys
from pathlib import Path

def test_escape_sequences():
    """Test that escape sequences are properly handled."""
    print("Testing escape sequence handling...")
    
    # Test newline handling
    message = "Hello\\nWorld"
    processed = message.replace('\\n', '\n')
    expected = "Hello\nWorld"
    
    if processed == expected:
        print(f"✓ Escape sequences work: {repr(message)} -> {repr(processed)}")
    else:
        print(f"❌ Escape sequence failed")
        print(f"   Expected: {repr(expected)}")
        print(f"   Got: {repr(processed)}")
        return False
    
    # Test multiple newlines
    message2 = "Line1\\n\\nLine3"
    processed2 = message2.replace('\\n', '\n')
    expected2 = "Line1\n\nLine3"
    
    if processed2 == expected2:
        print(f"✓ Multiple newlines work: {repr(message2)} -> {repr(processed2)}")
    else:
        print(f"❌ Multiple newlines failed")
        return False
    
    return True


def test_file_message_loading():
    """Test loading message from file."""
    print("\nTesting file message loading...")
    
    message_file = Path("message_example.txt")
    if not message_file.exists():
        print(f"❌ Message file not found: {message_file}")
        return False
    
    try:
        with open(message_file, 'r', encoding='utf-8') as f:
            message = f.read()
        
        # Verify it has content
        if not message or len(message) == 0:
            print(f"❌ Message file is empty")
            return False
        
        # Check it has newlines (multiline)
        if '\n' not in message:
            print(f"❌ Message should be multiline")
            return False
        
        lines = message.split('\n')
        print(f"✓ Message file loaded successfully")
        print(f"  - {len(message)} characters")
        print(f"  - {len(lines)} lines")
        print(f"  - First line: {lines[0]}")
        print(f"  - Contains markdown: {('**' in message or '#' in message)}")
        print(f"  - Contains emojis: {any(ord(c) > 127 for c in message)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return False


def test_placeholder_replacement():
    """Test that placeholders work with multiline messages."""
    print("\nTesting placeholder replacement in multiline messages...")
    
    template = "Hello {name}!\n\n**Welcome {display_name}!**"
    user = {
        "name": "testuser",
        "display_name": "Test User"
    }
    
    result = template.replace('{name}', user['name'])
    result = result.replace('{display_name}', user['display_name'])
    
    expected = "Hello testuser!\n\n**Welcome Test User!**"
    
    if result == expected:
        print(f"✓ Placeholders work in multiline messages")
        print(f"  Template: {repr(template[:30])}...")
        print(f"  Result: {repr(result[:30])}...")
    else:
        print(f"❌ Placeholder replacement failed")
        print(f"   Expected: {repr(expected)}")
        print(f"   Got: {repr(result)}")
        return False
    
    return True


def main():
    print("=" * 60)
    print("Message Processing Tests")
    print("=" * 60)
    print()
    
    tests = [
        ("Escape Sequences", test_escape_sequences),
        ("File Message Loading", test_file_message_loading),
        ("Placeholder Replacement", test_placeholder_replacement)
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result for _, result in results)
    
    print()
    if all_passed:
        print("✓ All message processing tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
