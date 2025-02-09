import discord
from discord import app_commands

SCHOOL_ROLES = ["Hanafi", "Maliki", "Shafi'i", "Hanbali"]

# Hilfsfunktion zum Entfernen anderer Rollen
async def remove_roles_in_category(user, category_roles, guild):
    roles_to_remove = [
        role for role in user.roles if role.name in category_roles
    ]
    if roles_to_remove:
        await user.remove_roles(*roles_to_remove)

def update_dropdown_options(selected_value, options):
    """
    Aktualisiert die Dropdown-Optionen, sodass nur die ausgewählte Option als 'ausgewählt' markiert wird.
    """
    for option in options:
        option.default = (option.value == selected_value)
    return options


# Dropdown-Menü für Altersgruppen
class AgeDropdown(discord.ui.Select):

    def __init__(self):
        options = [
            discord.SelectOption(label="15-20", value="15-20"),
            discord.SelectOption(label="21-25", value="21-25"),
            discord.SelectOption(label="26-30", value="26-30"),
            discord.SelectOption(label="31-35", value="31-35"),
            discord.SelectOption(label="36-40", value="36-40"),
            discord.SelectOption(label="40+", value="40+"),
        ]
        super().__init__(placeholder="Wähle deine Altersgruppe aus",
                         min_values=0,  # Abwählbar
                         max_values=1,
                         options=options,
                         custom_id="age_dropdown")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user_roles = interaction.user.roles

        # Rollen, die durch das Dropdown repräsentiert werden
        valid_roles = [discord.utils.get(guild.roles, name=option.value) for option in self.options]
        valid_roles = [role for role in valid_roles if role is not None]  # Nur existierende Rollen

        # Rollen, die der Benutzer derzeit hat und in diesem Dropdown enthalten sind
        current_roles = set(role for role in user_roles if role in valid_roles)

        # Rollen, die in der aktuellen Auswahl sind
        selected_roles = set(discord.utils.get(guild.roles, name=value) for value in self.values)

        # Rollen, die hinzugefügt oder entfernt werden sollen
        roles_to_add = selected_roles - current_roles
        roles_to_remove = current_roles - selected_roles

        # Änderungen anwenden
        if roles_to_add:
            await interaction.user.add_roles(*roles_to_add)
        if roles_to_remove:
            await interaction.user.remove_roles(*roles_to_remove)

        # Nachricht für den Benutzer
        added_roles = ", ".join([role.name for role in roles_to_add])
        removed_roles = ", ".join([role.name for role in roles_to_remove])

        response_message = "Deine Rollen wurden aktualisiert:\n"
        if roles_to_add:
            response_message += f"✅ Hinzugefügt: {added_roles}\n"
        if roles_to_remove:
            response_message += f"❌ Entfernt: {removed_roles}\n"

        if not roles_to_add and not roles_to_remove:
            response_message = "Keine Änderungen vorgenommen."

        await interaction.response.send_message(response_message, ephemeral=True)


class AgeDropdownView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)  # Persistente View
        self.add_item(AgeDropdown())


