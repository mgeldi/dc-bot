import discord
from discord import app_commands

@app_commands.command(name="sheikh-info", description="Informationen zu Sheikh Dr. Adnan Yusuf Husain")
async def sheikh_info(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Sheikh Dr. Adnan Yusuf Husain",
        description="Hier einige Informationen über den Sheikh:",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="Erfahrung & Bildung",
        value=(
            "• 20 Jahre Erfahrung im Erlernen und Lehren von Arabisch als Fremdsprache.\n"
            "• Bachelor, Master und Doktorat an renommierten arabischen Universitäten.\n"
            "• Doktor in Tafsir.\n"
        ),
        inline=False
    )

    embed.add_field(
        name="Zukünftige Aktivitäten",
        value=(
            "• Der Sheikh wird voraussichtlich ab Mitte Januar 2025 regelmäßig auf diesem Server aktiv sein.\n"
            "• Geplant sind tiefgehende Vorträge zu verschiedenen islamischen Themengebieten."
        ),
        inline=False
    )

    embed.add_field(
        name="Relevante Links",
        value=(
            "[Website des Sheikh mit kostenlosen Kursen](https://www.islamwissenschaften.com/)\n"
            "[Arabisch Kurs auf Skool mit individuellem Lehrplan](https://www.skool.com/lerne-arabisch/about)\n"
            "[Telegram Gruppe des Sheikh](https://t.me/adnanyh)"
        ),
        inline=False
    )

    embed.set_footer(text="Wir freuen uns, den Sheikh auf unserem Server begrüßen zu dürfen!")

    await interaction.response.send_message(embed=embed)

@app_commands.command(name="sheikh-kurse", description="Informationen zu den angebotenen Kursen vom Sheikh")
async def sheikh_kurse(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Sheikh Dr. Adnan Yusuf Husain - Kurse",
        description="Hier findest du eine Übersicht über die Kurse, die vom Sheikh angeboten werden:",
        color=discord.Color.green()
    )

    embed.add_field(
        name="Kostenlose Kurse - islamwissenschaften.com",
        value=(
            "• Alle Kurse sind kostenlos und beinhalten folgende Themen:\n"
            "  • Aqidah\n"
            "  • Arabisch (Grammatik)\n"
            "  • Fiqh\n"
            "  • Qur'anwissenschaften\n"
            "  • Tafsir\n"
            "  • Usul al-Fiqh\n"
            "• Kursplattform: [Islamwissenschaften.com](https://www.islamwissenschaften.com/courses)"
        ),
        inline=False
    )

    embed.add_field(
        name="Kostenpflichtiger Arabisch-Kurs",
        value=(
            "• Der Sheikh bietet auch einen Arabisch-Kurs an, der auf deinen individuellen Lernplan abgestimmt wird.\n"
            "• Der Kurs ist für alle Lernstufen geeignet und bietet ein personalisiertes Lernerlebnis.\n"
            "• Weitere Informationen findest du hier: [Skool Arabisch-Kurs](https://www.skool.com/lerne-arabisch/about)"
        ),
        inline=False
    )

    embed.add_field(
        name="Warum diese Kurse?",
        value=(
            "• Alle Kurse werden auf Deutsch angeboten.\n"
            "• Du erhältst eine fundierte und strukturierte Ausbildung in den Bereichen Islam und Arabisch.\n"
            "• Der Sheikh hat jahrzehntelange Erfahrung und vermittelt authentisches Wissen gemäß der Ahlus Sunnah wal Jamaah.\n"
            "• Die kostenlose Kursplattform bietet dir Zugang zu einer Vielzahl von Themen, um dein Wissen zu erweitern."
        ),
        inline=False
    )

    embed.set_footer(text="Nutze die Gelegenheit, dein Wissen zu erweitern und in die islamischen Wissenschaften einzutauchen!")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1316082550493548614/1323398851872428143/islamwissenschaften.png?ex=67745eb9&is=67730d39&hm=02ad3e5ffbd39cb64c6ffb1750f63813142f63fa52c4bf4cc6a2a71051fe91bf&=&format=webp&quality=lossless&width=375&height=375")

    await interaction.response.send_message(embed=embed)