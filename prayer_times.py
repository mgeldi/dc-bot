import discord
from discord import app_commands
from datetime import datetime
import requests

@app_commands.command(name="gebetszeiten", description="Zeigt die Gebetszeiten für eine bestimmte Stadt an.")
async def gebetszeiten(interaction: discord.Interaction, stadt: str, öffentlich: bool = False):
    rolle_namen = [role.name for role in interaction.user.roles]
    if "Bruder" not in rolle_namen and "Schwester" not in rolle_namen:
        await interaction.response.send_message("Du hast keine Berechtigung, diesen Befehl zu verwenden.", ephemeral=True)
        return

    gebetszeiten_data = get_prayer_times(stadt)
    if gebetszeiten_data:
        embed = discord.Embed(
            title=f"Gebetszeiten für {stadt}",
            description=f"Datum: {gebetszeiten_data['gregorian_date']} ({gebetszeiten_data['hijri_date']})",
            color=discord.Color.blue()
        )
        for gebet, zeit in gebetszeiten_data['timings'].items():
            embed.add_field(name=gebet, value=zeit, inline=True)
        embed.set_footer(text="Daten bereitgestellt von Aladhan.com")
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1316082550493548614/1321534361933316106/093e98cf90f519920d4569e9d0b69d33813821d55aab1a92b434752e2b5c33f4.png?ex=6774d688&is=67738508&hm=ef5086cc57ec7ad7810af2e065e1220103e5cc9b38e4aacfc5d0834e0ad8a55d&=&format=webp&quality=lossless&width=1355&height=1355")
        await interaction.response.send_message(embed=embed, ephemeral=not öffentlich)
    else:
        await interaction.response.send_message(f"Keine Gebetszeiten für {stadt} gefunden.", ephemeral=True)

def get_prayer_times(stadt):
    current_date = datetime.now().strftime("%d-%m-%Y")
    url = f'https://api.aladhan.com/v1/timingsByCity/{current_date}?city={stadt}&country=DE&method=99&fajr_angle=13.8&isha_angle=15'

    try:
        response = requests.get(url)
        data = response.json()

        if data['code'] == 200:
            timings = {
                'Fajr': data['data']['timings']['Fajr'],
                'Dhuhr': data['data']['timings']['Dhuhr'],
                'Asr': data['data']['timings']['Asr'],
                'Maghrib': data['data']['timings']['Maghrib'],
                'Isha': data['data']['timings']['Isha'],
            }

            gregorian_date = data['data']['date']['gregorian']['date']
            hijri_date = data['data']['date']['hijri']['date']

            return {
                'timings': timings,
                'gregorian_date': gregorian_date,
                'hijri_date': hijri_date
            }
        else:
            return None
    except Exception as e:
        print(f"Fehler beim Abrufen der Gebetszeiten: {e}")
        return None