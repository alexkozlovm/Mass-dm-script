# Discord Mass DM Sender

A Python script for automating Discord direct messages using GUI automation on macOS. This script controls the Discord desktop application to send personalized messages to multiple users.

## ⚠️ Important Warnings

**USE AT YOUR OWN RISK!**

- This script may violate Discord's Terms of Service
- Excessive automation can lead to account restrictions or permanent bans
- Always use reasonable delays between messages (minimum 5 seconds recommended)
- Test with a small number of users first
- Ensure you have permission to contact the users
- This tool is for educational purposes only

## Features

- ✅ Automated DM sending through Discord desktop app
- ✅ JSON-based user data import
- ✅ Personalized message templates with placeholders
- ✅ **Support for long, multiline messages with markdown formatting**
- ✅ **Load messages from text files for easier editing**
- ✅ Configurable delays to avoid rate limiting
- ✅ Resume capability (start from specific user index)
- ✅ Comprehensive logging
- ✅ Emergency stop feature (move mouse to corner)
- ✅ Works on macOS

## Requirements

- macOS (tested on macOS 10.14+)
- Python 3.7 or higher
- Discord desktop application
- Accessibility permissions for Terminal/Python

## Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/mikhailkozlov/Mass-dm-script.git
   cd Mass-dm-script
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Grant accessibility permissions:**
   - Go to **System Preferences → Security & Privacy → Privacy → Accessibility**
   - Add and enable Terminal (or your Python IDE)
   - This allows the script to control your mouse and keyboard

## Usage

### Basic Usage

**Simple message:**
```bash
python dm_sender.py users.json "Hello {name}! Welcome to our community!"
```

**Multiline message with markdown (using \n for newlines):**
```bash
python dm_sender.py users.json "# Hello {name}!\n\n**Welcome** to our server!\n\nJoin us at: discord.gg/example"
```

**Load message from a file:**
```bash
python dm_sender.py users.json --message-file message.txt
```

This is the recommended approach for longer, formatted messages. Simply create a text file with your message (see `message_example.txt` for an example).

### Command Line Options

```bash
python dm_sender.py <users_file> [message] [options]

Required:
  users_file          JSON file containing user data

Message (one of):
  message             Message to send (supports placeholders). Use \n for newlines.
  --message-file FILE Read message from a text file

Optional:
  --delay SECONDS    Delay between messages (default: 5, minimum: 5)
  --start INDEX      Start from this user index (default: 0)
  --max COUNT        Maximum messages to send (default: all)
```

### Examples

**Send to all users with 5-second delay:**
```bash
python dm_sender.py users.json "Hey {name}! 👋"
```

**Send with 10-second delay between messages:**
```bash
python dm_sender.py users.json "Hello {display_name}!" --delay 10
```

**Send multiline message with formatting:**
```bash
python dm_sender.py users.json "# Hi {name}!\n\n**Welcome** to our community! 🎉" --delay 10
```

**Send message from a file (recommended for long messages):**
```bash
python dm_sender.py users.json --message-file message.txt --delay 10
```

**Resume from user index 50:**
```bash
python dm_sender.py users.json "Hi there!" --start 50
```

**Send to only 10 users (testing):**
```bash
python dm_sender.py users.json "Test message" --max 10
```

## JSON User Data Format

Your JSON file should contain an array of user objects with the following structure:

```json
[
  {
    "id": 1026118653122461717,
    "name": "username",
    "display_name": "Display Name",
    "joined_at": "2025-09-17T20:19:08.383000+00:00"
  }
]
```

**Required fields:**
- `name` - Discord username (used for searching)

**Optional fields:**
- `id` - User ID
- `display_name` - Display name
- `joined_at` - Join date

See `users_example.json` for a complete example.

## Message Placeholders

You can use the following placeholders in your messages:

- `{name}` - User's username
- `{display_name}` - User's display name
- `{id}` - User's Discord ID

**Example:**
```bash
python dm_sender.py users.json "Hey {name}! Your ID is {id}"
```

## Formatting Long Messages

### Using Message Files (Recommended)

For longer messages with formatting, create a text file with your message:

