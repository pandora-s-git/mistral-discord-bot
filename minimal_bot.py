from mistralai.async_client import MistralAsyncClient
from mistralai.models.chat_completion import ChatMessage
import discord
from discord.ext import commands
client = MistralAsyncClient(api_key = "YOUR_API_KEY")
bot = commands.Bot(command_prefix = "mistral!", intents = discord.Intents.all())
@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = "the community!"))
    print("Bot is ready.\nHere is the invite link:", f"https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=0&scope=bot%20applications.commands")
@bot.event
async def on_message(message: discord.Message):
    if bot.user in message.mentions and message.author != bot.user:
        messages = [ChatMessage(role = "system", content = "You are an AI Assistant in a Discord Server.")] + [ChatMessage(role = "assistant" if m.author == bot.user else "user", content = m.clean_content.replace('@'+bot.user.name, "Assistant")) async for m in message.channel.history(limit = 5)][::-1]
        response = await client.chat(model = "open-mistral-7b", messages = messages, max_tokens = 256)
        await message.reply(content = response.choices[0].message.content)
bot.run("YOUR_BOT_TOKEN")