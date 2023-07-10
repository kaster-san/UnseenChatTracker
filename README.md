# UnseenChatTracker

UnseenChatTracker is a Python program that allows you to track and display unseen messages in your private Telegram chats. It helps you keep track of messages you haven't responded to yet, ensuring you don't miss any important conversations. With UnseenChatTracker, you can easily separate and identify unseen messages from your private chats, even when messages from channels and groups flood your chat list. 

Telegram doesn't provide a built-in way to differentiate between private chats, channels, and groups, making it challenging to keep track of unseen messages from individuals. This script addresses that limitation by focusing solely on your private chats and filtering out messages from channels and groups. 

## Features

- Retrieve API ID and API hash from user input or saved configuration
- Create or reuse session files for Telegram authentication
- Track and display unseen messages in private chats
- Option to display results in the terminal or write to a file
- Friendly messages when no unseen messages or chats are found

## Requirements

- Python 3.x
- telethon library (install using `pip install telethon`)

## Getting Started

1. Clone the repository or download the source code.

2. Install the required `telethon` library if you haven't already.
3. Obtain your Telegram API ID and API hash:

- Visit the [Telegram website](https://my.telegram.org/auth) and log in with your phone number.
- Under the **API development tools** section, create a new application.
- Fill in the required information and submit the form.
- You will be provided with an API ID and API hash. Keep these values handy.


4. Run the program: `python unseenchattracker.py`

5. Follow the prompts to input your Telegram API ID, API hash, and session file name (it s just a random name you need to provide for each session).

6. Choose whether you want to display the results in the terminal and/or write them to a file.

7. Sit back and let UnseenChatTracker track and display your unseen messages!

## Configuration

The program uses a `.config` file to store your API ID and API hash for convenience. If the file doesn't exist, it will prompt you to enter them. If the file exists, it will read the values from the file.

## Notes

- It's important to keep your API ID and API hash confidential and not share them with others.
- The program requires appropriate permissions to access your private chats on Telegram.
- UnseenChatTracker does not store or send any data to external servers. All processing is done locally on your machine.

## License

This project is licensed under the [GNUv2 License](LICENSE).