1. Create a text file (e.g., `message.txt`)
2. Write your message with formatting (markdown, emojis, newlines)
3. Use placeholders like `{name}` where needed
4. Run the script with `--message-file`:

```bash
python dm_sender.py users.json --message-file message.txt --delay 10
```

**Example message file (`message_example.txt`):**
```
# Join the best improvement cord now ❗️


**Free Dropmaps 🗺️**
**Free Coaching 👀**
**Free Improvement Tips 🥳**

**What are you waiting for? Join now!**

https://discord.gg/9pytq7PYx
```

### Using Command Line with \n

You can also use `\n` for newlines in command-line messages:

```bash
python dm_sender.py users.json "# Hello {name}!\n\n**Welcome!** 🎉\n\nJoin us!" --delay 10
```

**Note:** The `--message-file` option is recommended for longer messages as it's easier to write and edit.

## How It Works

1. **GUI Automation:** The script uses PyAutoGUI to control your mouse and keyboard
2. **Discord Search:** Opens Discord's quick switcher (Cmd+K) to search for users
3. **Message Sending:** Types the message and presses Enter
4. **Rate Limiting:** Waits between messages to avoid triggering Discord's spam detection

## Setup Before Running

1. **Open Discord Desktop App:**
   - Make sure you're logged in
   - The app should be visible (not minimized)

2. **Position Discord Window:**
   - Place the Discord window where it's clearly visible
   - Don't overlap with other windows during execution

3. **Prepare Your User Data:**
   - Create a JSON file with your user list
   - Verify the data is correctly formatted

4. **Test First:**
   - Run with `--max 2` to test with just 2 users
   - Verify messages are being sent correctly

## Emergency Stop

If something goes wrong, you can stop the script immediately by:

- Moving your mouse to the **top-left corner** of the screen (PyAutoGUI failsafe)
- Pressing **Ctrl+C** in the terminal

## Logging

The script creates a log file `dm_sender.log` with detailed information about:
- Users processed
- Messages sent/failed
- Any errors encountered

Check this file if you need to troubleshoot issues.

## Best Practices

1. **Start Small:** Test with 2-3 users before sending to hundreds
2. **Use Delays:** Keep delays at 5+ seconds (10+ is safer)
3. **Monitor Activity:** Watch the first few messages to ensure everything works
4. **Respect Users:** Only message users who expect to hear from you
5. **Check Logs:** Review `dm_sender.log` after each run
6. **Stay Compliant:** Be aware of and respect Discord's Terms of Service

## Troubleshooting

**Script not working:**
- Ensure Discord desktop app is open and logged in
- Check that you granted Accessibility permissions
- Verify Discord window is visible (not minimized)
- Make sure your JSON file is properly formatted

**Messages not sending:**
- Increase the delay with `--delay 10`
- Check if usernames in JSON are correct
- Discord search might not find the user if username is wrong

**Getting rate limited:**
- Increase delay between messages (--delay 15 or higher)
- Send fewer messages per session
- Wait a few hours before sending more

**Script stops unexpectedly:**
- Check `dm_sender.log` for error messages
- Ensure Discord window stays focused
- Don't interact with your computer while script is running

## Configuration

The `config.json` file contains:
- Default settings
- Message templates
- Safety warnings

You can modify this file to customize default behavior.

## Limitations

- **macOS Only:** This version is designed for macOS (uses Cmd+K shortcut)
- **GUI Required:** Must have Discord desktop app open and visible
- **Manual Setup:** Requires accessibility permissions
- **Rate Limits:** Discord may still rate limit your account
- **Username Required:** Can only search by username (name field)

## Alternative Approaches

If this script doesn't meet your needs, consider:

1. **Discord Bot API:** Create a proper bot (but bots can't DM users without mutual servers)
2. **User Account Bots:** Against Discord ToS and risky
3. **Manual Messaging:** The safest approach
4. **Discord's Official Features:** Use announcement channels or role mentions

## Contributing

Feel free to submit issues or pull requests if you have improvements!

## License

This project is provided as-is for educational purposes. Use at your own risk.

## Disclaimer

This tool is provided for educational and informational purposes only. The authors are not responsible for any misuse or consequences resulting from the use of this script. Always ensure you comply with Discord's Terms of Service and respect other users' privacy.