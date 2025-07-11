import discord
from discord.ext import commands
from discord import app_commands
import time

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="/", intents=intents)

user_messages = {}

@bot.event
async def on_ready():
    for guild in bot.guilds:
        await bot.tree.sync(guild=guild)
    print(f"{bot.user} aktif ve komutlar yüklendi!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "selam" in message.content.lower():
        await message.channel.send(f"sanada selam pezevenk! {message.author.mention} 👋")

    now = time.time()
    user_id = message.author.id

    if user_id not in user_messages:
        user_messages[user_id] = []

    user_messages[user_id].append((message, now))
    user_messages[user_id] = user_messages[user_id][-6:]

    if len(user_messages[user_id]) == 5:
        # Mesajlar arası farkları kontrol et
        zamanlar = [t for m, t in user_messages[user_id]]
        farklar = [zamanlar[i+1] - zamanlar[i] for i in range(4)]
        
        if all(f <= 1 for f in farklar):
            for msg, _ in user_messages[user_id][1:]:
                try:
                    await msg.delete()
                except:
                    pass
            await message.channel.send(f"{message.author.mention} lütfen spam atmayınız!")
            user_messages[user_id] = []

    await bot.process_commands(message)

@bot.tree.command(name="clear", description="Mesaj siler")
@app_commands.describe(miktar="Silinecek mesaj sayısı")
async def clear(interaction: discord.Interaction, miktar: int = 15):
    if interaction.user.id != interaction.guild.owner_id:
        await interaction.response.send_message("Bu komutu sadece sunucu sahibi kullanabilir.", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=miktar + 1)
    await interaction.followup.send(f"{len(deleted)-1} mesaj silindi.")


bot.run("TOKEN")
