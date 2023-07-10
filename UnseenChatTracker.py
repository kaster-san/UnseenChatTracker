import configparser
from telethon.sync import TelegramClient, events
import os
import sys

# Check if the .config file exists
config_file = ".config"
config = configparser.ConfigParser()

if os.path.exists(config_file):
    config.read(config_file)

# Create the 'Telegram' section if it doesn't exist
if not config.has_section("Telegram"):
    config.add_section("Telegram")

# Retrieve the API ID and API hash from the .config file if available
api_id = config.get("Telegram", "API_ID", fallback="")
api_hash = config.get("Telegram", "API_HASH", fallback="")

# Ask the user to input API ID and API hash if not found in the .config file
if not api_id:
    api_id = input("Enter your API ID: ")
    config.set("Telegram", "API_ID", api_id)
if not api_hash:
    api_hash = input("Enter your API hash: ")
    config.set("Telegram", "API_HASH", api_hash)

# Save the updated config to the .config file
with open(config_file, "w", encoding='utf-8') as configfile:
    config.write(configfile)

# Get the session file name from the user
session_files = [f for f in os.listdir('.') if f.endswith('.session')]

if session_files:
    print("Existing session files found:")
    for i, session_file in enumerate(session_files):
        print(f"{i+1} - {session_file}")
    print("0 - Create a new session")

    while True:
        choice = input("Select a session number (0 for new session): ")
        if choice.isdigit() and 0 <= int(choice) <= len(session_files):
            break
        else:
            print("Invalid choice. Please try again.")

    if choice == '0':
        session_file = input("Enter your new session file name: ")
    else:
        session_file = session_files[int(choice)-1]
else:
    session_file = input("Enter your session file name: ")

# Check if the session file already exists
if os.path.exists(session_file):
    print("Session file exists. Reusing the existing session.")
else:
    print("Session file does not exist. Creating a new session.")

client = TelegramClient(session_file, api_id, api_hash)

# Keep track of the last seen message ID for each chat
last_seen_message_ids = {}

# Name of the file to write the chat information to
filename = "unseen_messages.txt"

# Ask the user if they want to display the results in the terminal, write to a file, or both
display_results = input("Display results in the terminal? (y/n): ").lower() == "y"
write_to_file = input("Write results to a file? (y/n): ").lower() == "y"

@client.on(events.NewMessage())
async def handle_new_message(event):
    chat_id = event.chat_id
    message = event.message

    # Check if the message is from a person and not a bot, group, or channel
    if message.from_id and message.out and message.chat.type == 'user' and not message.sender.bot:
        # Check if we've already seen this message
        if message.id > last_seen_message_ids.get(chat_id, 0):
            # Update the last seen message ID for this chat
            last_seen_message_ids[chat_id] = message.id

# Start the client and run the event loop
with client:
    # Get all private chats with people (i.e., not bots, groups, or channels)
    all_chats = client.get_dialogs()
    private_chats = [chat for chat in all_chats if chat.is_user and not chat.entity.bot]

    total_chats = len(private_chats)
    processed_chats = 0

    # Loop through the private chats and check if you haven't responded yet
    unseen_chats = []
    for chat in private_chats:
        # Get the last message in the chat
        messages = client.get_messages(chat, limit=1)
        if messages:
            last_message = messages[0]
            # Check if the last message was sent by the other person
            if last_message.from_id != client.get_me().id:
                # Check if you've already seen the last message
                if last_message.id > last_seen_message_ids.get(chat.id, 0):
                    unseen_chats.append((chat.title, chat.id, last_message.message))
        else:
            unseen_chats.append((chat.title, chat.id, None))

        processed_chats += 1
        progress = processed_chats / total_chats * 100

        # Move the cursor to the beginning of the line
        sys.stdout.write("\r")
        # Display the processed chats and the progression bar
        sys.stdout.write(f"Processed chats: {processed_chats}/{total_chats}")
        sys.stdout.write(f"  Progress: [{'#' * int(progress / 10):<10}] {progress:.2f}%")
        sys.stdout.flush()

    sys.stdout.write("\n")  # Move to the next line
    
     if not unseen_chats:
            if display_results:
                print("welp, it looks like you are lonely as always. It's fine, you have me <3")

            if write_to_file:
                with open(filename, "w", encoding='utf-8') as file:
                    file.write("another file goes to waste. It looks like no one likes you.")

    if display_results:
        for chat in unseen_chats:
            if chat[2] is not None:
                print(f"Title: {chat[0]}\nID: {chat[1]}\nLast message: {chat[2]}\n")
            else:
                pass
           

    if write_to_file:
        with open(filename, "w", encoding='utf-8') as file:
            for chat in unseen_chats:
                if chat[2] is not None:
                    file.write(f"Title: {chat[0]}\nID: {chat[1]}\nLast message: {chat[2]}\n\n")
                else:
                    pass

    client.run_until_disconnected()
