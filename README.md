# Creating a Discord Bot with Mistral's API

In this guide, we'll walk you through the process of creating a Discord bot that utilizes Mistral's API for chat completion.  
This bot will be able to engage in conversations within your Discord server using Mistral's powerful AI capabilities.

## Prerequisites

Before we start, ensure you have the following:

- **Mistral API Key**: Obtain your API key from Mistral's website.
- **Discord Bot Token**: Generate a bot token from the Discord Developer Portal.
- **Python Installed**: Make sure you have Python installed on your system.

## Step 1: Setting Up Dependencies

First, you need to install the necessary Python packages. In your terminal or command prompt, run:

```bash
pip install mistralai discord.py
```

This command installs the Mistral AI client library (`mistralai`) and the Discord.py library (`discord.py`) which is used to interact with Discord's API.

## Step 2: Writing the Bot Code

### Importing Dependencies

In your Python script, begin by importing the required modules:

```python
from mistralai import Mistral
import discord
from discord.ext import commands
```

Here, we import the Mistral class from the Mistral AI library, as well as the necessary components from the Discord.py library.

### Setting Up Mistral's API and Discord Bot Settings

Next, define your Mistral API key, Mistral model, system prompt, Discord bot token, and bot command prefix:

```python
API_KEY = "YOUR_API_KEY"
model = "mistral-small-latest"
system_prompt = "You are an AI Assistant in a Discord Server."
BOT_TOKEN = "YOUR_BOT_TOKEN"
prefix = "mistral!"
```

Replace `"YOUR_API_KEY"` and `"YOUR_BOT_TOKEN"` with your actual Mistral API key and Discord bot token, respectively.

### Creating Client Instances

Create instances of Mistral's API client and Discord bot:

```python
client = Mistral(api_key=API_KEY)
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
```

The `Mistral` is used to interact with Mistral's API. The `commands.Bot` class represents your Discord bot instance.

### Handling Bot's Ready Event

Define an event handler for when the bot is ready:

```python
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="the community!"))
    print("Bot is ready!!")
    print("Here is the invite link:", f"https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=0&scope=bot%20applications.commands")
```

This function sets the bot's status and prints a message to indicate that the bot is ready. It also provides an invite link for adding the bot to a Discord server.

### Cleaning Discord Messages

Define a function to clean Discord messages, replacing the bot's mention with a generic term:

```python
def clean_message_content(message: discord.Message) -> str:
    return message.clean_content.replace('@'+bot.user.name, "Assistant")
```

This function takes a Discord message as input and returns the cleaned content, replacing the bot's mention with "Assistant".

### Handling Message Events

Now, let's handle message events when a user sends a message in the Discord server:

```python
@bot.event
async def on_message(message: discord.Message):

    if bot.user in message.mentions and message.author != bot.user:

        messages = [{"role": "assistant" if m.author == bot.user else "user", "content": clean_message_content(m)} async for m in message.channel.history(limit=5)]
        
        messages = messages[::-1]

        messages = [{"role": "system", "content": system_prompt}] + messages

        response = await client.chat.complete_async(model=model, messages=messages, max_tokens=256)

        response_content = response.choices[0].message.content
        await message.reply(content=response_content)
```

This function is triggered whenever a message is sent in a channel where the bot is present. It checks if the bot is mentioned in the message and if the message author is not the bot itself. If these conditions are met, it collects the last 5 messages from the channel and adds the system prompt, sends them to Mistral for completion, and replies with the generated response.

## Step 3: Running the Bot

Add the following code at the end of your script to run the bot:

```python
bot.run(BOT_TOKEN)
```

This function runs the bot with your specified bot token.

## Done!!

You've now created a Discord bot powered by Mistral's AI API! Your bot is ready to join your Discord server and engage in conversations with your community.

Feel free to customize the bot further based on your preferences and requirements!!

---

Thank You!!