# Dropdown-Menü für Städte
class CityDropdown(discord.ui.Select):

    def __init__(self):
        options = [
            # Deutschland 🇩🇪
            discord.SelectOption(label="Baden-Württemberg", value="Baden-Württemberg", emoji="🇩🇪"),
            discord.SelectOption(label="Bayern", value="Bayern", emoji="🇩🇪"),
            discord.SelectOption(label="Berlin", value="Berlin", emoji="🇩🇪"),
            discord.SelectOption(label="Bremen", value="Bremen", emoji="🇩🇪"),
            discord.SelectOption(label="Hamburg", value="Hamburg", emoji="🇩🇪"),
            discord.SelectOption(label="Hessen", value="Hessen", emoji="🇩🇪"),
            discord.SelectOption(label="Mecklenburg-Vorpommern", value="Mecklenburg-Vorpommern", emoji="🇩🇪"),
            discord.SelectOption(label="Niedersachsen", value="Niedersachsen", emoji="🇩🇪"),
            discord.SelectOption(label="Nordrhein-Westfalen", value="Nordrhein-Westfalen", emoji="🇩🇪"),
            discord.SelectOption(label="Rheinland-Pfalz", value="Rheinland-Pfalz", emoji="🇩🇪"),
            discord.SelectOption(label="Saarland", value="Saarland", emoji="🇩🇪"),
            discord.SelectOption(label="Sachsen", value="Sachsen", emoji="🇩🇪"),
            discord.SelectOption(label="Sachsen-Anhalt", value="Sachsen-Anhalt", emoji="🇩🇪"),
            discord.SelectOption(label="Schleswig-Holstein", value="Schleswig-Holstein", emoji="🇩🇪"),
            discord.SelectOption(label="Thüringen", value="Thüringen", emoji="🇩🇪"),

            # Österreich 🇦🇹
            discord.SelectOption(label="Burgenland", value="Burgenland", emoji="🇦🇹"),
            discord.SelectOption(label="Linz", value="Linz", emoji="🇦🇹"),
            discord.SelectOption(label="Niederösterreich", value="Niederösterreich", emoji="🇦🇹"),
            discord.SelectOption(label="Oberösterreich", value="Oberösterreich", emoji="🇦🇹"),
            discord.SelectOption(label="Steiermark", value="Steiermark", emoji="🇦🇹"),
            discord.SelectOption(label="Tirol", value="Tirol", emoji="🇦🇹"),
            discord.SelectOption(label="Wien", value="Wien", emoji="🇦🇹"),

            # Schweiz 🇨🇭
            discord.SelectOption(label="Aargau", value="Aargau", emoji="🇨🇭"),
            discord.SelectOption(label="Bern", value="Bern", emoji="🇨🇭"),
            discord.SelectOption(label="Zürich", value="Zürich", emoji="🇨🇭"),
        ]

        super().__init__(placeholder="Wähle deinen Ort aus",
                         min_values=0,  # Abwählbar
                         max_values=1,
                         options=options,
                         custom_id="city_dropdown")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user_roles = interaction.user.roles

        # Rollen, die durch das Dropdown repräsentiert werden
        valid_roles = [discord.utils.get(guild.roles, name=option.value) for option in self.options]
        valid_roles = [role for role in valid_roles if role is not None]  # Nur existierende Rollen

        # Rollen, die der Benutzer derzeit hat und in diesem Dropdown enthalten sind
        current_roles = set(role for role in user_roles if role in valid_roles)

        # Rollen, die in der aktuellen Auswahl sind
        selected_roles = set(discord.utils.get(guild.roles, name=value) for value in self.values)

        # Rollen, die hinzugefügt oder entfernt werden sollen
        roles_to_add = selected_roles - current_roles
        roles_to_remove = current_roles - selected_roles

        # Änderungen anwenden
        if roles_to_add:
            await interaction.user.add_roles(*roles_to_add)
        if roles_to_remove:
            await interaction.user.remove_roles(*roles_to_remove)

        # Nachricht für den Benutzer
        added_roles = ", ".join([role.name for role in roles_to_add])
        removed_roles = ", ".join([role.name for role in roles_to_remove])

        response_message = "Deine Rollen wurden aktualisiert:\n"
        if roles_to_add:
            response_message += f"✅ Hinzugefügt: {added_roles}\n"
        if roles_to_remove:
            response_message += f"❌ Entfernt: {removed_roles}\n"

        if not roles_to_add and not roles_to_remove:
            response_message = "Keine Änderungen vorgenommen."

        await interaction.response.send_message(response_message, ephemeral=True)


class CityDropdownView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)  # Persistente View
        self.add_item(CityDropdown())

# Dropdown-Menü für Rechtsschulen
class SchoolDropdown(discord.ui.Select):

    def __init__(self):
        # Mapping der Rollen zu Emojis
        school_emojis = {
            "Hanafi": "📕",
            "Maliki": "📙",
            "Shafi'i": "📗",
            "Hanbali": "📘",
        }

        # Optionen mit Emojis erstellen
        options = [
            discord.SelectOption(
                label=school,
                value=school,
                emoji=school_emojis.get(school, "📖")  # Standard-Emoji, falls keine Zuordnung existiert
            ) for school in SCHOOL_ROLES
        ]

        super().__init__(placeholder="Wähle deine Rechtsschule aus",
                         min_values=0,
                         max_values=1,
                         options=options,
                         custom_id="school_dropdown")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user_roles = interaction.user.roles

        # Überprüfen, ob die Rolle existiert
        selected_role_name = self.values[0] if self.values else None
        selected_role = discord.utils.get(guild.roles, name=selected_role_name)

        # Entfernen anderer Schul-Rollen
        school_roles = [
            discord.utils.get(guild.roles, name=school) for school in SCHOOL_ROLES
        ]
        school_roles = [role for role in school_roles if role is not None]

        for role in school_roles:
            if role in user_roles:
                await interaction.user.remove_roles(role)

        # Hinzufügen der ausgewählten Rolle, falls eine gewählt wurde
        if selected_role:
            await interaction.user.add_roles(selected_role)

        response_message = (
            f"Du hast die Rolle **{selected_role_name}** erhalten." 
            if selected_role_name else 
            "Alle Rechtsschulen-Rollen wurden entfernt."
        )

        await interaction.response.send_message(response_message, ephemeral=True)


class SchoolDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Persistente View
        self.add_item(SchoolDropdown())


