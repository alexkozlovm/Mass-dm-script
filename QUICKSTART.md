# Quick Start Guide

## Setup (5 minutes)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Grant permissions:**
   - Open **System Preferences → Security & Privacy → Privacy → Accessibility**
   - Click the lock to make changes
   - Add Terminal (or your Python IDE) to the list
   - Check the box to enable it

3. **Prepare your data:**
   - Create a JSON file with your user list (see `users_example.json`)
   - Or use the example file for testing

4. **Open Discord:**
   - Launch Discord desktop app
   - Make sure you're logged in
   - Keep the window visible

## First Test (2 minutes)

Send a test message to 2 users:

**Option 1: Simple message**
```bash
python dm_sender.py users_example.json "Hey {name}! This is a test." --max 2
```

**Option 2: Using a message file (for longer messages)**
```bash
python dm_sender.py users_example.json --message-file message_example.txt --max 2
```

**What will happen:**
1. Script counts down from 5 seconds
2. Opens Discord search (tries multiple methods automatically)
3. Types the username
4. Sends the message (including all lines and formatting)
5. Waits 5 seconds before next message

## Full Run

Once you've tested and everything works:

**Simple message:**
```bash
python dm_sender.py your_users.json "Your message here {name}" --delay 10
```

**Long formatted message from file:**
```bash
python dm_sender.py your_users.json --message-file your_message.txt --delay 10
```

## Tips

- **Watch the first few messages** to make sure it's working correctly
- **Use longer delays** (10-15 seconds) for large batches to be safer
- **Check the log file** (`dm_sender.log`) to see what happened
- **Emergency stop**: Move mouse to top-left corner or press Ctrl+C

## Troubleshooting

**Script can't control Discord:**
→ Check Accessibility permissions (System Preferences)

**Keyboard shortcut not working:**
→ Try: `python dm_sender.py users.json "Hi!" --search-method ctrl_k`
→ The script tries multiple methods automatically by default

**Wrong messages being sent:**
→ Make sure Discord window is focused and visible

**Getting rate limited:**
→ Increase delay with `--delay 15`

**Script stops early:**
→ Check `dm_sender.log` for error details

## Examples

**Test with 3 users, 8-second delay:**
```bash
python dm_sender.py users.json "Hi {display_name}!" --max 3 --delay 8
```

**Send formatted message from file:**
```bash
python dm_sender.py users.json --message-file message.txt --max 3 --delay 8
```

**Resume from user 50:**
```bash
python dm_sender.py users.json "Hello!" --start 50 --delay 10
```

**Send to all users with 15-second delay:**
```bash
python dm_sender.py users.json "Important update for {name}" --delay 15
```

**Multiline message on command line:**
```bash
python dm_sender.py users.json "# Hello {name}!\n\nWelcome! 🎉" --delay 10
```

## Safety Checklist

Before running for real:

- [ ] Tested with --max 2 or 3 users
- [ ] Verified messages are correct
- [ ] Set appropriate delay (10+ seconds recommended)
- [ ] Have permission to contact these users
- [ ] Understand Discord ToS risks
- [ ] Ready to monitor the process

## Need Help?

1. Read the full [README.md](README.md)
2. Check [config.json](config.json) for settings
3. Review `dm_sender.log` for errors
4. Run tests: `python test_dm_sender.py`

---

⚠️ **Remember**: Use responsibly and at your own risk!
