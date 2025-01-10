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
        name="Biografie",
        value=(
            "• Der Sheikh ist 38 Jahre alt und begann 2006 sein Studium am Sprachinstitut der Islamischen Universität von Madinah.\n"
            "• 2013 schloss er sein Bachelorstudium in Schari'a an derselben Universität ab.\n"
            "• 2016 erlangte er den Master in Islamwissenschaften mit Schwerpunkt \"Meinungsverschiedenheiten in den Wissenschaften der Schari'a\" an der Ibn-Tofail-Universität in Marokko.\n"
            "• Seine Doktorarbeit im Bereich \"Tafsir\" schloss er 2024 ab.\n"
        ),
        inline=False
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
            "[Telegram Gruppe des Sheikhs](https://t.me/adnanyh)"
        ),
        inline=False
    )

    embed.set_footer(text="Wir freuen uns, den Sheikh auf unserem Server begrüßen zu dürfen!")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1316082550493548614/1323708229858889738/sheikh.jpg?ex=67757edb&is=67742d5b&hm=40288fc45a447f4786b0e11a37a53e08fb2ad03e7db4dd8d2d55d5769ad176a1&=&format=webp&width=1530&height=1355")

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