# Dropdown-Menü für Bildungsrollen
class BildungsrollenDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Quran", value="Quran", emoji="🕋"),
            discord.SelectOption(label="Buchvorlesungen", value="Buchvorlesungen", emoji="📖"),
            discord.SelectOption(label="Vorträge", value="Vorträge", emoji="📚"),
        ]
        super().__init__(placeholder="Wähle deine Bildungsrollen aus",
                         min_values=0,
                         max_values=len(options),
                         options=options,
                         custom_id="bildungsrollen_dropdown")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user_roles = interaction.user.roles

        # Rollen, die durch das Dropdown repräsentiert werden
        valid_roles = [discord.utils.get(guild.roles, name=option.value) for option in self.options]
        valid_roles = [role for role in valid_roles if role is not None]  # Nur existierende Rollen

        # Rollen, die der Benutzer derzeit hat und in diesem Dropdown enthalten sind
        current_roles = set(role for role in user_roles if role in valid_roles)

        # Rollen, die in der aktuellen Auswahl sind
        selected_roles = set(
            discord.utils.get(guild.roles, name=value) for value in self.values if value
        )

        # Rollen, die hinzugefügt oder entfernt werden sollen
        roles_to_add = selected_roles - current_roles
        roles_to_remove = current_roles - selected_roles

        # Änderungen anwenden
        if roles_to_add:
            await interaction.user.add_roles(*roles_to_add)
        if roles_to_remove:
            await interaction.user.remove_roles(*roles_to_remove)

        # Nachricht für den Benutzer
        added_roles = ", ".join([role.name for role in roles_to_add])
        removed_roles = ", ".join([role.name for role in roles_to_remove])

        response_message = "Deine Rollen wurden aktualisiert:\n"
        if roles_to_add:
            response_message += f"✅ Hinzugefügt: {added_roles}\n"
        if roles_to_remove:
            response_message += f"❌ Entfernt: {removed_roles}\n"

        if not roles_to_add and not roles_to_remove:
            response_message = "Keine Änderungen vorgenommen."

        await interaction.response.send_message(response_message, ephemeral=True)


class BildungsrollenDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Persistente View
        self.add_item(BildungsrollenDropdown())


# Slash Command zum Posten der Dropdown-Menüs
@app_commands.command(name="setup_roles", description="Postet die Dropdown-Menüs für die Rollenwahl")
async def setup_roles(interaction: discord.Interaction):
    await interaction.response.send_message("Erstelle Rollen-Auswahl...")

    # Altersgruppen
    embed_age = discord.Embed(title="👥 Wähle deine Altersgruppe",
                              color=discord.Color.blue())
    embed_age.set_image(
        url=
        "https://media.discordapp.net/attachments/1335345553197895732/1336232038180716557/11.png?ex=67a9a60f&is=67a8548f&hm=485fe6090433de2cbd64c6203d4eabbbf749d62cb60fd30519424bbc021d502c&=&format=webp&quality=lossless&width=1440&height=810"
    )  # Thumbnail hinzufügen
    await interaction.channel.send(embed=embed_age, view=AgeDropdownView())

    # Städte
    embed_city = discord.Embed(
        title="🌆 Wähle deinen Ort aus",
        color=discord.Color.green())
    embed_city.set_image(
        url=
        "https://media.discordapp.net/attachments/1335345553197895732/1337067644045754422/Location.png?ex=67a96487&is=67a81307&hm=d6116ee95d796e9212836c799cc8eda1d91f7f340ba961af8160c34ab955fd38&=&format=webp&quality=lossless&width=1440&height=810"
    )
    await interaction.channel.send(embed=embed_city, view=CityDropdownView())

    # Rechtsschulen
    embed_school = discord.Embed(title="📚 Wähle deine Rechtsschule",
                                 color=discord.Color.gold())
    embed_school.set_image(
        url=
        "https://media.discordapp.net/attachments/1335345553197895732/1336232037706633227/9.png?ex=67a9a60f&is=67a8548f&hm=6cd42a8f86874e2b5cd145daea113a4a5898a0480d2287a28c3f4bddaa2871dd&=&format=webp&quality=lossless&width=1440&height=810"
    )
    await interaction.channel.send(embed=embed_school,
                                   view=SchoolDropdownView())

    # Bildungsrollen
    embed_school = discord.Embed(title="📖 Wähle deine islamischen Bildungsrollen",
                                 color=discord.Color.red())
    embed_school.set_image(
        url=
        "https://media.discordapp.net/attachments/1335345553197895732/1336232037954228256/10.png?ex=67a9a60f&is=67a8548f&hm=9aabaaa2cfeb0d57c881677906ee14b6771f1065afd381b6f2cac4d9cfcce0f5&=&format=webp&quality=lossless&width=1440&height=810"
    )
    await interaction.channel.send(embed=embed_school,
                                   view=BildungsrollenDropdownView())
