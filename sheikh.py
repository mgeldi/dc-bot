import discord
from datetime import datetime
from discord import app_commands

@app_commands.command(name="sheikh-info", description="Informationen zu Sheikh Dr. Adnan Yusuf Husain")
async def sheikh_info(interaction: discord.Interaction):
    # Geburtsdatum des Sheikh
    birth_date = datetime(1986, 12, 30)

    # Aktuelles Datum
    current_date = datetime.now()

    # Berechnung des Alters
    sheikh_age = current_date.year - birth_date.year - ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))

    embed = discord.Embed(
        title="Sheikh Dr. Adnan Yusuf Husain",
        description="Hier einige Informationen über den Sheikh:",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="📖 Biografie",
        value=(
            f"• Der Sheikh ist {sheikh_age} Jahre alt und begann 2006 sein Studium am Sprachinstitut der Islamischen Universität von Madinah.\n"
            "• 2013 schloss er sein Bachelorstudium in Schari'a an derselben Universität ab.\n"
            "• 2016 erlangte er den Master in Islamwissenschaften mit Schwerpunkt \"Meinungsverschiedenheiten in den Wissenschaften der Schari'a\" an der Ibn-Tofail-Universität in Marokko.\n"
            "• Seine Doktorarbeit im Bereich \"Tafsir\" schloss er 2024 ab.\n"
        ),
        inline=False
    )

    # Erfahrung & Bildung - Fokus auf didaktische und berufliche Expertise
    embed.add_field(
        name="🎓 Erfahrung & Fachgebiete",
        value=(
            "• Über 20 Jahre Erfahrung im Unterrichten von Arabisch als Fremdsprache, sowohl in akademischen als auch in nicht-akademischen Kontexten.\n"
            "• Er entwickelt und unterrichtet maßgeschneiderte Arabischkurse, die auf individuelle Bedürfnisse der Lernenden abgestimmt sind.\n"
            "• Islamische Fachgebiete: Tafsir, Schari'a, arabische Linguistik und die Lehre von Meinungsverschiedenheiten in den islamischen Wissenschaften.\n"
        ),
        inline=False
    )

    embed.add_field(
        name="🗓️ Aktuelle Aktivitäten",
        value=(
            "• Wir freuen uns, euch mitzuteilen, dass unser geschätzter Sheikh am **18. Januar 2025** mit seinem ersten Vortrag beginnen wird.\n"
            "• Ab diesem Zeitpunkt finden die Vorträge bzw. Unterrichte regelmäßig **jeden Sonntag um 11:00 Uhr** statt.\n"
            "• In den Vorträgen habt ihr selbstverständlich die Möglichkeit, live Fragen zu stellen und direkt mit dem Sheikh zu interagieren."
        ),
        inline=False
    )

    embed.add_field(
        name="🔗 Relevante Links",
        value=(
            "• [Website des Sheikh mit kostenlosen Kursen](https://www.islamwissenschaften.com/)\n"
            "• [Arabisch-Kurs auf Skool mit individuellem Lehrplan](https://www.skool.com/lerne-arabisch/about)\n"
            "• [Telegram Gruppe des Sheikhs](https://t.me/adnanyh)"
        ),
        inline=False
    )

    embed.set_footer(text="Wir freuen uns, den Sheikh auf unserem Server begrüßen zu dürfen! Seih live bei seinen Vorträgen dabei!")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1335345553197895732/1335398021214765136/sheikh.jpg?ex=67a005d2&is=679eb452&hm=c0b0d5d664168cb8488659bb096e6de3392755dcd5581c7c412e9a2175396a98&=&format=webp&width=1530&height=1355")

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
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1335345553197895732/1335398127242576005/islamwissenschaften.png?ex=67a005ec&is=679eb46c&hm=95e1f010320158b5fd6fa2fb4a55474e2451335b68fb1024cdbdc995e8f99ea0&=&format=webp&quality=lossless&width=375&height=375")

    await interaction.response.send_message(embed=embed)