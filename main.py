# Import the dependencies required to use Mistral's Client. Since Discord works mostly asynchronously, we want the Async Client.
from mistralai.async_client import MistralAsyncClient
from mistralai.models.chat_completion import ChatMessage

# We can then import Discord's dependencies.
import discord
from discord.ext import commands

# Mistral's API KEY and other settings.
API_KEY = "YOUR_API_KEY"
model = "open-mistral-7b"
system_prompt = "You are an AI Assistant in a Discord Server."

# We create the client instance.
client = MistralAsyncClient(api_key = API_KEY)

# Discord bot settings.
BOT_TOKEN = "YOUR_BOT_TOKEN"
prefix = "mistral!"

# We create the bot's instance.
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = prefix, intents = intents)

# This handles when the Discord bot is ready.
@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = "the community!"))
    print("Bot is ready!!")
    print("Here is the invite link:", f"https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=0&scope=bot%20applications.commands")

# A simple function that cleans the Discord messages by removing the bot's mention and replacing it.
def clean_message_content(message: discord.Message) -> str:
    return message.clean_content.replace('@'+bot.user.name, "Assistant")

# The main event that's triggered every time a message is sent.
@bot.event
async def on_message(message: discord.Message):

    # In case a message is sent from someone else and mentions the bot.
    if bot.user in message.mentions and message.author != bot.user:

        # We get all previous messages and make a ChatMessage list. Here we get the previous 5 messages.
        messages = [ChatMessage(role = "assistant" if m.author == bot.user else "user", content = clean_message_content(m)) async for m in message.channel.history(limit = 5)]
        
        # Because of how Discord handles it, we have to reverse the order of the messages since they are originally from the most recent to oldest; we want them from oldest to the most recent.
        messages = messages[::-1]

        # We don't want to forget the system prompt defined earlier.
        messages = [ChatMessage(role = "system", content = system_prompt)] + messages

        # We finally send the request and wait for a response.
        response = await client.chat(model = model, messages = messages, max_tokens = 256)

        # We want to then retrieve the content and reply.
        response_content = response.choices[0].message.content
        await message.reply(content = response_content)

# Everything is ready, we can run the bot!
bot.run(BOT_TOKEN)
