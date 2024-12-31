import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
import requests
import os

# Intents aktivieren
intents = discord.Intents.default()
intents.guilds = True  # Für Guild-Informationen
bot = commands.Bot(command_prefix="/", intents=intents)

# Bot starten
@bot.event
async def on_ready():
    await bot.tree.sync()  # Slash Commands mit Discord synchronisieren

    from roles import AgeDropdownView, CityDropdownView, SchoolDropdownView, BildungsrollenDropdownView
    from verification import VerificationButtons

    bot.add_view(AgeDropdownView())
    bot.add_view(CityDropdownView())
    bot.add_view(SchoolDropdownView())
    bot.add_view(BildungsrollenDropdownView())
    bot.add_view(VerificationButtons())
    print(f"Bot ist online! Eingeloggt als {bot.user}")

if __name__ == "__main__":
    load_dotenv()
    
    from prayer_times import gebetszeiten
    from sheikh import sheikh_info, sheikh_kurse
    from verification import verify_bruder, verify_schwester, setup_verification, ticket_add
    from roles import setup_roles

    bot.tree.add_command(gebetszeiten)
    bot.tree.add_command(sheikh_info)
    bot.tree.add_command(sheikh_kurse)
    bot.tree.add_command(verify_bruder)
    bot.tree.add_command(verify_schwester)
    bot.tree.add_command(setup_verification)
    bot.tree.add_command(ticket_add)
    bot.tree.add_command(setup_roles)

    bot.run(os.getenv("BOT_TOKEN"))