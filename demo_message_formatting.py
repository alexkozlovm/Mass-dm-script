#!/usr/bin/env python3
"""
Demo script to show how messages are formatted and processed
without requiring GUI automation or Discord
"""

from pathlib import Path


def demo_command_line_message():
    """Demonstrate command-line message with newlines."""
    print("=" * 70)
    print("DEMO 1: Command-line message with \\n for newlines")
    print("=" * 70)
    print()
    
    # Simulate what the user would type
    input_message = "# Hello {name}!\\n\\n**Welcome** to our server!\\n\\nJoin us! 🎉"
    print(f"Command: python dm_sender.py users.json \"{input_message}\" --delay 10")
    print()
    
    # Process escape sequences (safely - only \n)
    processed_message = input_message.replace('\\n', '\n')
    
    # Apply placeholders
    user = {"name": "JohnDoe", "display_name": "John Doe", "id": 123456789}
    final_message = processed_message.replace('{name}', user['name'])
    
    print("Message that would be sent to Discord:")
    print("-" * 70)
    print(final_message)
    print("-" * 70)
    print()


def demo_file_message():
    """Demonstrate loading message from a file."""
    print("=" * 70)
    print("DEMO 2: Message loaded from file")
    print("=" * 70)
    print()
    
    print(f"Command: python dm_sender.py users.json --message-file message_example.txt --delay 10")
    print()
    
    # Load the message file
    message_file = Path("message_example.txt")
    with open(message_file, 'r', encoding='utf-8') as f:
        message = f.read()
    
    # Apply placeholders (for demo, we don't have placeholders in the example file)
    user = {"name": "JohnDoe", "display_name": "John Doe", "id": 123456789}
    final_message = message.replace('{name}', user.get('name', ''))
    final_message = final_message.replace('{display_name}', user.get('display_name', ''))
    final_message = final_message.replace('{id}', str(user.get('id', '')))
    
    print("Message that would be sent to Discord:")
    print("-" * 70)
    print(final_message)
    print("-" * 70)
    print()


def demo_with_placeholders():
    """Demonstrate message with personalized placeholders."""
    print("=" * 70)
    print("DEMO 3: File message with placeholders")
    print("=" * 70)
    print()
    
    # Create a sample message with placeholders
    template = """# Hello {name}! 👋

**Welcome {display_name}!**

We're excited to have you join our community!

**Here's what we offer:**
- Free resources 📚
- Active community 💬
- Expert support 🎯

Join us now at: discord.gg/example

Looking forward to seeing you there!"""
    
    print("Template message:")
    print("-" * 70)
    print(template)
    print("-" * 70)
    print()
    
    # Apply placeholders for three different users
    users = [
        {"name": "alice123", "display_name": "Alice Smith"},
        {"name": "bob_dev", "display_name": "Bob Developer"},
        {"name": "charlie", "display_name": "Charlie"}
    ]
    
    print("Personalized messages for each user:")
    print()
    
    for i, user in enumerate(users, 1):
        final_message = template.replace('{name}', user['name'])
        final_message = final_message.replace('{display_name}', user['display_name'])
        
        print(f"User {i}: @{user['name']}")
        print("-" * 70)
        print(final_message)
        print("-" * 70)
        print()


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "MESSAGE FORMATTING DEMONSTRATION" + " " * 21 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    print("This demonstrates the new message formatting features:")
    print("  1. Multiline messages using \\n escape sequences")
    print("  2. Loading messages from text files")
    print("  3. Using placeholders for personalization")
    print()
    
    demo_command_line_message()
    demo_file_message()
    demo_with_placeholders()
    
    print("=" * 70)
    print("TIPS")
    print("=" * 70)
    print()
    print("✓ For short messages, use command line with \\n")
    print("✓ For long messages, use --message-file (easier to edit)")
    print("✓ Use {name}, {display_name}, or {id} for personalization")
    print("✓ Files support markdown formatting (**, #, etc.)")
    print("✓ Emojis work in both methods")
    print()


if __name__ == "__main__":
    main()
