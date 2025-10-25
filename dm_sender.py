#!/usr/bin/env python3
"""
Discord Mass DM Sender Script
==============================

This script automates sending direct messages on Discord using GUI automation.
It works by controlling the Discord desktop application on macOS.

⚠️  WARNING: Using this script may violate Discord's Terms of Service.
    Use at your own risk. Excessive automation can lead to account restrictions
    or bans. Always use reasonable delays between messages.

Requirements:
- Discord desktop app must be open and logged in
- Python 3.7+
- Required packages: pyautogui, pyobjc-framework-Quartz (macOS specific)
"""

import json
import time
import sys
import logging
from typing import List, Dict, Optional
from pathlib import Path

try:
    import pyautogui
except ImportError:
    print("Error: pyautogui not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

# Configure PyAutoGUI safety features
pyautogui.FAILSAFE = True  # Move mouse to corner to abort
pyautogui.PAUSE = 1.0  # Default pause between actions

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dm_sender.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants
MIN_DELAY_SECONDS = 5  # Minimum delay to avoid rate limiting


class DiscordDMSender:
    """Automates sending DMs through Discord desktop app using GUI automation."""
    
    def __init__(self, users_file: str, message_template: str, delay: int = 5, search_method: str = 'auto'):
        """
        Initialize the DM sender.
        
        Args:
            users_file: Path to JSON file containing user data
            message_template: Message to send (can include {name} placeholder)
            delay: Delay in seconds between messages (minimum 5 recommended)
            search_method: Method to open search ('cmd_k', 'ctrl_k', 'auto')
        """
        self.users_file = Path(users_file)
        self.message_template = message_template
        self.delay = max(delay, MIN_DELAY_SECONDS)
        self.search_method = search_method
        self.users: List[Dict] = []
        self.sent_count = 0
        self.failed_count = 0
        
    def load_users(self) -> bool:
        """Load user data from JSON file."""
        try:
            with open(self.users_file, 'r') as f:
                data = json.load(f)
                
            # Handle both array of users and single user object
            if isinstance(data, list):
                self.users = data
            else:
                self.users = [data]
                
            logger.info(f"Loaded {len(self.users)} users from {self.users_file}")
            return True
            
        except FileNotFoundError:
            logger.error(f"File not found: {self.users_file}")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {self.users_file}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error loading users: {e}")
            return False
    
    def format_message(self, user: Dict) -> str:
        """Format message with user-specific information."""
        message = self.message_template
        
        # Replace placeholders
        message = message.replace('{name}', user.get('name', ''))
        message = message.replace('{display_name}', user.get('display_name', ''))
        message = message.replace('{id}', str(user.get('id', '')))
        
        return message
    
    def open_discord_search(self) -> bool:
        """
        Open Discord's search/quick switcher using various methods.
        Tries multiple approaches to maximize compatibility.
        """
        methods = []
        
        if self.search_method == 'cmd_k':
            methods = [('command', 'k')]
        elif self.search_method == 'ctrl_k':
            methods = [('ctrl', 'k')]
        else:  # auto - try multiple methods
            methods = [
                ('command', 'k'),  # Standard macOS shortcut
                ('ctrl', 'k'),     # Alternative that works on some systems
                ('cmd', 'k'),      # Another variation
            ]
        
        for method in methods:
            try:
                logger.debug(f"Trying search method: {'+'.join(method)}")
                
                # Press the hotkey
                if len(method) == 2:
                    pyautogui.hotkey(method[0], method[1])
                else:
                    pyautogui.hotkey(*method)
                
                time.sleep(1.5)  # Give more time for UI to respond
                
                # Try typing a space and backspace to test if search opened
                pyautogui.press('space')
                time.sleep(0.1)
                pyautogui.press('backspace')
                time.sleep(0.3)
                
                logger.debug(f"Successfully opened Discord search using {'+'.join(method)}")
                return True
                
            except Exception as e:
                logger.debug(f"Method {'+'.join(method)} failed: {e}")
                # Close any potentially opened dialog
                pyautogui.press('esc')
                time.sleep(0.3)
                continue
        
        logger.error("All search methods failed. Please ensure Discord is focused.")
        return False
    
    def search_user(self, username: str) -> bool:
        """Search for a user in Discord."""
        try:
            # Type username in search
            pyautogui.write(username, interval=0.1)
            time.sleep(1)
            
            # Press Enter to select first result
            pyautogui.press('enter')
            time.sleep(1.5)
            
            logger.debug(f"Searched for user: {username}")
            return True
        except Exception as e:
            logger.error(f"Failed to search for user {username}: {e}")
            return False
    
    def send_message(self, message: str) -> bool:
        """Type and send a message."""
        try:
            # Split message by newlines and handle multi-line messages
            lines = message.split('\n')
            
            for i, line in enumerate(lines):
                # Type the line
                pyautogui.write(line, interval=0.05)
                
                # If not the last line, press Shift+Enter for newline
                if i < len(lines) - 1:
                    pyautogui.hotkey('shift', 'enter')
                    time.sleep(0.1)
            
            time.sleep(0.5)
            
            # Press Enter to send
            pyautogui.press('enter')
            time.sleep(0.5)
            
            logger.debug("Message sent")
            return True
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False
    
    def send_dm_to_user(self, user: Dict) -> bool:
        """Send a DM to a specific user."""
        username = user.get('name', '')
        if not username:
            logger.warning(f"User has no name: {user}")
            return False
        
        logger.info(f"Sending DM to {username} (ID: {user.get('id', 'unknown')})")
        
        try:
            # Open search
            if not self.open_discord_search():
                return False
            
            # Search for user
            if not self.search_user(username):
                # Clear search on failure
                pyautogui.press('esc')
                time.sleep(0.5)
                return False
            
            # Format and send message
            message = self.format_message(user)
            if not self.send_message(message):
                return False
            
            logger.info(f"✓ Successfully sent DM to {username}")
            self.sent_count += 1
            return True
            
        except Exception as e:
            logger.error(f"Error sending DM to {username}: {e}")
            self.failed_count += 1
            return False
    
    def run(self, start_index: int = 0, max_messages: Optional[int] = None):
        """
        Run the DM sending process.
        
        Args:
            start_index: Index to start from (useful for resuming)
            max_messages: Maximum number of messages to send (None = all)
        """
        if not self.load_users():
            logger.error("Failed to load users. Exiting.")
            return
        
        if not self.users:
            logger.error("No users to send messages to.")
            return
        
        # Calculate end index
        end_index = len(self.users)
        if max_messages is not None:
            end_index = min(start_index + max_messages, end_index)
        
        logger.info("=" * 60)
        logger.info("Discord DM Sender Starting")
        logger.info("=" * 60)
        logger.info(f"Total users: {len(self.users)}")
        logger.info(f"Starting from index: {start_index}")
        logger.info(f"Will send to: {end_index - start_index} users")
        logger.info(f"Delay between messages: {self.delay} seconds")
        logger.info("=" * 60)
        logger.info("")
        logger.info("⚠️  Make sure Discord desktop app is open and focused!")
        logger.info("⚠️  Move mouse to top-left corner to emergency stop")
        logger.info("")
        
        # Countdown
        for i in range(5, 0, -1):
            logger.info(f"Starting in {i}...")
            time.sleep(1)
        
        logger.info("Starting now!")
        logger.info("")
        
        # Process users
        for i in range(start_index, end_index):
            user = self.users[i]
            
            logger.info(f"[{i+1}/{end_index}] Processing user...")
            
            # Send DM
            success = self.send_dm_to_user(user)
            
            # Wait before next message (important to avoid rate limiting)
            if i < end_index - 1:  # Don't wait after last message
                logger.info(f"Waiting {self.delay} seconds before next message...")
                time.sleep(self.delay)
        
        # Summary
        logger.info("")
        logger.info("=" * 60)
        logger.info("Summary")
        logger.info("=" * 60)
        logger.info(f"Total processed: {end_index - start_index}")
        logger.info(f"Successfully sent: {self.sent_count}")
        logger.info(f"Failed: {self.failed_count}")
        logger.info("=" * 60)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Discord Mass DM Sender - Automates sending DMs via GUI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Send to all users in users.json with default message
  python dm_sender.py users.json "Hello {name}!"
  
  # Send with custom delay (10 seconds between messages)
  python dm_sender.py users.json "Hi there!" --delay 10
  
  # Send multiline message (use \\n for newlines)
  python dm_sender.py users.json "Hello {name}!\\n\\nWelcome to our server!" --delay 10
  
  # Send message from a file
  python dm_sender.py users.json --message-file message.txt --delay 10
  
  # Resume from user index 50
  python dm_sender.py users.json "Hello!" --start 50
  
  # Send to maximum 10 users
  python dm_sender.py users.json "Hello!" --max 10

⚠️  WARNING: This may violate Discord's Terms of Service. Use at your own risk!
        """
    )
    
    parser.add_argument('users_file', help='JSON file containing user data')
    parser.add_argument('message', nargs='?', default=None,
                       help='Message to send (use {name}, {display_name}, or {id} as placeholders). Use \\n for newlines.')
    parser.add_argument('--message-file', type=str, default=None,
                       help='Read message from a file instead of command line')
    parser.add_argument('--delay', type=int, default=5, 
                       help='Delay in seconds between messages (default: 5, minimum: 5)')
    parser.add_argument('--start', type=int, default=0,
                       help='Start from this user index (default: 0)')
    parser.add_argument('--max', type=int, default=None,
                       help='Maximum number of messages to send (default: all)')
    parser.add_argument('--search-method', type=str, default='auto',
                       choices=['auto', 'cmd_k', 'ctrl_k'],
                       help='Method to open Discord search. "auto" tries multiple methods (default: auto)')
    
    args = parser.parse_args()
    
    # Determine message source
    message = None
    if args.message_file:
        # Read message from file
        try:
            message_path = Path(args.message_file)
            if not message_path.exists():
                logger.error(f"Message file not found: {args.message_file}")
                sys.exit(1)
            with open(message_path, 'r', encoding='utf-8') as f:
                message = f.read()
            logger.info(f"Loaded message from {args.message_file}")
        except Exception as e:
            logger.error(f"Error reading message file: {e}")
            sys.exit(1)
    elif args.message:
        # Use command line message and process only newline escape sequences
        # Only replace \\n with actual newlines for safety (avoid other escape sequences)
        message = args.message.replace('\\n', '\n')
    else:
        logger.error("Error: You must provide either a message or --message-file")
        parser.print_help()
        sys.exit(1)
    
    # Validate delay
    if args.delay < MIN_DELAY_SECONDS:
        logger.warning(f"Delay is less than {MIN_DELAY_SECONDS} seconds. Setting to minimum of {MIN_DELAY_SECONDS} seconds.")
        args.delay = MIN_DELAY_SECONDS
    
    # Create sender and run
    sender = DiscordDMSender(args.users_file, message, args.delay, args.search_method)
    
    try:
        sender.run(start_index=args.start, max_messages=args.max)
    except KeyboardInterrupt:
        logger.info("\n\nInterrupted by user. Exiting...")
    except pyautogui.FailSafeException:
        logger.info("\n\nEmergency stop activated (mouse moved to corner). Exiting...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise


if __name__ == "__main__":
    main()
